#!/bin/bash
# Start IKK automation only (not Flask)
export PLAYWRIGHT_HEADLESS=true
python ikk_automation.py "$@"
