#!/usr/bin/env python3
"""
Malicious URL Detector - Command Line Interface
Analyzes URLs for malicious/phishing/malware/defacement indicators
"""

import sys
import pandas as pd
import joblib
import re
import math
import tldextract
from urllib.parse import urlparse

# ─── Trusted Domains ────────────────────────────────────
TRUSTED_DOMAINS = {
    'google', 'youtube', 'facebook', 'twitter', 'instagram',
    'linkedin', 'microsoft', 'apple', 'amazon', 'netflix',
    'github', 'wikipedia', 'reddit', 'yahoo', 'bing', 'adobe',
    'dropbox', 'spotify', 'paypal', 'ebay', 'whatsapp',
    'telegram', 'zoom', 'slack', 'wordpress', 'shopify', 'salesforce'
}

def extract_all_features_v2(url):
    """Extract all features from a URL"""
    basic = {
        'url_length'        : len(url),
        'num_dots'          : url.count('.'),
        'num_hyphens'       : url.count('-'),
        'num_underscores'   : url.count('_'),
        'num_slashes'       : url.count('/'),
        'num_at'            : url.count('@'),
        'num_question'      : url.count('?'),
        'num_equals'        : url.count('='),
        'num_ampersand'     : url.count('&'),
        'num_digits'        : sum(c.isdigit() for c in url),
        'num_special_chars' : len(re.findall(r'[^a-zA-Z0-9]', url)),
    }
    security = {
        'has_https'         : 1 if url.startswith('https') else 0,
        'has_http'          : 1 if url.startswith('http') else 0,
        'has_ip_address'    : 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        'has_at_symbol'     : 1 if '@' in url else 0,
        'has_double_slash'  : 1 if '//' in url[7:] else 0,
        'has_prefix_suffix' : 1 if '-' in urlparse(url).netloc else 0,
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
            'domain_length'     : 0,
            'subdomain_length'  : 0,
            'tld_length'        : 0,
            'path_length'       : 0,
            'query_length'      : 0,
            'num_subdomains'    : 0,
            'is_trusted_domain' : 0,
        }
    
    prob      = [url.count(c) / len(url) for c in set(url)]
    entropy   = -sum(p * math.log2(p) for p in prob)
    entropy_f = {'url_entropy': round(entropy, 4)}

    suspicious_keywords = [
        'login', 'verify', 'secure', 'account', 'update',
        'banking', 'confirm', 'password', 'signin', 'wallet',
        'free', 'lucky', 'winner', 'click', 'setup', 'install'
    ]
    keyword_f = {
        'has_suspicious_keyword': 1 if any(
            kw in url.lower() for kw in suspicious_keywords
        ) else 0
    }
    features = {}
    features.update(basic)
    features.update(security)
    features.update(domain_f)
    features.update(entropy_f)
    features.update(keyword_f)
    return features

def predict_url(url):
    """Predict if URL is malicious"""
    try:
        model   = joblib.load(r'D:\malicious-url-detection\models\rf_model_v2.pkl')
        encoder = joblib.load(r'D:\malicious-url-detection\models\label_encoder.pkl')
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return

    # Rule-based pre-check
    try:
        extracted   = tldextract.extract(url)
        domain_name = extracted.domain.lower()
        is_trusted  = domain_name in TRUSTED_DOMAINS
    except:
        is_trusted = False

    print("\n" + "=" * 60)
    print(f"🔍 URL        : {url}")
    print("=" * 60)

    if is_trusted:
        print(f"🏷️  Prediction : ✅ BENIGN")
        print(f"📊 Confidence : 100.00%")
        print(f"ℹ️  Reason     : Trusted domain whitelist")
    else:
        features   = pd.DataFrame([extract_all_features_v2(url)])
        pred       = model.predict(features)[0]
        prob_vals  = model.predict_proba(features)[0]
        label      = encoder.inverse_transform([pred])[0]
        confidence = max(prob_vals)

        emoji_map = {
            'benign'     : '✅',
            'phishing'   : '🎣',
            'malware'    : '☠️',
            'defacement' : '🔨'
        }

        emoji = emoji_map.get(label, '⚪')
        print(f"🏷️  Prediction : {emoji} {label.upper()}")
        print(f"📊 Confidence : {confidence * 100:.2f}%")
        print("-" * 60)
        print("📈 Probabilities by Class:")
        for lbl, prob in sorted(zip(encoder.classes_, prob_vals), key=lambda x: -x[1]):
            em = emoji_map.get(lbl, '⚪')
            bar = '█' * int(prob * 25)
            print(f"   {em} {lbl:<12} {prob*100:>6.2f}%  {bar}")

    print("=" * 60 + "\n")

def main():
    """Main CLI interface"""
    print("\n🔍 Malicious URL Detector - Command Line Tool")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # URL provided as argument
        url = sys.argv[1]
        predict_url(url)
    else:
        # Interactive mode
        print("Enter URLs to analyze (type 'quit' to exit)\n")
        while True:
            try:
                url = input("Enter URL (or 'quit'): ").strip()
                if url.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                if not url:
                    print("⚠️  Please enter a URL\n")
                    continue
                predict_url(url)
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    main()
