import re
from urllib.parse import urlparse

def clean_price(price_str):
    """Clean and convert price string to float"""
    if not price_str:
        return 0.0
    
    # Remove currency symbols and thousands separators
    cleaned = re.sub(r'[^\d.,]', '', price_str)
    cleaned = cleaned.replace(',', '')
    
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def get_domain_from_url(url):
    """Extract domain from URL"""
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    domain = domain.split('/')[0]
    return domain

def extract_currency(price_str):
    """Extract currency symbol or code from price string"""
    if not price_str:
        return 'INR'
    
    # Look for currency symbols
    currency_map = {
        '$': 'USD',
        '€': 'EUR',
        '£': 'GBP',
        '₹': 'INR'
    }
    
    for symbol, code in currency_map.items():
        if symbol in price_str:
            return code
    
    # Look for currency codes
    match = re.search(r'([A-Z]{3})', price_str)
    if match:
        return match.group(1)
    
    return 'INR'

def validate_url(url):
    """Basic URL validation"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False