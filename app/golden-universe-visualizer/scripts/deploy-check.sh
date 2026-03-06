#!/bin/bash

# Pre-Deployment Checklist Script
# This script verifies all requirements are met before deployment

set -e

echo "🔍 Running pre-deployment checks..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

# Function to check for errors
check_error() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
        ((ERRORS++))
    fi
}

# Function to check for warnings
check_warning() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${YELLOW}⚠${NC} $1"
        ((WARNINGS++))
    fi
}

echo ""
echo "1️⃣  Checking environment..."

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -ge 20 ]; then
    echo -e "${GREEN}✓${NC} Node.js version ($NODE_VERSION.x) is compatible"
else
    echo -e "${RED}✗${NC} Node.js version must be 20.x or higher"
    ((ERRORS++))
fi

# Check if .env.production exists
if [ -f ".env.production" ]; then
    echo -e "${GREEN}✓${NC} Production environment file exists"
else
    echo -e "${YELLOW}⚠${NC} .env.production not found (optional)"
    ((WARNINGS++))
fi

# Check Git status
if [ -d ".git" ]; then
    if [ -z "$(git status --porcelain)" ]; then
        echo -e "${GREEN}✓${NC} Working directory is clean"
    else
        echo -e "${YELLOW}⚠${NC} Uncommitted changes detected"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠${NC} Not a git repository"
    ((WARNINGS++))
fi

echo ""
echo "2️⃣  Running code quality checks..."

# Run linter
npm run lint > /dev/null 2>&1
check_error "ESLint passes"

# Run type check
npm run type-check > /dev/null 2>&1
check_error "TypeScript type check passes"

# Check formatting
npm run format:check > /dev/null 2>&1
check_warning "Code formatting is correct"

echo ""
echo "3️⃣  Running tests..."

# Run tests
npm test > /dev/null 2>&1
check_error "All tests pass"

echo ""
echo "4️⃣  Checking dependencies..."

# Check for security vulnerabilities
npm audit --audit-level=high > /dev/null 2>&1
check_warning "No high/critical security vulnerabilities"

# Check for outdated packages
OUTDATED=$(npm outdated 2>&1 || true)
if [ -z "$OUTDATED" ]; then
    echo -e "${GREEN}✓${NC} All dependencies are up to date"
else
    echo -e "${YELLOW}⚠${NC} Some dependencies are outdated"
    ((WARNINGS++))
fi

echo ""
echo "5️⃣  Building application..."

# Try to build
npm run build > /dev/null 2>&1
check_error "Production build succeeds"

# Check build size
if [ -d "dist" ]; then
    BUILD_SIZE=$(du -sk dist | cut -f1)
    if [ $BUILD_SIZE -lt 5120 ]; then  # Less than 5MB
        echo -e "${GREEN}✓${NC} Build size is reasonable ($(du -sh dist | cut -f1))"
    else
        echo -e "${YELLOW}⚠${NC} Build size is large ($(du -sh dist | cut -f1))"
        ((WARNINGS++))
    fi
fi

echo ""
echo "6️⃣  Checking deployment files..."

# Check for required deployment files
DEPLOYMENT_FILES=(
    "vercel.json"
    "netlify.toml"
    "Dockerfile"
    ".dockerignore"
    "DEPLOYMENT.md"
)

for file in "${DEPLOYMENT_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file exists"
    else
        echo -e "${YELLOW}⚠${NC} $file not found"
        ((WARNINGS++))
    fi
done

echo ""
echo "7️⃣  Checking documentation..."

# Check if documentation exists
DOCS=(
    "README.md"
    "CONTRIBUTING.md"
    "CHANGELOG.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo -e "${GREEN}✓${NC} $doc exists"
    else
        echo -e "${YELLOW}⚠${NC} $doc not found"
        ((WARNINGS++))
    fi
done

# Summary
echo ""
echo "========================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment checks passed!${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠️  $WARNINGS warning(s) found${NC}"
        echo "Review warnings above before deploying"
    fi
    echo "Ready to deploy to production!"
    exit 0
else
    echo -e "${RED}❌ Deployment checks failed!${NC}"
    echo -e "${RED}$ERRORS error(s) found${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}$WARNINGS warning(s) found${NC}"
    fi
    echo "Fix errors above before deploying"
    exit 1
fi
