#!/bin/bash
# Release: build & publish to PyPI

set -e

VERSION=$(grep 'version = ' pyproject.toml | head -1 | sed 's/.*version = "\(.*\)".*/\1/')

echo "🚀 Releasing storytelling v$VERSION"
echo ""

# Build
echo "📦 Building..."
python3 -m build

# Publish
echo ""
echo "📤 Publishing to PyPI..."
twine upload dist/*

echo ""
echo "✅ Published v$VERSION"
