#!/bin/bash
# Storytelling Release Script - Simple & Direct

set -e

echo "📦 Release: storytelling"

# Install dev dependencies
echo "🔧 Installing dependencies..."
pip install -e ".[dev,test]"

# Run checks
echo "🔍 Running checks..."
make check
make build

# Upload to PyPI
echo "📤 Ready to publish to PyPI"
echo "   Run: twine upload dist/*"
echo ""
echo "   Or for test PyPI: twine upload --repository testpypi dist/*"
