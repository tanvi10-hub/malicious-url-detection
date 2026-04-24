#!/usr/bin/env python3
"""
Malicious URL Detector - Minimalist CLI Version
Runs URL predictions using trained models without Flask
"""

import sys
import os
import logging
import pandas as pd
import joblib

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import current_config
from src.utils import extract_all_features_v2, normalize_url, is_valid_url

# Configure logging
logging.basicConfig(
    level=current_config.LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_models():
    """Load ML models from disk"""
    try:
        if not os.path.exists(current_config.MODEL_PATH):
            logger.error(f"Model file not found: {current_config.MODEL_PATH}")
            return None, None
        
        if not os.path.exists(current_config.ENCODER_PATH):
            logger.error(f"Encoder file not found: {current_config.ENCODER_PATH}")
            return None, None
        
        model = joblib.load(current_config.MODEL_PATH)
        encoder = joblib.load(current_config.ENCODER_PATH)
        logger.info("Models loaded successfully")
        return model, encoder
    except Exception as e:
        logger.error(f"Failed to load models: {str(e)}")
        return None, None


def analyze_url(url, model, encoder):
    """
    Analyze a single URL
    
    Args:
        url (str): URL to analyze
        model: Trained ML model
        encoder: Label encoder for predictions
    
    Returns:
        bool: True if analysis successful, False otherwise
    """
    if model is None or encoder is None:
        logger.error("Models not loaded")
        return False
    
    # Normalize and validate URL
    normalized_url = normalize_url(url)
    if not is_valid_url(normalized_url):
        print(f"❌ Invalid URL format: {url}")
        return False
    
    print("\n" + "="*80)
    print(f"URL: {normalized_url}")
    print("="*80)
    
    try:
        # Extract features
        features_dict = extract_all_features_v2(
            normalized_url,
            current_config.TRUSTED_DOMAINS,
            current_config.SUSPICIOUS_KEYWORDS
        )
        
        # Check if trusted domain
        import tldextract
        extracted = tldextract.extract(normalized_url)
        domain_name = extracted.domain.lower()
        is_trusted = domain_name in current_config.TRUSTED_DOMAINS
        
        if is_trusted:
            print("✅ PREDICTION:  BENIGN")
            print("🔒 REASON:     Trusted Domain Whitelist")
            print("📊 CONFIDENCE: 100.00%")
        else:
            # Make prediction
            features_df = pd.DataFrame([features_dict])
            pred = model.predict(features_df)[0]
            prob_vals = model.predict_proba(features_df)[0]
            label = encoder.inverse_transform([pred])[0]
            confidence = max(prob_vals) * 100
            
            # Display results
            status_icon = "✅" if label.lower() == "benign" else "⚠️"
            print(f"{status_icon} PREDICTION:  {label.upper()}")
            print(f"🔒 REASON:     ML Model Prediction (Random Forest)")
            print(f"📊 CONFIDENCE: {confidence:.2f}%")
            print("\n📈 CLASS PROBABILITIES:")
            for lbl, prob in sorted(zip(encoder.classes_, prob_vals), key=lambda x: -x[1]):
                bar_length = int(prob * 20)
                bar = "█" * bar_length + "░" * (20 - bar_length)
                print(f"   {lbl:12} [{bar}] {prob*100:6.2f}%")
        
        print("\n📋 EXTRACTED FEATURES:")
        # Display key features
        key_features = [
            'url_length', 'has_https', 'has_ip_address', 
            'num_dots', 'domain_length', 'is_trusted_domain',
            'has_suspicious_keyword', 'url_entropy'
        ]
        for feat in key_features:
            if feat in features_dict:
                print(f"   {feat:25} = {features_dict[feat]}")
        
        print("="*80 + "\n")
        return True
    
    except Exception as e:
        logger.error(f"Error analyzing URL: {str(e)}")
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Main CLI function"""
    print("\n🛡️  Malicious URL Detector - CLI Version")
    print("="*80)
    
    # Load models
    model, encoder = load_models()
    if model is None or encoder is None:
        print("❌ Failed to load models. Exiting.")
        sys.exit(1)
    
    # Process command line arguments
    if len(sys.argv) > 1:
        success_count = 0
        total_count = 0
        
        for url in sys.argv[1:]:
            total_count += 1
            if analyze_url(url, model, encoder):
                success_count += 1
        
        print(f"Analyzed {success_count}/{total_count} URLs successfully")
        sys.exit(0 if success_count == total_count else 1)
    else:
        print("\n📝 Usage: python app_simple.py <url1> [url2] [url3] ...")
        print("\n📌 Examples:")
        print("   python app_simple.py https://www.google.com")
        print("   python app_simple.py http://example.com https://github.com")
        print("\n" + "="*80)
        sys.exit(0)


if __name__ == "__main__":
    main()
