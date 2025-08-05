#!/usr/bin/env python3
"""
Debug script for Villa Los Jardines scraper
"""

import requests
from bs4 import BeautifulSoup
import json

def debug_page_structure():
    """Debug the page structure to understand how to extract data."""
    
    url = "https://www.portalinmobiliario.com/venta/casa/rm-metropolitana/nunoa/villa-los-jardines---villa-los-presidentes"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    print("Fetching page...")
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print(f"Page title: {soup.title.string if soup.title else 'No title'}")
    
    # Find property containers
    selectors = [
        '.ui-search-result__wrapper',
        'article',
        '.ui-search-result',
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
        elements = soup.select(selector)
        if elements:
            print(f"\nFound {len(elements)} elements with selector: {selector}")
            
            # Examine first element in detail
            first_element = elements[0]
            print(f"\nFirst element classes: {first_element.get('class', [])}")
            print(f"First element tag: {first_element.name}")
            
            # Look for title
            title_selectors = ['h3', 'h2', 'h1', '.ui-search-item__title', '[class*="title"]']
            for title_sel in title_selectors:
                title_elem = first_element.select_one(title_sel)
                if title_elem:
                    print(f"Title found with {title_sel}: {title_elem.get_text(strip=True)}")
                    break
            
            # Look for price
            price_selectors = ['.ui-search-price__part', '.ui-search-price', '[class*="price"]', '.andes-money-amount']
            for price_sel in price_selectors:
                price_elem = first_element.select_one(price_sel)
                if price_elem:
                    print(f"Price found with {price_sel}: {price_elem.get_text(strip=True)}")
                    break
            
            # Look for details (bedrooms, bathrooms, etc.)
            detail_selectors = ['.ui-search-item__group__element', '[class*="bedroom"]', '[class*="bathroom"]', '[class*="room"]']
            for detail_sel in detail_selectors:
                detail_elems = first_element.select(detail_sel)
                if detail_elems:
                    print(f"Details found with {detail_sel}:")
                    for elem in detail_elems[:3]:  # Show first 3
                        print(f"  - {elem.get_text(strip=True)}")
                    break
            
            # Show raw text (first 500 chars)
            raw_text = first_element.get_text(strip=True)
            print(f"\nRaw text (first 500 chars): {raw_text[:500]}...")
            
            # Save first element HTML for inspection
            with open('debug_first_element.html', 'w', encoding='utf-8') as f:
                f.write(str(first_element))
            print(f"\nSaved first element HTML to debug_first_element.html")
            
            break
    
    # Also save the full page HTML for inspection
    with open('debug_full_page.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"\nSaved full page HTML to debug_full_page.html")

if __name__ == "__main__":
    debug_page_structure() 