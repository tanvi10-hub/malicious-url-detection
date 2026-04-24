"""
Utility functions for URL feature extraction and analysis
Shared across all application versions
"""

import re
import math
import logging
from urllib.parse import urlparse
import tldextract

logger = logging.getLogger(__name__)


def extract_all_features_v2(url, trusted_domains, suspicious_keywords):
    """
    Extract all features from URL for ML model prediction
    
    Args:
        url (str): URL to analyze
        trusted_domains (set): Set of trusted domain names
        suspicious_keywords (list): List of suspicious keywords
    
    Returns:
        dict: Dictionary containing all extracted features
    
    Raises:
        ValueError: If URL is empty or None
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    # Basic features
    basic = {
        'url_length': len(url),
        'num_dots': url.count('.'),
        'num_hyphens': url.count('-'),
        'num_underscores': url.count('_'),
        'num_slashes': url.count('/'),
        'num_at': url.count('@'),
        'num_question': url.count('?'),
        'num_equals': url.count('='),
        'num_ampersand': url.count('&'),
        'num_digits': sum(c.isdigit() for c in url),
        'num_special_chars': len(re.findall(r'[^a-zA-Z0-9]', url)),
    }
    
    # Security features
    security = {
        'has_https': 1 if url.startswith('https') else 0,
        'has_http': 1 if url.startswith('http') else 0,
        'has_ip_address': 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        'has_at_symbol': 1 if '@' in url else 0,
        'has_double_slash': 1 if '//' in url[7:] else 0,
        'has_prefix_suffix': 1 if '-' in urlparse(url).netloc else 0,
    }
    
    # Domain features
    try:
        extracted = tldextract.extract(url)
        parsed = urlparse(url)
        domain = extracted.domain
        subdomain = extracted.subdomain
        suffix = extracted.suffix
        path = parsed.path
        query = parsed.query
        
        domain_f = {
            'domain_length': len(domain),
            'subdomain_length': len(subdomain),
            'tld_length': len(suffix),
            'path_length': len(path),
            'query_length': len(query),
            'num_subdomains': len(subdomain.split('.')) if subdomain else 0,
            'is_trusted_domain': 1 if domain.lower() in trusted_domains else 0,
        }
    except Exception as e:
        logger.warning(f"Error extracting domain features: {e}")
        domain_f = {
            'domain_length': 0,
            'subdomain_length': 0,
            'tld_length': 0,
            'path_length': 0,
            'query_length': 0,
            'num_subdomains': 0,
            'is_trusted_domain': 0,
        }
    
    # Entropy feature
    try:
        if len(url) > 0:
            prob = [url.count(c) / len(url) for c in set(url)]
            entropy = -sum(p * math.log2(p) for p in prob if p > 0)
            entropy_f = {'url_entropy': round(entropy, 4)}
        else:
            entropy_f = {'url_entropy': 0.0}
    except Exception as e:
        logger.warning(f"Error calculating entropy: {e}")
        entropy_f = {'url_entropy': 0.0}
    
    # Keyword feature
    keyword_f = {
        'has_suspicious_keyword': 1 if any(kw in url.lower() for kw in suspicious_keywords) else 0
    }
    
    # Combine all features
    features = {}
    features.update(basic)
    features.update(security)
    features.update(domain_f)
    features.update(entropy_f)
    features.update(keyword_f)
    
    return features


def is_valid_url(url):
    """
    Validate URL format
    
    Args:
        url (str): URL to validate
    
    Returns:
        bool: True if URL is valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    try:
        result = urlparse(url)
        # Check if URL has scheme and netloc
        has_scheme = bool(result.scheme)
        has_netloc = bool(result.netloc)
        return has_scheme and has_netloc
    except Exception:
        return False


def normalize_url(url):
    """
    Normalize URL by adding https:// if no protocol specified
    
    Args:
        url (str): URL to normalize
    
    Returns:
        str: Normalized URL
    """
    if not url:
        return url
    
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url
