#!/bin/bash

# Golden Universe Backend Test Script
# This script tests the backend API endpoints

echo "==========================================="
echo "Golden Universe Backend Test"
echo "==========================================="
echo ""

API_URL="http://localhost:3001/api"
TIMEOUT=5

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local expected_status=${3:-200}
    local data=$4

    echo -n "Testing ${method} ${endpoint}... "

    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" -m $TIMEOUT "${API_URL}${endpoint}")
    elif [ "$method" = "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -d "$data" -m $TIMEOUT "${API_URL}${endpoint}")
    fi

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)

    if [ "$http_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $http_code)"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Expected $expected_status, got $http_code)"
        return 1
    fi
}

# Check if server is running
echo "Checking if server is running..."
if ! curl -s -m 2 "http://localhost:3001/api" > /dev/null 2>&1; then
    echo -e "${RED}Error: Server is not running on port 3001${NC}"
    echo "Please start the server with: npm run server:dev"
    exit 1
fi

echo -e "${GREEN}Server is running!${NC}"
echo ""

# Test root endpoint
echo "API Endpoints:"
echo "=============="
test_endpoint "GET" "/"

# Test health endpoints
echo ""
echo "Health Endpoints:"
echo "================="
test_endpoint "GET" "/health"
test_endpoint "GET" "/health/metrics"

# Test theories endpoints
echo ""
echo "Theory Endpoints:"
echo "================="
test_endpoint "GET" "/theories"
test_endpoint "GET" "/theories/stats"

# Test derivations endpoints
echo ""
echo "Derivation Endpoints:"
echo "===================="
test_endpoint "GET" "/derivations"
test_endpoint "GET" "/derivations/stats"
test_endpoint "GET" "/derivations/1" 404  # May not exist yet

# Test equations endpoints
echo ""
echo "Equation Endpoints:"
echo "=================="
test_endpoint "GET" "/equations"
test_endpoint "GET" "/equations/categories"

# Test calculations endpoints
echo ""
echo "Calculation Endpoints:"
echo "====================="
test_endpoint "GET" "/calculations"
test_endpoint "GET" "/calculations/results"

# Test search endpoint
echo ""
echo "Search Endpoints:"
echo "================"
test_endpoint "GET" "/search?q=test" 200

echo ""
echo "==========================================="
echo "Test Complete!"
echo "==========================================="
echo ""
echo "To view full API documentation, visit:"
echo "  http://localhost:3001/api-docs"
echo ""
