"""
Configuration file for Portal Inmobiliario scraper
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URL for the scraper
BASE_URL = "https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana"

# Scraping settings - can be overridden by environment variables
MAX_PAGES = int(os.getenv('SCRAPER_MAX_PAGES', 3))  # Maximum number of pages to scrape
DELAY_BETWEEN_PAGES = int(os.getenv('SCRAPER_DELAY', 2))  # Seconds to wait between page requests
DELAY_BETWEEN_REQUESTS = 3  # Seconds to wait between individual requests

# Browser settings (for Selenium scraper)
HEADLESS_MODE = os.getenv('SCRAPER_HEADLESS', 'true').lower() == 'true'  # Set to False for debugging
BROWSER_WINDOW_SIZE = "1920,1080"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# API Keys (load from environment variables)
MAP_API_KEY = os.getenv('MAP_API_KEY')  # Google Maps API key if needed
EXTERNAL_API_KEY = os.getenv('EXTERNAL_API_KEY')  # Any external API keys

# Output settings
OUTPUT_FORMATS = ["csv", "json"]  # Available: "csv", "json"
OUTPUT_PREFIX = "rental_properties"

# Data extraction patterns
PRICE_PATTERNS = [
    r'\$\s*([\d,]+)',
    r'(\d+)\s*pesos',
    r'(\d+)\s*CLP'
]

SQUARE_METERS_PATTERNS = [
    r'(\d+)\s*m²',
    r'(\d+)\s*metros',
    r'(\d+)\s*m2'
]

BEDROOMS_PATTERNS = [
    r'(\d+)\s*dormitorio',
    r'(\d+)\s*habitación',
    r'(\d+)\s*pieza'
]

BATHROOMS_PATTERNS = [
    r'(\d+)\s*baño',
    r'(\d+)\s*baños'
]

# Address patterns for Santiago neighborhoods
ADDRESS_PATTERNS = [
    r'Santiago.*?(?=\$|\d+\s*m²)',
    r'Barrio.*?(?=\$|\d+\s*m²)',
    r'[A-Z][a-z]+.*?Santiago',
    r'[A-Z][a-z]+.*?RM'
]

# Property container selectors (CSS selectors to find property listings)
PROPERTY_SELECTORS = [
    'article',
    '.ui-search-result',
    '.ui-search-result__wrapper',
    '[data-testid*="result"]',
    '.ui-search-result__content',
    'div[class*="result"]',
    'div[class*="item"]',
    'div[class*="property"]',
    'div[class*="listing"]'
]

# Logging settings
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "scraper.log"
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# Request headers for simple scraper
REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Timeout settings
REQUEST_TIMEOUT = 30  # Seconds
PAGE_LOAD_TIMEOUT = 10  # Seconds for Selenium

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 5  # Seconds

# Data validation
MIN_PRICE = 100000  # Minimum valid price in CLP
MAX_PRICE = 10000000  # Maximum valid price in CLP
MIN_SQUARE_METERS = 20  # Minimum valid square meters
MAX_SQUARE_METERS = 500  # Maximum valid square meters

# Filter settings (optional - set to None to disable)
MIN_BEDROOMS = None  # Minimum number of bedrooms to include
MAX_BEDROOMS = None  # Maximum number of bedrooms to include
MIN_BATHROOMS = None  # Minimum number of bathrooms to include
MAX_BATHROOMS = None  # Maximum number of bathrooms to include
MIN_PRICE_FILTER = None  # Minimum price filter
MAX_PRICE_FILTER = None  # Maximum price filter

# Export settings
INCLUDE_RAW_TEXT = True  # Include raw text in output for debugging
INCLUDE_TIMESTAMP = True  # Include timestamp in output
ENCODING = 'utf-8'  # Output file encoding 