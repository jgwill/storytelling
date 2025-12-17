#!/bin/bash
# Storytelling Release Script
# Prepares distribution and publishes to PyPI

set -e  # Exit on any error

echo "🚀 Storytelling Release Script Starting..."

# Conda environment activation
echo "🔬 Finding and activating storytelling conda environment..."
__conda_setup="$('/usr/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/usr/etc/profile.d/conda.sh" ]; then
        . "/usr/etc/profile.d/conda.sh"
    else
        export PATH="/usr/bin:$PATH"
    fi
fi
unset __conda_setup

conda activate storytelling || { echo "Error: Conda environment 'storytelling' not found or failed to activate. Please create it or adjust the script."; exit 1; }


# Clean previous builds
echo "🧹 Cleaning previous builds..."
make clean

# Bump version (patch increment)
echo "📈 Bumping patch version in pyproject.toml..."
# Get current version
CURRENT_VERSION=$(grep -E "^\s*version\s*=\s*[\"']" pyproject.toml | sed -E "s/.*[\"']([^\"']+)[\"'].*/\1/")
echo "Current version: ${CURRENT_VERSION}"

# Split version into parts
MAJOR=$(echo "${CURRENT_VERSION}" | cut -d. -f1)
MINOR=$(echo "${CURRENT_VERSION}" | cut -d. -f2)
PATCH=$(echo "${CURRENT_VERSION}" | cut -d. -f3)

# Increment patch version
NEW_PATCH=$((PATCH + 1))
NEW_VERSION="${MAJOR}.${MINOR}.${NEW_PATCH}"
echo "New version: ${NEW_VERSION}"

# Update pyproject.toml
sed -i "s/^version = \"${CURRENT_VERSION}\"/version = \"${NEW_VERSION}\"/" pyproject.toml

# Build distribution
echo "🔨 Building distribution..."
make build

# Upload to PyPI
echo "📦 Publishing to PyPI..."
make release

# Get the new version for tagging (already available in NEW_VERSION)
echo "🏷️ Creating git tag..."
git add pyproject.toml
git commit -m "v${NEW_VERSION}" || echo "No changes to commit"
git tag "v${NEW_VERSION}"

echo "✅ Release complete!"
echo "📋 Version: v${NEW_VERSION}"
echo "📋 Next steps:"
echo "   - Push changes: git push origin main"
echo "   - Push tag: git push origin v${NEW_VERSION}"
echo "   - Verify package on PyPI: https://pypi.org/project/storytelling/"
echo "   - Test installation: pip install storytelling"
