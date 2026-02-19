#!/bin/bash

# Automated GitHub Push Script for DATA Project
# This script handles GitHub authentication and repository push

set -e  # Exit on any error

echo "🚀 Automated GitHub Push for DATA Project"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -d "Beginner" ] || [ ! -d "Intermediate" ]; then
    print_error "Not in the DATA project directory. Please run this script from the DATA folder."
    exit 1
fi

print_status "Checking GitHub CLI authentication..."

# Check if GitHub CLI is authenticated
if ! gh auth status >/dev/null 2>&1; then
    print_warning "GitHub CLI is not authenticated."
    print_status "Starting GitHub authentication process..."

    # Try to authenticate with GitHub CLI
    if gh auth login --hostname github.com --git-protocol https; then
        print_success "GitHub CLI authentication successful!"
    else
        print_error "GitHub CLI authentication failed."
        print_status "Please try authenticating manually:"
        echo "  gh auth login"
        echo "  Or visit: https://github.com/login/device"
        exit 1
    fi
else
    print_success "GitHub CLI is already authenticated."
fi

# Verify the repository exists
print_status "Verifying repository access..."
if ! gh repo view kipruto45/Data-Enginerring-full-project >/dev/null 2>&1; then
    print_error "Cannot access repository kipruto45/Data-Enginerring-full-project"
    print_status "Please check:"
    echo "  1. Repository exists: https://github.com/kipruto45/Data-Enginerring-full-project"
    echo "  2. You have write access to the repository"
    exit 1
fi

print_success "Repository access confirmed."

# Check git status
print_status "Checking git repository status..."
if [ -n "$(git status --porcelain)" ]; then
    print_warning "Working directory has uncommitted changes."
    print_status "Committing current changes..."
    git add .
    git commit -m "Auto-commit: $(date)" || true
fi

# Set up git with GitHub CLI authentication
print_status "Configuring git for GitHub CLI..."
gh auth setup-git

# Push to GitHub
print_status "Pushing to GitHub repository..."
if git push origin main; then
    print_success "Repository successfully pushed to GitHub!"
    print_status "Repository URL: https://github.com/kipruto45/Data-Enginerring-full-project"
else
    print_error "Git push failed."
    print_status "Trying alternative push method..."

    # Try force push
    if git push -f origin main; then
        print_success "Repository pushed with force push."
    else
        print_error "All push attempts failed."
        print_status "Manual upload instructions:"
        echo "  1. ZIP file created at: $(pwd)/../DATA-project.zip"
        echo "  2. Go to: https://github.com/kipruto45/Data-Enginerring-full-project"
        echo "  3. Click 'Add file' → 'Upload files'"
        echo "  4. Upload the ZIP file"
        exit 1
    fi
fi

print_success "🎉 Project successfully deployed to GitHub!"
print_status "View your project at: https://github.com/kipruto45/Data-Enginerring-full-project"