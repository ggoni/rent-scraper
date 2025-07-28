#!/usr/bin/env python3
"""
Portal Inmobiliario Rental Property Scraper - Selenium Version

This scraper uses Selenium WebDriver to handle JavaScript-rendered content
and provides more accurate data extraction for dynamic websites.
"""

import time
import json
import csv
import logging
import re
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

import config


class PortalInmobiliarioScraper:
    """Selenium-based scraper for Portal Inmobiliario rental properties."""
    
    def __init__(self):
        """Initialize the scraper with configuration."""
        self.base_url = config.BASE_URL
        self.max_pages = config.MAX_PAGES
        self.delay_between_pages = config.DELAY_BETWEEN_PAGES
        self.delay_between_requests = config.DELAY_BETWEEN_REQUESTS
        self.headless_mode = config.HEADLESS_MODE
        self.browser_window_size = config.BROWSER_WINDOW_SIZE
        self.user_agent = config.USER_AGENT
        self.timeout = config.PAGE_LOAD_TIMEOUT
        self.max_retries = config.MAX_RETRIES
        self.retry_delay = config.RETRY_DELAY
        
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, config.LOG_LEVEL),
            format=config.LOG_FORMAT,
            handlers=[
                logging.FileHandler(config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize data storage
        self.properties = []
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options."""
        try:
            chrome_options = Options()
            
            if self.headless_mode:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument(f"--window-size={self.browser_window_size}")
            chrome_options.add_argument(f"--user-agent={self.user_agent}")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-javascript")
            
            # Use webdriver-manager to automatically download and manage ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(self.timeout)
            
            self.logger.info("Chrome WebDriver setup completed successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to setup Chrome WebDriver: {e}")
            raise
    
    def extract_property_data(self, property_element) -> Optional[Dict]:
        """Extract property data from a single property element."""
        try:
            property_data = {
                'price': None,
                'location': None,
                'bedrooms': None,
                'bathrooms': None,
                'square_meters': None,
                'raw_text': '',
                'timestamp': datetime.now().isoformat()
            }
            
            # Get the raw text for debugging
            raw_text = property_element.text.strip()
            property_data['raw_text'] = raw_text
            
            # Extract price
            for pattern in config.PRICE_PATTERNS:
                match = re.search(pattern, raw_text)
                if match:
                    price_str = match.group(1).replace(',', '')
                    try:
                        property_data['price'] = int(price_str)
                        break
                    except ValueError:
                        continue
            
            # Extract square meters
            for pattern in config.SQUARE_METERS_PATTERNS:
                match = re.search(pattern, raw_text)
                if match:
                    try:
                        property_data['square_meters'] = int(match.group(1))
                        break
                    except ValueError:
                        continue
            
            # Extract bedrooms
            for pattern in config.BEDROOMS_PATTERNS:
                match = re.search(pattern, raw_text)
                if match:
                    try:
                        property_data['bedrooms'] = int(match.group(1))
                        break
                    except ValueError:
                        continue
            
            # Extract bathrooms
            for pattern in config.BATHROOMS_PATTERNS:
                match = re.search(pattern, raw_text)
                if match:
                    try:
                        property_data['bathrooms'] = int(match.group(1))
                        break
                    except ValueError:
                        continue
            
            # Extract location/address
            for pattern in config.ADDRESS_PATTERNS:
                match = re.search(pattern, raw_text)
                if match:
                    property_data['location'] = match.group(0).strip()
                    break
            
            # Validate data
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
        # Check if we have at least some basic data
        if not data.get('price') and not data.get('location'):
            return False
        
        # Validate price range
        if data.get('price'):
            if not (config.MIN_PRICE <= data['price'] <= config.MAX_PRICE):
                return False
        
        # Validate square meters
        if data.get('square_meters'):
            if not (config.MIN_SQUARE_METERS <= data['square_meters'] <= config.MAX_SQUARE_METERS):
                return False
        
        return True
    
    def scrape_page(self, url: str) -> List[Dict]:
        """Scrape a single page and extract property data."""
        properties = []
        
        try:
            self.logger.info(f"Scraping page: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Find property containers
            property_elements = []
            for selector in config.PROPERTY_SELECTORS:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        property_elements = elements
                        self.logger.info(f"Found {len(elements)} properties using selector: {selector}")
                        break
                except NoSuchElementException:
                    continue
            
            if not property_elements:
                self.logger.warning("No property elements found on page")
                return properties
            
            # Extract data from each property
            for element in property_elements:
                property_data = self.extract_property_data(element)
                if property_data:
                    properties.append(property_data)
                    self.logger.debug(f"Extracted property: {property_data.get('price')} CLP")
            
            self.logger.info(f"Successfully extracted {len(properties)} properties from page")
            
        except TimeoutException:
            self.logger.error(f"Timeout while loading page: {url}")
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
        if "json" in config.OUTPUT_FORMATS:
            json_filename = f"{config.OUTPUT_PREFIX}_{timestamp}.json"
            try:
                with open(json_filename, 'w', encoding=config.ENCODING) as f:
                    json.dump(self.properties, f, indent=2, ensure_ascii=False)
                self.logger.info(f"Data exported to JSON: {json_filename}")
            except Exception as e:
                self.logger.error(f"Error exporting to JSON: {e}")
        
        # Export to CSV
        if "csv" in config.OUTPUT_FORMATS:
            csv_filename = f"{config.OUTPUT_PREFIX}_{timestamp}.csv"
            try:
                with open(csv_filename, 'w', newline='', encoding=config.ENCODING) as f:
                    if self.properties:
                        fieldnames = self.properties[0].keys()
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(self.properties)
                self.logger.info(f"Data exported to CSV: {csv_filename}")
            except Exception as e:
                self.logger.error(f"Error exporting to CSV: {e}")
    
    def run(self):
        """Main method to run the scraper."""
        try:
            self.logger.info("Starting Portal Inmobiliario scraper (Selenium version)")
            
            # Setup WebDriver
            self.setup_driver()
            
            # Scrape all pages
            self.scrape_all_pages()
            
            # Export data
            self.export_data()
            
            self.logger.info("Scraping completed successfully!")
            
        except Exception as e:
            self.logger.error(f"Scraping failed: {e}")
            raise
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("WebDriver closed")


def main():
    """Main function to run the scraper."""
    scraper = PortalInmobiliarioScraper()
    scraper.run()


if __name__ == "__main__":
    main() 