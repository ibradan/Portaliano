#!/bin/bash
# Docker Build & Deploy Script for Portaliano
# ============================================

set -e  # Exit on any error

echo "🐳 Building Optimized Portaliano Docker Image"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Build image
echo -e "${BLUE}📦 Building Docker image...${NC}"
docker build -t portaliano:latest .

# Show image size
echo -e "${YELLOW}📊 Image size:${NC}"
docker images portaliano:latest --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Show what will be excluded (for verification)
echo -e "${YELLOW}🚫 Files excluded by .dockerignore:${NC}"
echo "   - venv/ directory (~136MB)"
echo "   - __pycache__/ directories"
echo "   - Documentation files (*.md)"
echo "   - Development scripts"
echo "   - Git directory"

# Compare with project size
echo -e "${YELLOW}📏 Size comparison:${NC}"
PROJECT_SIZE=$(du -sh . --exclude=venv | cut -f1)
VENV_SIZE=$(du -sh venv/ | cut -f1)
echo "   - Project (without venv): $PROJECT_SIZE"
echo "   - Virtual environment: $VENV_SIZE"
echo "   - Docker image: See above"

echo ""
echo -e "${GREEN}✅ Docker image built successfully!${NC}"
echo ""
echo -e "${BLUE}🚀 To run the container:${NC}"
echo "   docker-compose up -d"
echo ""
echo -e "${BLUE}🔍 To check running containers:${NC}"
echo "   docker-compose ps"
echo ""
echo -e "${BLUE}📋 To view logs:${NC}"
echo "   docker-compose logs -f portaliano"
echo ""
echo -e "${BLUE}🛑 To stop:${NC}"
echo "   docker-compose down"
