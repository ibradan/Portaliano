#!/bin/bash
# Start Portal Flask App (all automation via web)

# Activate venv if exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Default port
PORT=${PORT:-5000}
export PORT
export FLASK_ENV=production
export PLAYWRIGHT_HEADLESS=true
export PYTHONUNBUFFERED=1

# Run Flask app
python app.py
