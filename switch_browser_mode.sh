#!/bin/bash
# Quick Browser Mode Switcher for Portaliano

BROWSER_CONFIG_FILE="browser_config.py"

show_current_mode() {
    echo "🌐 Current Browser Configuration:"
    echo "================================="
    python3 browser_config.py
}

set_visible_mode() {
    echo "🔄 Setting browser to VISIBLE mode..."
    sed -i 's/HEADLESS_MODE = True/HEADLESS_MODE = False/g' "$BROWSER_CONFIG_FILE"
    sed -i 's/HEADLESS_MODE = [Tt]rue/HEADLESS_MODE = False/g' "$BROWSER_CONFIG_FILE"
    echo "✅ Browser will now be VISIBLE during automation"
    show_current_mode
}

set_headless_mode() {
    echo "🔄 Setting browser to HEADLESS mode..."
    sed -i 's/HEADLESS_MODE = False/HEADLESS_MODE = True/g' "$BROWSER_CONFIG_FILE"
    sed -i 's/HEADLESS_MODE = [Ff]alse/HEADLESS_MODE = True/g' "$BROWSER_CONFIG_FILE"
    echo "✅ Browser will now run in BACKGROUND (headless)"
    show_current_mode
}

case "$1" in
    "visible"|"show"|"dev"|"development")
        set_visible_mode
        ;;
    "headless"|"hide"|"prod"|"production")
        set_headless_mode
        ;;
    "status"|"current"|"")
        show_current_mode
        ;;
    *)
        echo "🚀 Portaliano Browser Mode Switcher"
        echo "====================================="
        echo ""
        echo "Usage: $0 [mode]"
        echo ""
        echo "Modes:"
        echo "  visible   - Show browser window (for development/debugging)"
        echo "  headless  - Hide browser window (for production/server)"
        echo "  status    - Show current configuration"
        echo ""
        echo "Aliases:"
        echo "  visible: show, dev, development"
        echo "  headless: hide, prod, production"
        echo "  status: current, (no argument)"
        echo ""
        echo "Examples:"
        echo "  $0 visible    # Enable visible browser"
        echo "  $0 headless   # Enable headless browser"
        echo "  $0            # Show current status"
        ;;
esac
