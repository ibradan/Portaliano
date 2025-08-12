#!/usr/bin/env python3
"""
Browser Configuration for Portaliano Automation
================================================

Central place to control browser behavior for all automation scripts.

Usage (static edit):
- HEADLESS_MODE = False  -> Browser window visible (development/debugging)
- HEADLESS_MODE = True   -> Browser runs in background (production/server)

Environment overrides (preferred for Docker / deployment):
- Set HEADLESS_MODE=true|false|1|0|yes|no|on|off
- Set SLOW_MO=<milliseconds delay> (e.g. 0 / 50 / 200)

Precedence:
1. Environment variables (if provided)
2. Values defined in this file

Example:
    HEADLESS_MODE=true SLOW_MO=0 python3 app.py

This keeps local dev simple (edit file) while making container/runtime configurable.
"""

from os import getenv

# Base (fallback) browser configuration
HEADLESS_MODE = True  # Default: headless. Override via env HEADLESS_MODE

# Browser Arguments (for optimization)
BROWSER_ARGS = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-features=VizDisplayCompositor',
    '--disable-web-security'
]

# Browser Speed (milliseconds delay between actions)
SLOW_MO = 0  # Fallback default. Can be overridden by env SLOW_MO

# --- Environment Overrides -------------------------------------------------
_env_headless = getenv("HEADLESS_MODE")
if _env_headless is not None:
    _val = _env_headless.strip().lower()
    if _val in ("1", "true", "yes", "on"):  # truthy
        HEADLESS_MODE = True
    elif _val in ("0", "false", "no", "off"):  # falsy
        HEADLESS_MODE = False

_env_slow_mo = getenv("SLOW_MO")
if _env_slow_mo and _env_slow_mo.isdigit():
    try:
        SLOW_MO = max(0, int(_env_slow_mo))
    except ValueError:
        pass  # ignore invalid value, keep fallback

def get_browser_config():
    """
    Get browser configuration for automation scripts.
    
    Returns:
        dict: Browser configuration with headless mode, args, and slow_mo
    """
    return {
        'headless': HEADLESS_MODE,
        'args': BROWSER_ARGS,
        'slow_mo': SLOW_MO
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
    HEADLESS_MODE = True
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
    print(f"🔧 Browser Args: {len(BROWSER_ARGS)} optimizations")
    print("\n📝 Configuration precedence:")
    print("   1. Environment variables (HEADLESS_MODE, SLOW_MO)")
    print("   2. Values in browser_config.py")
    print("\n🔄 Override examples:")
    print("   HEADLESS_MODE=false python3 app.py  # show browser")
    print("   HEADLESS_MODE=true SLOW_MO=50 python3 app.py")
    print("\n🐳 Docker Compose:")
    print("   environment:")
    print("     - HEADLESS_MODE=true")
    print("     - SLOW_MO=0")
else:
    # Show concise config when imported
    print(f"🖥️ Browser mode: {get_browser_mode_description()}")
