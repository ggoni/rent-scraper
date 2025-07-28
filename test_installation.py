#!/usr/bin/env python3
"""
Test script for Portal Inmobiliario scraper installation and basic functionality.
"""

import sys
import importlib
import logging
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing module imports...")
    
    required_modules = [
        'requests',
        'bs4',
        'selenium',
        'pandas',
        'lxml',
        'fake_useragent',
        'webdriver_manager',
        'dotenv'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️  Failed to import: {', '.join(failed_imports)}")
        print("💡 Try installing missing dependencies:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All required modules imported successfully!")
        return True

def test_config():
    """Test if configuration can be loaded."""
    print("\n🔧 Testing configuration...")
    
    try:
        import config
        print("✅ Configuration loaded successfully")
        
        # Test environment variable loading
        print(f"   Base URL: {config.BASE_URL}")
        print(f"   Max Pages: {config.MAX_PAGES}")
        print(f"   Headless Mode: {config.HEADLESS_MODE}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_basic_functionality():
    """Test basic scraper functionality."""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test simple scraper
        from simple_scraper_no_selenium import MinimalPortalInmobiliarioScraper
        
        scraper = MinimalPortalInmobiliarioScraper()
        print("✅ Minimal scraper initialized successfully")
        
        # Test a simple request
        import requests
        response = requests.get("https://www.google.com", timeout=5)
        print("✅ Network connectivity test passed")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable loading."""
    print("\n🔐 Testing environment variables...")
    
    try:
        from dotenv import load_dotenv
        import os
        
        # Load environment variables
        load_dotenv()
        
        # Test if we can access environment variables
        scraper_delay = os.getenv('SCRAPER_DELAY', '3')
        scraper_max_pages = os.getenv('SCRAPER_MAX_PAGES', '3')
        
        print(f"✅ Environment variables loaded:")
        print(f"   SCRAPER_DELAY: {scraper_delay}")
        print(f"   SCRAPER_MAX_PAGES: {scraper_max_pages}")
        
        return True
    except Exception as e:
        print(f"❌ Environment variable test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Portal Inmobiliario Scraper - Installation Test")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("Basic Functionality", test_basic_functionality),
        ("Environment Variables", test_environment_variables)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your installation is ready.")
        print("\n📝 Next steps:")
        print("   1. Set up your .env.local file with your settings")
        print("   2. Run: python scraper.py (Selenium version)")
        print("   3. Or run: python simple_scraper.py (Requests version)")
        print("   4. Or run: python simple_scraper_no_selenium.py (Minimal version)")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n💡 Troubleshooting:")
        print("   - Install missing dependencies: pip install -r requirements.txt")
        print("   - For compilation issues, try: pip install -r requirements-minimal.txt")
        print("   - Check your Python version (requires 3.8+)")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 