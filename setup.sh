#!/bin/bash
# Atlas Coder Setup Script
# ===========================
# 
# Complete automated setup for Atlas Coder development environment.
# This script sets up a virtual environment, installs dependencies,
# configures direnv, and verifies the setup.
#
# Usage: ./setup.sh

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

echo "${GREEN}🚀 Starting Atlas Coder Setup...${NC}"

# 1. Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv || print_error "Failed to create virtual environment."
print_status "Virtual environment created."

# 2. Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate || print_error "Failed to activate virtual environment."
print_status "Virtual environment activated."

# 3. Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1 || print_warning "Failed to upgrade pip, continuing anyway."
print_status "Pip upgraded."

# 4. Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt || print_error "Failed to install main dependencies."
print_status "Main dependencies installed."

# Install development dependencies if requirements-dev.txt exists
if [ -f "requirements-dev.txt" ]; then
    echo "Installing development dependencies from requirements-dev.txt..."
    pip install -r requirements-dev.txt || print_warning "Failed to install development dependencies, continuing anyway."
    print_status "Development dependencies installed."
fi

# 5. Configure direnv (if available)
echo "Configuring direnv..."
if command -v direnv &> /dev/null; then
    echo 'source .venv/bin/activate' > .envrc
    echo 'export PYTHONPATH="${PWD}:${PYTHONPATH}"' >> .envrc
    direnv allow . || print_warning "Failed to allow direnv, manual activation may be needed."
    print_status "direnv configured."
else
    print_warning "direnv not found. Please install it for automatic environment loading, or activate manually with 'source .venv/bin/activate'."
fi

# 6. Verify setup with atlas-coder status
echo "Verifying setup with 'atlas-coder status'..."
# Ensure the CLI is executable within the venv
if ! python -m atlas_coder status; then
    print_error "'atlas-coder status' command failed. Setup may not be complete."
fi
print_status "'atlas-coder status' verification successful."

echo "${GREEN}🎉 Atlas Coder Setup Complete!${NC}"
echo "To activate your environment, run: ${YELLOW}source .venv/bin/activate${NC}"
if ! command -v direnv &> /dev/null; then
    echo "Remember to set your OPENROUTER_API_KEY in a .env file: ${YELLOW}echo \"OPENROUTER_API_KEY=your_key_here\" > .env${NC}"
fi
