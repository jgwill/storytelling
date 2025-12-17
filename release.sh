#!/bin/bash
# Release: bump version, build & publish to PyPI

set -e

# Get current version
CURRENT=$(grep 'version = ' pyproject.toml | head -1 | sed 's/.*version = "\(.*\)".*/\1/')

# Bump patch version (0.2.2 -> 0.2.3)
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"
NEW_PATCH=$((PATCH + 1))
NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"

echo "🚀 Releasing storytelling"
echo "   $CURRENT → $NEW_VERSION"
echo ""

# Update version in pyproject.toml
sed -i "s/version = \"$CURRENT\"/version = \"$NEW_VERSION\"/" pyproject.toml

# Commit version bump
git add pyproject.toml
git commit -m "chore: bump version to $NEW_VERSION"

# Clean old builds and build
echo "📦 Building..."
make clean
python3 -m build

# Publish
echo ""
echo "📤 Publishing to PyPI..."
twine upload dist/*

# Tag release
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"

echo ""
echo "✅ Published v$NEW_VERSION"
echo "   Don't forget: git push && git push --tags"
