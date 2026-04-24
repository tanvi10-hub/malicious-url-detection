"""
Malicious URL Detector Web Application - Flask Backend
Built with Flask, featuring a modern, responsive UI
Group Members: Tanvi Gode, Astha Singh, Gayatri Tasalwar
"""

import logging
import os
import sys
import joblib
import pandas as pd
import requests
from flask import Flask, render_template, request, jsonify
from functools import lru_cache

# Import configuration and utilities
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import current_config
from src.utils import extract_all_features_v2, normalize_url, is_valid_url

# Configure logging
logging.basicConfig(
    level=current_config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.config['SECRET_KEY'] = current_config.SECRET_KEY
MODEL_INIT_ERROR = None


def _download_file(url, destination):
    """Download file from URL to destination path."""
    if not url:
        raise ValueError("Download URL is empty")

    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with requests.get(url, stream=True, timeout=current_config.MODEL_DOWNLOAD_TIMEOUT) as response:
        response.raise_for_status()
        with open(destination, "wb") as file_handle:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file_handle.write(chunk)


def _ensure_model_file(path, url, file_label):
    """Ensure model artifacts exist locally; optionally download them."""
    if os.path.exists(path):
        return

    if not current_config.AUTO_DOWNLOAD_MODELS:
        raise FileNotFoundError(f"{file_label} file not found: {path}")

    logger.info(f"{file_label} missing. Downloading from configured URL.")
    _download_file(url, path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"{file_label} download failed: {path}")

# Load models safely
@lru_cache(maxsize=1)
def load_models():
    """Load ML models from disk (cached)"""
    try:
        _ensure_model_file(
            current_config.MODEL_PATH,
            current_config.MODEL_URL,
            "Model"
        )
        _ensure_model_file(
            current_config.ENCODER_PATH,
            current_config.ENCODER_URL,
            "Encoder"
        )
        
        model = joblib.load(current_config.MODEL_PATH)
        encoder = joblib.load(current_config.ENCODER_PATH)
        logger.info("Models loaded successfully")
        return model, encoder
    except Exception as e:
        logger.error(f"Failed to load models: {str(e)}")
        raise

# Load models on startup
try:
    model, encoder = load_models()
except Exception as e:
    logger.error(f"Critical error: {str(e)}")
    model = None
    encoder = None
    MODEL_INIT_ERROR = str(e)


def ensure_models_loaded():
    """Load models lazily if startup load failed."""
    global model, encoder, MODEL_INIT_ERROR
    if model is not None and encoder is not None:
        return True, None

    try:
        model, encoder = load_models()
        MODEL_INIT_ERROR = None
        return True, None
    except Exception as e:
        MODEL_INIT_ERROR = str(e)
        logger.error(f"Lazy model load failed: {MODEL_INIT_ERROR}")
        return False, MODEL_INIT_ERROR

@app.route('/')
def home():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for deployment monitoring"""
    ok, error = ensure_models_loaded()
    if not ok:
        return jsonify({'status': 'unhealthy', 'error': f'Models not loaded: {error}'}), 500
    return jsonify({'status': 'healthy'}), 200

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    API endpoint for URL analysis
    
    Expected JSON payload:
        {
            "url": "https://example.com"
        }
    
    Returns:
        JSON response with prediction, confidence, and features
    """
    try:
        # Check if models are loaded
        ok, error = ensure_models_loaded()
        if not ok:
            logger.error("Models not loaded")
            return jsonify({'error': f'Service unavailable: Models not loaded ({error})'}), 503
        
        # Get URL from request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request: JSON body required'}), 400
        
        url = data.get('url', '').strip()
        
        # Validate URL
        if not url:
            return jsonify({'error': 'Please enter a URL'}), 400
        
        # Normalize URL
        normalized_url = normalize_url(url)
        
        # Check URL format
        if not is_valid_url(normalized_url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Check URL length
        if len(normalized_url) > int(os.getenv('MAX_URL_LENGTH', 2000)):
            return jsonify({'error': 'URL is too long'}), 400
        
        logger.info(f"Analyzing URL: {normalized_url[:50]}...")
        
        # Extract features
        try:
            features_dict = extract_all_features_v2(
                normalized_url,
                current_config.TRUSTED_DOMAINS,
                current_config.SUSPICIOUS_KEYWORDS
            )
        except ValueError as e:
            logger.error(f"Feature extraction error: {str(e)}")
            return jsonify({'error': f'Feature extraction failed: {str(e)}'}), 400
        except Exception as e:
            logger.error(f"Unexpected error during feature extraction: {str(e)}")
            return jsonify({'error': 'Feature extraction failed'}), 500
        
        # Check if trusted domain
        import tldextract
        try:
            extracted = tldextract.extract(normalized_url)
            domain_name = extracted.domain.lower()
            is_trusted = domain_name in current_config.TRUSTED_DOMAINS
        except Exception as e:
            logger.warning(f"Error checking trusted domain: {str(e)}")
            is_trusted = False
        
        # Generate prediction
        if is_trusted:
            result = {
                'url': normalized_url,
                'prediction': 'BENIGN',
                'confidence': 100.0,
                'reason': 'Trusted domain whitelist',
                'safe': True,
                'probabilities': {
                    'benign': 1.0,
                    'phishing': 0.0,
                    'malware': 0.0,
                    'defacement': 0.0
                },
                'features': features_dict
            }
            logger.info(f"URL classified as BENIGN (trusted domain)")
        else:
            try:
                features_df = pd.DataFrame([features_dict])
                pred = model.predict(features_df)[0]
                prob_vals = model.predict_proba(features_df)[0]
                label = encoder.inverse_transform([pred])[0]
                confidence = float(max(prob_vals))
                
                result = {
                    'url': normalized_url,
                    'prediction': label.upper(),
                    'confidence': confidence * 100,
                    'reason': 'ML Model Prediction (Random Forest)',
                    'safe': label.lower() == 'benign',
                    'probabilities': {
                        lbl: float(prob) for lbl, prob in zip(encoder.classes_, prob_vals)
                    },
                    'features': features_dict
                }
                logger.info(f"URL classified as {label.upper()} with confidence {confidence*100:.2f}%")
            except Exception as e:
                logger.error(f"Model prediction error: {str(e)}")
                return jsonify({'error': 'Model prediction failed'}), 500
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Unexpected error in analyze endpoint: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    try:
        logger.info(f"Starting Flask app in {current_config.FLASK_ENV} mode")
        app.run(
            debug=current_config.DEBUG,
            host=current_config.HOST,
            port=current_config.PORT,
            use_reloader=False
        )
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        sys.exit(1)