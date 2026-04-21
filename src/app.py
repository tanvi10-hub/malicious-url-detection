"""
Malicious URL Detector Web Application - Flask Backend
Built with Flask, featuring a modern, responsive UI
Group Members: Tanvi Gode, Astha Singh, Gayatri Tasalwar
"""

from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import re
import math
import tldextract
from urllib.parse import urlparse
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Trusted Domains
TRUSTED_DOMAINS = {
    'google', 'youtube', 'facebook', 'twitter', 'instagram',
    'linkedin', 'microsoft', 'apple', 'amazon', 'netflix',
    'github', 'wikipedia', 'reddit', 'yahoo', 'bing', 'adobe',
    'dropbox', 'spotify', 'paypal', 'ebay', 'whatsapp',
    'telegram', 'zoom', 'slack', 'wordpress', 'shopify', 'salesforce'
}

def extract_all_features_v2(url):
    """Extract all features from URL"""
    basic = {
        'url_length': len(url), 'num_dots': url.count('.'), 'num_hyphens': url.count('-'),
        'num_underscores': url.count('_'), 'num_slashes': url.count('/'), 'num_at': url.count('@'),
        'num_question': url.count('?'), 'num_equals': url.count('='), 'num_ampersand': url.count('&'),
        'num_digits': sum(c.isdigit() for c in url), 'num_special_chars': len(re.findall(r'[^a-zA-Z0-9]', url)),
    }
    security = {
        'has_https': 1 if url.startswith('https') else 0, 'has_http': 1 if url.startswith('http') else 0,
        'has_ip_address': 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0, 'has_at_symbol': 1 if '@' in url else 0,
        'has_double_slash': 1 if '//' in url[7:] else 0, 'has_prefix_suffix': 1 if '-' in urlparse(url).netloc else 0,
    }
    try:
        extracted = tldextract.extract(url)
        parsed    = urlparse(url)
        domain    = extracted.domain
        subdomain = extracted.subdomain
        suffix    = extracted.suffix
        path      = parsed.path
        query     = parsed.query
        domain_f  = {
            'domain_length'     : len(domain),
            'subdomain_length'  : len(subdomain),
            'tld_length'        : len(suffix),
            'path_length'       : len(path),
            'query_length'      : len(query),
            'num_subdomains'    : len(subdomain.split('.')) if subdomain else 0,
            'is_trusted_domain' : 1 if domain.lower() in TRUSTED_DOMAINS else 0,
        }
    except:
        domain_f = {
            'domain_length': 0, 'subdomain_length': 0, 'tld_length': 0, 'path_length': 0,
            'query_length': 0, 'num_subdomains': 0, 'is_trusted_domain': 0,
        }
    
    prob = [url.count(c) / len(url) for c in set(url)]
    entropy = -sum(p * math.log2(p) for p in prob)
    entropy_f = {'url_entropy': round(entropy, 4)}

    suspicious_keywords = ['login', 'verify', 'secure', 'account', 'update', 'banking', 'confirm', 'password', 'signin', 'wallet', 'free', 'lucky', 'winner', 'click', 'setup', 'install']
    keyword_f = {'has_suspicious_keyword': 1 if any(kw in url.lower() for kw in suspicious_keywords) else 0}
    
    features = {}
    features.update(basic)
    features.update(security)
    features.update(domain_f)
    features.update(entropy_f)
    features.update(keyword_f)
    return features

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """API endpoint for URL analysis"""
    data = request.json
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'Please enter a URL'}), 400
    
    try:
        model = joblib.load(r'D:\malicious-url-detection\models\rf_model_v2.pkl')
        encoder = joblib.load(r'D:\malicious-url-detection\models\label_encoder.pkl')
    except Exception as e:
        return jsonify({'error': f'Model loading error: {str(e)}'}), 500
    
    try:
        extracted = tldextract.extract(url)
        domain_name = extracted.domain.lower()
        is_trusted = domain_name in TRUSTED_DOMAINS
    except:
        is_trusted = False
    
    if is_trusted:
        result = {
            'url': url,
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
            'features': extract_all_features_v2(url)
        }
    else:
        features = pd.DataFrame([extract_all_features_v2(url)])
        pred = model.predict(features)[0]
        prob_vals = model.predict_proba(features)[0]
        label = encoder.inverse_transform([pred])[0]
        confidence = float(max(prob_vals))
        
        result = {
            'url': url,
            'prediction': label.upper(),
            'confidence': confidence * 100,
            'reason': 'ML Model Prediction (Random Forest)',
            'safe': label.lower() == 'benign',
            'probabilities': {
                lbl: float(prob) for lbl, prob in zip(encoder.classes_, prob_vals)
            },
            'features': extract_all_features_v2(url)
        }
    
    return jsonify(result)

if __name__ == '__main__':
    import os
    debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)