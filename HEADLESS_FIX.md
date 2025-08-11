# Headless Browser Fix Summary

## Issue
The IKK automation was failing in Docker because Playwright was trying to launch a browser in headed mode (`headless=False`) but there was no display server available, resulting in the error:
```
Target page, context or browser has been closed
Browser logs:
Looks like you launched a headed browser without having a XServer running.
Set either 'headless: true' or use 'xvfb-run <your-playwright-app>' before running Playwright.
```

## Root Cause
- `ikk_automation.py` was hardcoded to use `headless=False`
- Docker containers don't have display servers by default
- Missing environment variable configuration for headless mode

## Changes Made

### 1. Updated `static/ikk_automation.py`
- Added `import os` to check environment variables
- Modified browser launch to respect `PLAYWRIGHT_HEADLESS` environment variable
- Default behavior is now headless mode (`true`) for Docker compatibility
- Added informative logging about browser mode

### 2. Updated `docker-compose.yml`
- Added `PLAYWRIGHT_HEADLESS=true` environment variable
- Ensures all automation runs in headless mode in Docker

### 3. Updated startup scripts
- `start_ikk.sh`: Added `export PLAYWRIGHT_HEADLESS=true`
- `start_portal.sh`: Added `export PLAYWRIGHT_HEADLESS=true`

### 4. Updated `app.py`
- Modified `run_automation_process()` to pass `PLAYWRIGHT_HEADLESS` to subprocess environment
- Ensures Flask-triggered automation also runs in headless mode

## Testing
Created `test_headless.py` to verify the browser configuration works correctly.

## Result
- IKK automation now runs in headless mode by default in Docker
- Can still run in headed mode locally by setting `PLAYWRIGHT_HEADLESS=false`
- Consistent behavior across all automation scripts
- IKH automation was already correctly configured

## Environment Variables
- `PLAYWRIGHT_HEADLESS=true` (default): Run in headless mode
- `PLAYWRIGHT_HEADLESS=false`: Run in headed mode (requires display server)

The automation should now work correctly in Docker environments without the display server error.
