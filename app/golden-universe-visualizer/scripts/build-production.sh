#!/bin/bash

# Production Build Script for Golden Universe Visualizer
# This script builds the application for production deployment

set -e  # Exit on error

echo "🚀 Starting production build..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 20.x or higher.${NC}"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 20 ]; then
    echo -e "${RED}❌ Node.js version must be 20.x or higher. Current version: $(node -v)${NC}"
    exit 1
fi

echo -e "${BLUE}📦 Node.js version: $(node -v)${NC}"

# Clean previous builds
echo -e "${BLUE}🧹 Cleaning previous builds...${NC}"
rm -rf dist
rm -rf node_modules/.vite

# Install dependencies
echo -e "${BLUE}📥 Installing dependencies...${NC}"
npm ci --prefer-offline --no-audit

# Run linter
echo -e "${BLUE}🔍 Running linter...${NC}"
npm run lint

# Run type check
echo -e "${BLUE}📝 Running type check...${NC}"
npm run type-check

# Run tests
echo -e "${BLUE}🧪 Running tests...${NC}"
npm test

# Build the application
echo -e "${BLUE}🏗️  Building application...${NC}"
NODE_ENV=production npm run build

# Check if build succeeded
if [ ! -d "dist" ]; then
    echo -e "${RED}❌ Build failed! dist directory not found.${NC}"
    exit 1
fi

# Get build size
BUILD_SIZE=$(du -sh dist | cut -f1)
echo -e "${GREEN}✅ Build completed successfully!${NC}"
echo -e "${GREEN}📊 Build size: $BUILD_SIZE${NC}"

# Generate build report
echo -e "${BLUE}📋 Build summary:${NC}"
echo "  - Output directory: dist/"
echo "  - Build size: $BUILD_SIZE"
echo "  - Timestamp: $(date)"
echo "  - Git commit: $(git rev-parse --short HEAD 2>/dev/null || echo 'N/A')"
echo "  - Git branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'N/A')"

# Check for bundle stats
if [ -f "dist/stats.html" ]; then
    echo -e "${BLUE}📈 Bundle analyzer report: dist/stats.html${NC}"
fi

# Verify critical files exist
echo -e "${BLUE}🔎 Verifying build artifacts...${NC}"
CRITICAL_FILES=("dist/index.html" "dist/assets")
for file in "${CRITICAL_FILES[@]}"; do
    if [ ! -e "$file" ]; then
        echo -e "${RED}❌ Critical file missing: $file${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ All critical files present${NC}"

# Show next steps
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✨ Production build complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Test the build locally: npm run preview"
echo "  2. Deploy to Vercel: npm run deploy:vercel"
echo "  3. Deploy to Netlify: npm run deploy:netlify"
echo "  4. Or deploy with Docker: docker build -t golden-universe ."
echo ""
echo "For detailed deployment instructions, see DEPLOYMENT.md"
