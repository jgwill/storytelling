#!/bin/bash
# Release: bump version, build & publish storytelling-mcp to PyPI

set -e

# Ensure we're in the mcp directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Get current version from pyproject.toml in parent (storytelling package)
# For storytelling-mcp, we'll manage version independently here
VERSION_FILE="pyproject.toml"
if [ ! -f "$VERSION_FILE" ]; then
    echo "❌ Error: $VERSION_FILE not found in $SCRIPT_DIR"
    exit 1
fi

CURRENT=$(grep 'version = ' "$VERSION_FILE" 2>/dev/null | head -1 | sed 's/.*version = "\(.*\)".*/\1/' || echo "0.1.0")

# Parse version
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"
NEW_PATCH=$((PATCH + 1))
NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"

echo "🚀 Releasing storytelling-mcp"
echo "   Current: $CURRENT"
echo "   New:     $NEW_VERSION"
echo ""

# Check if pyproject.toml exists in mcp directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: mcp/pyproject.toml not found"
    echo "   storytelling-mcp must have its own pyproject.toml for PyPI distribution"
    exit 1
fi

# Update version in mcp pyproject.toml
echo "📝 Updating version in mcp/pyproject.toml..."
sed -i "s/version = \"$CURRENT\"/version = \"$NEW_VERSION\"/" pyproject.toml

# Update version in __init__.py if it exists
if [ -f "__init__.py" ]; then
    if grep -q "__version__" __init__.py; then
        sed -i "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" __init__.py
        echo "📝 Updated __init__.py"
    fi
fi

# Build the MCP package
echo "📦 Building storytelling-mcp package..."
python3 -m build

# Publish to PyPI
echo ""
echo "📤 Publishing storytelling-mcp to PyPI..."
twine upload dist/*

# Tag release (from parent directory)
cd ..
git add mcp/pyproject.toml mcp/__init__.py 2>/dev/null || true
git add mcp/pyproject.toml 2>/dev/null || true
git commit -m "chore(mcp): bump version to $NEW_VERSION"

git tag -a "mcp-v$NEW_VERSION" -m "Release storytelling-mcp v$NEW_VERSION"

echo ""
echo "✅ Published storytelling-mcp v$NEW_VERSION"
echo "   Don't forget: git push && git push --tags"
