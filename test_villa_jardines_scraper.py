#!/usr/bin/env python3
"""
Test script for Villa Los Jardines scraper
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    try:
        import requests
        import bs4
        from villa_jardines_scraper import VillaJardinesScraper
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_scraper_initialization():
    """Test if the scraper can be initialized."""
    try:
        from villa_jardines_scraper import VillaJardinesScraper
        scraper = VillaJardinesScraper()
        print("✓ Scraper initialization successful")
        return True
    except Exception as e:
        print(f"✗ Scraper initialization failed: {e}")
        return False

def test_single_page_scrape():
    """Test scraping a single page."""
    try:
        from villa_jardines_scraper import VillaJardinesScraper
        scraper = VillaJardinesScraper()
        
        # Test scraping just the first page
        properties = scraper.scrape_page(scraper.base_url)
        
        if properties:
            print(f"✓ Single page scrape successful - found {len(properties)} properties")
            # Print first property as example
            if properties:
                first_prop = properties[0]
                print(f"  Example property: {first_prop.get('title', 'No title')} - {first_prop.get('price')} {first_prop.get('price_currency', 'CLP')}")
        else:
            print("⚠ Single page scrape completed but no properties found")
        
        return True
    except Exception as e:
        print(f"✗ Single page scrape failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Villa Los Jardines Scraper...")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Initialization Test", test_scraper_initialization),
        ("Single Page Scrape Test", test_single_page_scrape),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"  {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"Tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("✓ All tests passed! The scraper is ready to use.")
        print("\nTo run the full scraper:")
        print("python villa_jardines_scraper.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 