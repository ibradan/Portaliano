#!/bin/bash
# Portaliano launcher with Virtual Environment
echo "🚀 Starting Portaliano with Virtual Environment"
echo "=============================================="

# Change to script directory
cd "$(dirname "$0")"

# Check venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "💡 Run: ./setup_venv.sh first"
    exit 1
fi

# Activate venv
source venv/bin/activate

# Set environment variables
export PLAYWRIGHT_HEADLESS=true
export FLASK_ENV=development

echo "✅ Virtual environment activated"
echo "📁 Project: $(pwd)"
echo "🐍 Python: $(which python)"
echo "🌐 Starting Flask application..."
echo "   URL: http://localhost:5000"
echo "   Press Ctrl+C to stop"
echo "=============================================="

# Start application
python app.py
