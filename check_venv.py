#!/usr/bin/env python3
"""Check virtual environment setup"""
import sys
import os

def check_venv():
    print("🔍 Virtual Environment Check")
    print("=" * 40)
    
    # Check if in venv
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    print(f"🐍 Python executable: {sys.executable}")
    print(f"📁 Python prefix: {sys.prefix}")
    print(f"🏠 Working directory: {os.getcwd()}")
    print(f"🔗 In virtual env: {'✅ YES' if in_venv else '❌ NO'}")
    
    if in_venv:
        print("✅ Virtual environment is active!")
    else:
        print("⚠️ Not in virtual environment")
        print("💡 Run: source venv/bin/activate")
    
    print("\n📦 Checking packages...")
    try:
        import flask
        print(f"✅ Flask: {flask.__version__}")
    except ImportError:
        print("❌ Flask not installed")
    
    try:
        import playwright
        print("✅ Playwright: Available")
    except ImportError:
        print("❌ Playwright not installed")
    
    return in_venv

if __name__ == "__main__":
    check_venv()
