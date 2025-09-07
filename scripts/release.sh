#!/bin/bash
# Release automation script for storytelling package

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

# Function to get current version from package
get_current_version() {
    python3 -c "import storytelling; print(storytelling.__version__)"
}

# Function to update version in files
update_version() {
    local new_version=$1
    
    # Update pyproject.toml
    sed -i "s/version = \".*\"/version = \"$new_version\"/" pyproject.toml
    
    # Update __init__.py
    sed -i "s/__version__ = \".*\"/__version__ = \"$new_version\"/" storytelling/__init__.py
    
    print_success "Updated version to $new_version"
}

# Function to validate version format
validate_version() {
    local version=$1
    if [[ ! $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        print_error "Invalid version format. Use semantic versioning (e.g., 1.0.0)"
        return 1
    fi
    return 0
}

# Main release function
release() {
    local release_type=$1
    local custom_version=$2
    
    print_status "Starting release process..."
    
    # Check if we're in the right directory
    if [ ! -f "pyproject.toml" ]; then
        print_error "pyproject.toml not found. Are you in the correct directory?"
        exit 1
    fi
    
    # Check if git is clean
    if ! git diff-index --quiet HEAD --; then
        print_error "Git working directory is not clean. Please commit or stash changes."
        exit 1
    fi
    
    # Get current version
    current_version=$(get_current_version)
    print_status "Current version: $current_version"
    
    # Determine new version
    if [ -n "$custom_version" ]; then
        new_version=$custom_version
        if ! validate_version "$new_version"; then
            exit 1
        fi
    else
        case $release_type in
            major)
                new_version=$(python3 -c "
import storytelling
parts = storytelling.__version__.split('.')
print(f'{int(parts[0])+1}.0.0')
")
                ;;
            minor)
                new_version=$(python3 -c "
import storytelling
parts = storytelling.__version__.split('.')
print(f'{parts[0]}.{int(parts[1])+1}.0')
")
                ;;
            patch)
                new_version=$(python3 -c "
import storytelling
parts = storytelling.__version__.split('.')
print(f'{parts[0]}.{parts[1]}.{int(parts[2])+1}')
")
                ;;
            *)
                print_error "Invalid release type. Use: major, minor, patch, or provide custom version"
                exit 1
                ;;
        esac
    fi
    
    print_status "New version: $new_version"
    
    # Confirm release
    read -p "Continue with release $new_version? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Release cancelled"
        exit 0
    fi
    
    # Run all checks
    print_status "Running pre-release checks..."
    
    # Lint and type check
    print_status "Running linting and type checks..."
    if ! make ci-lint; then
        print_error "Linting failed. Fix issues before release."
        exit 1
    fi
    
    # Run tests
    print_status "Running tests..."
    if ! make ci-test; then
        print_error "Tests failed. Fix issues before release."
        exit 1
    fi
    
    # Update version
    print_status "Updating version..."
    update_version "$new_version"
    
    # Build package
    print_status "Building package..."
    if ! make build; then
        print_error "Build failed."
        exit 1
    fi
    
    # Check build
    print_status "Checking build artifacts..."
    if ! make check-build; then
        print_error "Build check failed."
        exit 1
    fi
    
    # Create git commit and tag
    print_status "Creating git commit and tag..."
    git add pyproject.toml storytelling/__init__.py
    git commit -m "Release v$new_version"
    git tag -a "v$new_version" -m "Release v$new_version"
    
    print_success "Release preparation complete!"
    print_status "To complete the release:"
    echo "  1. Push changes: git push && git push --tags"
    echo "  2. Upload to PyPI: make release"
    echo "  3. Or upload to test PyPI first: make release-test"
    
    # Ask if user wants to push automatically
    read -p "Push to git now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Pushing to git..."
        git push
        git push --tags
        print_success "Pushed to git successfully!"
        
        # Ask about PyPI upload
        read -p "Upload to test PyPI? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Uploading to test PyPI..."
            if make release-test; then
                print_success "Upload to test PyPI successful!"
                
                read -p "Upload to production PyPI? (y/N): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    print_status "Uploading to production PyPI..."
                    make release
                    print_success "Release v$new_version complete!"
                fi
            else
                print_error "Upload to test PyPI failed."
            fi
        fi
    fi
}

# Show usage
usage() {
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  release <type>     Release with automatic version bump (major|minor|patch)"
    echo "  release <version>  Release with specific version (e.g., 1.2.3)"
    echo "  check              Run all pre-release checks"
    echo "  build              Build package"
    echo "  upload-test        Upload to test PyPI"
    echo "  upload             Upload to production PyPI"
    echo "  help               Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 release patch      # Bump patch version (0.1.0 -> 0.1.1)"
    echo "  $0 release minor      # Bump minor version (0.1.1 -> 0.2.0)"
    echo "  $0 release major      # Bump major version (0.2.0 -> 1.0.0)"
    echo "  $0 release 1.5.0      # Release specific version"
}

# Main script
case "${1:-help}" in
    release)
        if [ -z "$2" ]; then
            print_error "Please specify release type or version"
            usage
            exit 1
        fi
        release "$2" "$3"
        ;;
    check)
        print_status "Running pre-release checks..."
        make ci-lint && make ci-test
        print_success "All checks passed!"
        ;;
    build)
        print_status "Building package..."
        make build
        ;;
    upload-test)
        print_status "Uploading to test PyPI..."
        make release-test
        ;;
    upload)
        print_status "Uploading to production PyPI..."
        make release
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        print_error "Unknown command: $1"
        usage
        exit 1
        ;;
esac