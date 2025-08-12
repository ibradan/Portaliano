#!/bin/bash
# Size Analysis Script for Portaliano Docker Optimization
# =======================================================

set -e

echo "📊 Portaliano Size Analysis for Docker Optimization"
echo "=================================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔍 Current Project Structure:${NC}"
echo "-----------------------------"

# Project size breakdown
echo -e "${YELLOW}📁 Project directory sizes:${NC}"
du -sh * 2>/dev/null | sort -hr

echo ""
echo -e "${YELLOW}🗂️ Virtual environment breakdown:${NC}"
if [ -d "venv" ]; then
    du -sh venv/* 2>/dev/null | sort -hr | head -10
else
    echo "   No venv directory found"
fi

echo ""
echo -e "${YELLOW}🧰 Playwright cache sizes:${NC}"
if [ -d "$HOME/.cache/ms-playwright" ]; then
    du -sh $HOME/.cache/ms-playwright/* 2>/dev/null
    echo "   Total Playwright cache: $(du -sh $HOME/.cache/ms-playwright 2>/dev/null | cut -f1)"
else
    echo "   No Playwright cache found"
fi

echo ""
echo -e "${YELLOW}📋 Docker optimization impact:${NC}"
echo "Files excluded by .dockerignore:"

# Calculate sizes that will be excluded
VENV_SIZE=$(du -sh venv 2>/dev/null | cut -f1 || echo "0")
CACHE_SIZE=$(du -sh __pycache__ 2>/dev/null | cut -f1 || echo "0") 
DOC_SIZE=$(find . -name "*.md" -exec du -ch {} + 2>/dev/null | tail -1 | cut -f1 || echo "0")

echo "   - Virtual environment (venv/): $VENV_SIZE"
echo "   - Python cache (__pycache__/): $CACHE_SIZE"
echo "   - Documentation files (*.md): $DOC_SIZE"
echo "   - Git directory (.git/): $(du -sh .git 2>/dev/null | cut -f1 || echo 'N/A')"

echo ""
echo -e "${YELLOW}🎯 Expected Docker image benefits:${NC}"
echo "   - No venv directory (dependencies installed via pip)"
echo "   - No development files (scripts, docs, cache)"
echo "   - Multi-stage build reduces final size"
echo "   - Only essential browser (Chromium) included"
echo "   - Optimized system dependencies"

echo ""
echo -e "${GREEN}💡 Optimization Summary:${NC}"
echo "   - Project size: $(du -sh . | cut -f1)"
echo "   - Essential files only: $(du -sh . --exclude=venv --exclude=.git --exclude=__pycache__ --exclude='*.md' | cut -f1)"
echo "   - Playwright browsers will be downloaded inside container"
echo "   - Multi-stage build will minimize final layer"

echo ""
echo -e "${BLUE}🚀 Ready to build optimized Docker image!${NC}"
echo "Run: ./docker-build.sh"
