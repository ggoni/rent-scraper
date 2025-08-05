#!/usr/bin/env python3
"""
Portal Inmobiliario Villa Los Jardines Scraper

Specialized scraper for Villa Los Jardines - Villa Los Presidentes neighborhood
URL: https://www.portalinmobiliario.com/venta/casa/rm-metropolitana/nunoa/villa-los-jardines---villa-los-presidentes
"""

import time
import json
import csv
import logging
import re
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class VillaJardinesScraper:
    """Specialized scraper for Villa Los Jardines - Villa Los Presidentes properties."""
    
    def __init__(self):
        """Initialize the scraper with Villa Los Jardines specific configuration."""
        self.base_url = "https://www.portalinmobiliario.com/venta/casa/rm-metropolitana/nunoa/villa-los-jardines---villa-los-presidentes"
        self.max_pages = 10  # Adjust based on actual page count
        self.delay_between_pages = 3
        self.delay_between_requests = 2
        self.timeout = 30
        self.max_retries = 3
        self.retry_delay = 5
        
        # Headers optimized for Portal Inmobiliario
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('villa_jardines_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize data storage
        self.properties = []
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Villa Los Jardines specific patterns
        self.price_patterns = [
            r'\$([\d,]+)',
            r'UF([\d,]+)',
            r'(\d+)\s*pesos',
            r'(\d+)\s*CLP'
        ]
        
        self.square_meters_patterns = [
            r'(\d+)\s*m²\s*útiles',
            r'(\d+)\s*m²',
            r'(\d+)\s*metros',
            r'(\d+)\s*m2'
        ]
        
        self.bedrooms_patterns = [
            r'(\d+)\s*dormitorio',
            r'(\d+)\s*habitación',
            r'(\d+)\s*pieza'
        ]
        
        self.bathrooms_patterns = [
            r'(\d+)\s*baño',
            r'(\d+)\s*baños'
        ]
        
        self.address_patterns = [
            r'[A-Z][a-z]+.*?Ñuñoa',
            r'[A-Z][a-z]+.*?Villa Los Jardínes',
            r'[A-Z][a-z]+.*?Villa Los Presidentes',
            r'[A-Z][a-z]+.*?Región Metropolitana'
        ]
    
    def make_request(self, url: str) -> Optional[BeautifulSoup]:
        """Make HTTP request and return BeautifulSoup object."""
        for attempt in range(self.max_retries):
            try:
                self.logger.debug(f"Making request to: {url} (attempt {attempt + 1})")
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                return soup
                
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    self.logger.error(f"All retry attempts failed for: {url}")
                    return None
        
        return None
    
    def extract_property_data(self, property_element) -> Optional[Dict]:
        """Extract property data from a single property element."""
        try:
            property_data = {
                'title': None,
                'price': None,
                'price_currency': None,
                'location': None,
                'bedrooms': None,
                'bathrooms': None,
                'square_meters': None,
                'address': None,
                'features': [],
                'raw_text': '',
                'timestamp': datetime.now().isoformat()
            }
            
            # Get the raw text for debugging
            raw_text = property_element.get_text(strip=True)
            property_data['raw_text'] = raw_text
            
            # Extract title - look for specific title classes
            title_selectors = [
                '.poly-component__title',
                'h3',
                'h2', 
                'h1',
                '.ui-search-item__title',
                '[class*="title"]',
                '[class*="name"]'
            ]
            
            for selector in title_selectors:
                title_element = property_element.select_one(selector)
                if title_element:
                    title_text = title_element.get_text(strip=True)
                    if title_text and len(title_text) > 5:  # Basic validation
                        property_data['title'] = title_text
                        break
            
            # Extract price - look for price elements first, then use regex
            price_selectors = [
                '.poly-component__price .andes-money-amount__fraction',
                '.andes-money-amount__fraction',
                '.ui-search-price__part',
                '.ui-search-price',
                '[class*="price"]',
                '.andes-money-amount'
            ]
            
            for selector in price_selectors:
                price_element = property_element.select_one(selector)
                if price_element:
                    price_text = price_element.get_text(strip=True)
                    # For the specific Portal Inmobiliario format, try direct extraction first
                    if price_text and price_text.replace('.', '').replace(',', '').isdigit():
                        try:
                            property_data['price'] = int(price_text.replace('.', '').replace(',', ''))
                            property_data['price_currency'] = 'CLP'
                            break
                        except ValueError:
                            pass
                    
                    # Try to extract price from the element text using patterns
                    for pattern in self.price_patterns:
                        match = re.search(pattern, price_text)
                        if match:
                            price_str = match.group(1).replace(',', '').replace('.', '')
                            try:
                                property_data['price'] = int(price_str)
                                if 'UF' in price_text:
                                    property_data['price_currency'] = 'UF'
                                else:
                                    property_data['price_currency'] = 'CLP'
                                break
                            except ValueError:
                                continue
            
            # If no price found in elements, try regex on raw text
            if not property_data.get('price'):
                for pattern in self.price_patterns:
                    match = re.search(pattern, raw_text)
                    if match:
                        price_str = match.group(1).replace(',', '').replace('.', '')
                        try:
                            property_data['price'] = int(price_str)
                            if 'UF' in pattern:
                                property_data['price_currency'] = 'UF'
                            else:
                                property_data['price_currency'] = 'CLP'
                            break
                        except ValueError:
                            continue
            
            # Extract square meters - look for specific elements first
            square_meters_selectors = [
                '.poly-attributes_list__item',
                '[class*="size"]',
                '[class*="area"]',
                '[class*="meters"]'
            ]
            
            for selector in square_meters_selectors:
                element = property_element.select_one(selector)
                if element:
                    element_text = element.get_text(strip=True)
                    for pattern in self.square_meters_patterns:
                        match = re.search(pattern, element_text)
                        if match:
                            try:
                                property_data['square_meters'] = int(match.group(1))
                                break
                            except ValueError:
                                continue
            
            # If no square meters found in elements, try regex on raw text
            if not property_data.get('square_meters'):
                for pattern in self.square_meters_patterns:
                    match = re.search(pattern, raw_text)
                    if match:
                        try:
                            property_data['square_meters'] = int(match.group(1))
                            break
                        except ValueError:
                            continue
            
            # Extract bedrooms and bathrooms - look for specific elements first
            details_selectors = [
                '.poly-attributes_list__item',
                '[class*="bedroom"]',
                '[class*="bathroom"]',
                '[class*="room"]',
                '.ui-search-item__group__element'
            ]
            
            for selector in details_selectors:
                elements = property_element.select(selector)
                for element in elements:
                    element_text = element.get_text(strip=True)
                    
                    # Check for bedrooms
                    if not property_data.get('bedrooms'):
                        for pattern in self.bedrooms_patterns:
                            match = re.search(pattern, element_text)
                            if match:
                                try:
                                    property_data['bedrooms'] = int(match.group(1))
                                    break
                                except ValueError:
                                    continue
                    
                    # Check for bathrooms
                    if not property_data.get('bathrooms'):
                        for pattern in self.bathrooms_patterns:
                            match = re.search(pattern, element_text)
                            if match:
                                try:
                                    property_data['bathrooms'] = int(match.group(1))
                                    break
                                except ValueError:
                                    continue
            
            # If not found in elements, try regex on raw text
            if not property_data.get('bedrooms'):
                for pattern in self.bedrooms_patterns:
                    match = re.search(pattern, raw_text)
                    if match:
                        try:
                            property_data['bedrooms'] = int(match.group(1))
                            break
                        except ValueError:
                            continue
            
            if not property_data.get('bathrooms'):
                for pattern in self.bathrooms_patterns:
                    match = re.search(pattern, raw_text)
                    if match:
                        try:
                            property_data['bathrooms'] = int(match.group(1))
                            break
                        except ValueError:
                            continue
            
            # Extract address/location
            address_selectors = [
                '.poly-component__location',
                '[class*="location"]',
                '[class*="address"]',
                '[class*="neighborhood"]'
            ]
            
            for selector in address_selectors:
                element = property_element.select_one(selector)
                if element:
                    address_text = element.get_text(strip=True)
                    if address_text and len(address_text) > 5:
                        property_data['address'] = address_text
                        break
            
            # If no address found in elements, try regex on raw text
            if not property_data.get('address'):
                for pattern in self.address_patterns:
                    match = re.search(pattern, raw_text)
                    if match:
                        property_data['address'] = match.group(0).strip()
                        break
            
            # Extract features (garden, parking, etc.)
            features = []
            feature_keywords = ['jardín', 'estacionamiento', 'piscina', 'parrilla', 'alarma', 'aire acondicionado', 'gimnasio', 'quincho']
            for keyword in feature_keywords:
                if keyword in raw_text.lower():
                    features.append(keyword)
            property_data['features'] = features
            
            # More lenient validation for this specific area
            if self._validate_property_data(property_data):
                return property_data
            else:
                self.logger.debug(f"Property data validation failed: {property_data}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error extracting property data: {e}")
            return None
    
    def _validate_property_data(self, data: Dict) -> bool:
        """Validate extracted property data."""
        # More lenient validation for Villa Los Jardines area
        # Check if we have at least some basic data
        if not data.get('price') and not data.get('title'):
            return False
        
        # Validate price range (more lenient for this area)
        if data.get('price'):
            if data.get('price_currency') == 'UF':
                if not (100 <= data['price'] <= 50000):  # Wider UF range
                    return False
            else:  # CLP
                if not (10000000 <= data['price'] <= 1000000000):  # Wider CLP range
                    return False
        
        # Validate square meters (more lenient)
        if data.get('square_meters'):
            if not (20 <= data['square_meters'] <= 1000):
                return False
        
        return True
    
    def scrape_page(self, url: str) -> List[Dict]:
        """Scrape a single page and extract property data."""
        properties = []
        
        try:
            self.logger.info(f"Scraping page: {url}")
            soup = self.make_request(url)
            
            if not soup:
                self.logger.error(f"Failed to get page content: {url}")
                return properties
            
            # Find property containers - multiple selectors for Portal Inmobiliario
            property_elements = []
            selectors = [
                'article',
                '.ui-search-result',
                '.ui-search-result__wrapper',
                '[data-testid*="result"]',
                '.ui-search-result__content',
                'div[class*="result"]',
                'div[class*="item"]',
                'div[class*="property"]',
                'div[class*="listing"]',
                'li[class*="result"]',
                'div[class*="card"]'
            ]
            
            for selector in selectors:
                try:
                    elements = soup.select(selector)
                    if elements:
                        property_elements = elements
                        self.logger.info(f"Found {len(elements)} properties using selector: {selector}")
                        break
                except Exception:
                    continue
            
            if not property_elements:
                self.logger.warning("No property elements found on page")
                return properties
            
            # Extract data from each property
            for element in property_elements:
                property_data = self.extract_property_data(element)
                if property_data:
                    properties.append(property_data)
                    self.logger.debug(f"Extracted property: {property_data.get('title', 'No title')} - {property_data.get('price')} {property_data.get('price_currency', 'CLP')}")
            
            self.logger.info(f"Successfully extracted {len(properties)} properties from page")
            
        except Exception as e:
            self.logger.error(f"Error scraping page {url}: {e}")
        
        return properties
    
    def scrape_all_pages(self):
        """Scrape all pages within the configured limit."""
        self.logger.info(f"Starting to scrape up to {self.max_pages} pages")
        
        for page in range(1, self.max_pages + 1):
            try:
                # Construct page URL
                if page == 1:
                    url = self.base_url
                else:
                    url = f"{self.base_url}?page={page}"
                
                # Scrape the page
                page_properties = self.scrape_page(url)
                
                if not page_properties:
                    self.logger.info(f"No properties found on page {page}, stopping pagination")
                    break
                
                self.properties.extend(page_properties)
                
                self.logger.info(f"Page {page}: Found {len(page_properties)} properties")
                
                # Delay between pages
                if page < self.max_pages:
                    self.logger.info(f"Waiting {self.delay_between_pages} seconds before next page...")
                    time.sleep(self.delay_between_pages)
                
            except Exception as e:
                self.logger.error(f"Error scraping page {page}: {e}")
                break
        
        self.logger.info(f"Scraping completed. Total properties found: {len(self.properties)}")
    
    def export_data(self):
        """Export scraped data to CSV and JSON files."""
        if not self.properties:
            self.logger.warning("No properties to export")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export to JSON
        json_filename = f"villa_jardines_properties_{timestamp}.json"
        try:
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(self.properties, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Data exported to JSON: {json_filename}")
        except Exception as e:
            self.logger.error(f"Error exporting to JSON: {e}")
        
        # Export to CSV
        csv_filename = f"villa_jardines_properties_{timestamp}.csv"
        try:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                if self.properties:
                    fieldnames = self.properties[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.properties)
            self.logger.info(f"Data exported to CSV: {csv_filename}")
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {e}")
    
    def print_summary(self):
        """Print a summary of the scraped data."""
        if not self.properties:
            print("No properties found.")
            return
        
        print(f"\n=== VILLA LOS JARDINES SCRAPING SUMMARY ===")
        print(f"Total properties found: {len(self.properties)}")
        
        # Price statistics
        prices = [p['price'] for p in self.properties if p.get('price')]
        if prices:
            print(f"Price range: ${min(prices):,} - ${max(prices):,} CLP")
            print(f"Average price: ${sum(prices)//len(prices):,} CLP")
        
        # Bedroom statistics
        bedrooms = [p['bedrooms'] for p in self.properties if p.get('bedrooms')]
        if bedrooms:
            print(f"Bedroom range: {min(bedrooms)} - {max(bedrooms)}")
            print(f"Average bedrooms: {sum(bedrooms)/len(bedrooms):.1f}")
        
        # Square meters statistics
        square_meters = [p['square_meters'] for p in self.properties if p.get('square_meters')]
        if square_meters:
            print(f"Size range: {min(square_meters)} - {max(square_meters)} m²")
            print(f"Average size: {sum(square_meters)/len(square_meters):.1f} m²")
        
        print("=" * 50)
    
    def run(self):
        """Main method to run the scraper."""
        try:
            self.logger.info("Starting Villa Los Jardines scraper")
            self.logger.info(f"Target URL: {self.base_url}")
            
            # Scrape all pages
            self.scrape_all_pages()
            
            # Print summary
            self.print_summary()
            
            # Export data
            self.export_data()
            
            self.logger.info("Scraping completed successfully!")
            
        except Exception as e:
            self.logger.error(f"Scraping failed: {e}")
            raise
        finally:
            self.session.close()


def main():
    """Main function to run the scraper."""
    scraper = VillaJardinesScraper()
    scraper.run()


if __name__ == "__main__":
    main() 