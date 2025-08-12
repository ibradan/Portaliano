# 🎛️ Browser Configuration System

## ✨ New Feature: Centralized Browser Control

### 📁 Files Added
- **`browser_config.py`** - Central configuration file
- **`switch_browser_mode.sh`** - Quick mode switcher script

### 🔧 Files Modified
- **`static/ikh_automation.py`** - Now uses browser_config
- **`static/ikk_automation.py`** - Now uses browser_config
- **`README.md`** - Updated with new features

## 🚀 Usage

### Quick Mode Switching
```bash
# Development mode (browser visible)
./switch_browser_mode.sh visible

# Production mode (browser hidden)  
./switch_browser_mode.sh headless

# Check current status
./switch_browser_mode.sh
```

### Manual Configuration
Edit `browser_config.py`:
```python
HEADLESS_MODE = False  # True for headless, False for visible
```

## 🎯 Benefits

### 🎛️ Centralized Control
- ✅ One file controls all automation browser behavior
- ✅ No need to edit multiple automation scripts
- ✅ Consistent configuration across IKH and IKK

### ⚡ Quick Switching
- ✅ Switch modes with single command
- ✅ No manual file editing required
- ✅ Instant configuration changes

### 🔧 Advanced Options
- ✅ Configurable browser arguments
- ✅ Adjustable automation speed (slow_mo)
- ✅ Development/Production presets
- ✅ Programmatic configuration API

## 🌟 Configuration Options

### Browser Modes
| Mode | Description | Use Case |
|------|-------------|----------|
| `visible` | Browser window shown | Development, debugging |
| `headless` | Browser runs in background | Production, server |

### Speed Settings
```python
SLOW_MO = 0     # Fastest (production)
SLOW_MO = 50    # Normal (development)  
SLOW_MO = 500   # Slow (debugging)
```

### Presets Available
```python
set_development_mode()  # Visible + slower
set_production_mode()   # Headless + fastest
set_debug_mode()        # Visible + very slow
```

## 🔄 Migration from Old System

### Before (Manual per script)
```python
# ikh_automation.py
browser = playwright.chromium.launch(headless=False, ...)

# ikk_automation.py  
browser = playwright.chromium.launch(headless=False, ...)
```

### After (Centralized)
```python
# All scripts now use:
browser_config = get_browser_config()
browser = playwright.chromium.launch(**browser_config)
```

## 🎉 Result

**Now you can easily switch browser modes:**

- 📝 **Edit once**: Change `browser_config.py` 
- 🔄 **Apply everywhere**: All automation scripts use the same config
- ⚡ **Quick switch**: Use `./switch_browser_mode.sh visible/headless`
- 🎯 **No script modification**: Keep automation code clean

**Perfect for different environments:**
- 👨‍💻 **Development**: `./switch_browser_mode.sh visible` 
- 🚀 **Production**: `./switch_browser_mode.sh headless`
- 🔍 **Debugging**: Edit `SLOW_MO = 500` in config file

This makes Portaliano much more flexible and easier to manage! 🌟
