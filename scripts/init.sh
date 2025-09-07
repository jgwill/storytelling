#!/bin/bash
# Development environment initialization script for storytelling package

set -e  # Exit on any error

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get Python version
get_python_version() {
    python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
}

print_status "Initializing development environment for storytelling package..."

# Check Python version
PYTHON_VERSION=$(get_python_version)
REQUIRED_VERSION="3.8"

if ! command_exists python3; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

print_status "Found Python $PYTHON_VERSION"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    print_error "pyproject.toml not found. Are you in the correct directory?"
    exit 1
fi

# Check if virtual environment should be created
CREATE_VENV=${1:-"yes"}

if [ "$CREATE_VENV" = "yes" ] && [ ! -d ".venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv .venv
    print_success "Virtual environment created in .venv/"
    
    print_status "To activate the virtual environment, run:"
    echo "  source .venv/bin/activate"
    echo ""
fi

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    print_status "Activating virtual environment..."
    source .venv/bin/activate
    print_success "Virtual environment activated"
fi

# Upgrade pip, setuptools, and wheel
print_status "Upgrading pip, setuptools, and wheel..."
python3 -m pip install --upgrade pip setuptools wheel

# Install the package in development mode with all dependencies
print_status "Installing package in development mode with dependencies..."
pip install -e ".[dev,test,docs]"

# Initialize pre-commit hooks if pre-commit is available
if command_exists pre-commit; then
    print_status "Installing pre-commit hooks..."
    pre-commit install
    print_success "Pre-commit hooks installed"
else
    print_warning "pre-commit not found. Install it with 'pip install pre-commit' to enable git hooks."
fi

# Create basic directories
print_status "Creating project structure..."
mkdir -p tests docs

# Create basic test file if it doesn't exist
if [ ! -f "tests/test_core.py" ]; then
    print_status "Creating basic test file..."
    cat > tests/test_core.py << 'EOF'
"""Tests for storytelling.core module."""

import pytest
from storytelling.core import Story


def test_story_creation():
    """Test basic story creation."""
    story = Story("Test Title", "Test content")
    assert story.title == "Test Title"
    assert story.content == "Test content"
    assert story.metadata == {}


def test_story_add_content():
    """Test adding content to story."""
    story = Story("Test Title")
    story.add_content("First paragraph")
    assert story.content == "First paragraph"
    
    story.add_content("Second paragraph")
    assert story.content == "First paragraph\n\nSecond paragraph"


def test_story_metadata():
    """Test story metadata functionality."""
    story = Story("Test Title")
    story.set_metadata("author", "Test Author")
    story.set_metadata("genre", "Fiction")
    
    assert story.get_metadata("author") == "Test Author"
    assert story.get_metadata("genre") == "Fiction"
    assert story.get_metadata("nonexistent") is None


def test_story_string_representation():
    """Test story string representations."""
    story = Story("Test Title", "Some content")
    assert str(story) == "Story: Test Title"
    assert repr(story) == "Story(title='Test Title', content_length=12)"
EOF
    print_success "Created tests/test_core.py"
fi

# Create __init__.py for tests
if [ ! -f "tests/__init__.py" ]; then
    touch "tests/__init__.py"
    print_success "Created tests/__init__.py"
fi

# Run initial tests to make sure everything works
print_status "Running initial tests..."
if python3 -m pytest tests/ -v; then
    print_success "All tests passed!"
else
    print_warning "Some tests failed. This is normal for a new project."
fi

# Show status
print_status "Running project status check..."
python3 -c "
import storytelling
print(f'Package version: {storytelling.__version__}')
print(f'Package location: {storytelling.__file__}')
"

print_success "Development environment initialization complete!"
print_status "Next steps:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Run tests: make test"
echo "  3. Check code quality: make lint"
echo "  4. Build package: make build"
echo "  5. See all available commands: make help"
echo ""
print_status "Happy coding!"