#!/usr/bin/env python3
"""
Browser Configuration for Portaliano Automation
================================================

This file controls browser behavior for all automation scripts.
Simply change HEADLESS_MODE to switch between visible and headless browser.

Usage:
- HEADLESS_MODE = False  -> Browser window visible (for development/debugging)
- HEADLESS_MODE = False   -> Browser runs in background (for production/server)
"""

# Browser Configuration
HEADLESS_MODE = True  # Change this to True for headless mode, False to show browser

# Browser Arguments (for optimization)
BROWSER_ARGS = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-features=VizDisplayCompositor',
    '--disable-web-security',
    '--disable-blink-features=AutomationControlled',
    '--disable-extensions'
]

# Browser Speed (milliseconds delay between actions)
SLOW_MO = 100  # Increased from 0 to prevent timeout issues

# Timeout Configuration (milliseconds)
DEFAULT_TIMEOUT = 60000  # 60 seconds default timeout
NAVIGATION_TIMEOUT = 90000  # 90 seconds for page navigation
ACTION_TIMEOUT = 45000  # 45 seconds for click/type actions

def get_browser_config():
    """
    Get browser configuration for automation scripts.
    
    Returns:
        dict: Browser configuration with headless mode, args, slow_mo, and timeouts
    """
    return {
        'headless': HEADLESS_MODE,
        'args': BROWSER_ARGS,
        'slow_mo': SLOW_MO,
        'default_timeout': DEFAULT_TIMEOUT,
        'navigation_timeout': NAVIGATION_TIMEOUT,
        'action_timeout': ACTION_TIMEOUT
    }

def get_browser_mode_description():
    """
    Get human-readable description of current browser mode.
    
    Returns:
        str: Description of browser mode
    """
    return "Headless (Background)" if HEADLESS_MODE else "Headed (Visible)"

def set_headless_mode(headless=True):
    """
    Programmatically set headless mode (for advanced usage).
    
    Args:
        headless (bool): True for headless, False for visible browser
    """
    global HEADLESS_MODE
    HEADLESS_MODE = headless

# Quick configuration presets
def set_development_mode():
    """Set browser for development (visible, slower)"""
    global HEADLESS_MODE, SLOW_MO
    HEADLESS_MODE = False
    SLOW_MO = 50

def set_production_mode():
    """Set browser for production (headless, fastest)"""
    global HEADLESS_MODE, SLOW_MO
    HEADLESS_MODE = False
    SLOW_MO = 0

def set_debug_mode():
    """Set browser for debugging (visible, very slow)"""
    global HEADLESS_MODE, SLOW_MO
    HEADLESS_MODE = False
    SLOW_MO = 500

# Display current configuration when imported
if __name__ == "__main__":
    print("🌐 Portaliano Browser Configuration")
    print("=" * 40)
    print(f"🖥️  Browser Mode: {get_browser_mode_description()}")
    print(f"⚡ Slow Motion: {SLOW_MO}ms")
    print(f"⏱️  Default Timeout: {DEFAULT_TIMEOUT/1000}s")
    print(f"🧭 Navigation Timeout: {NAVIGATION_TIMEOUT/1000}s")
    print(f"🎯 Action Timeout: {ACTION_TIMEOUT/1000}s")
    print(f"🔧 Browser Args: {len(BROWSER_ARGS)} optimizations")
    print("\n📝 To change configuration:")
    print("   Edit HEADLESS_MODE in browser_config.py")
    print("   - False = Browser visible")
    print("   - True  = Browser hidden")
else:
    # Show config when imported
    print(f"🖥️ Browser mode: {get_browser_mode_description()}")
