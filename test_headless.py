#!/usr/bin/env python3
"""
Test script to verify headless browser configuration
"""
import os
from playwright.sync_api import sync_playwright

def test_headless():
    """Test if browser launches in headless mode"""
    print("🧪 Testing headless browser configuration...")
    
    # Check environment variable
    headless_mode = os.getenv('PLAYWRIGHT_HEADLESS', 'true').lower() == 'true'
    print(f"🔧 PLAYWRIGHT_HEADLESS: {os.getenv('PLAYWRIGHT_HEADLESS', 'not set')}")
    print(f"🖥️ Browser mode: {'Headless' if headless_mode else 'Headed'}")
    
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=headless_mode, slow_mo=0)
            print("✅ Browser launched successfully!")
            
            context = browser.new_context()
            page = context.new_page()
            
            # Simple test navigation
            page.goto("https://www.google.com")
            title = page.title()
            print(f"📄 Page title: {title}")
            
            browser.close()
            print("✅ Test completed successfully!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_headless()
    exit(0 if success else 1)
