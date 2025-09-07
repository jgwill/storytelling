# Storytelling

A Python package for storytelling applications.

## Features

- Create and manage story objects
- Add content and metadata to stories
- Command-line interface for story management
- Professional package structure with development tools

## Installation

### From Source

```bash
git clone https://github.com/jgwill/storytelling.git
cd storytelling
pip install -e .
```

### For Development

```bash
git clone https://github.com/jgwill/storytelling.git
cd storytelling
./scripts/init.sh
```

This will set up a virtual environment and install all development dependencies.

## Usage

### Python API

```python
from storytelling import Story

# Create a new story
story = Story("My Adventure", "Once upon a time...")

# Add more content
story.add_content("The hero embarked on a journey.")

# Add metadata
story.set_metadata("author", "Your Name")
story.set_metadata("genre", "Adventure")

# Access story information
print(story.title)  # "My Adventure"
print(story.content)  # Full story content
print(story.get_metadata("author"))  # "Your Name"
```

### Command Line Interface

```bash
# Create a new story
storytelling create "My Story Title" --content "Story content here" --author "Author Name"

# Show help
storytelling --help
```

## Development

This project uses modern Python packaging and development practices.

### Quick Start

```bash
# Initialize development environment
./scripts/init.sh

# Run tests
make test

# Check code quality
make lint

# Format code
make format

# Build package
make build

# See all available commands
make help
```

### Development Commands

The project includes a comprehensive Makefile with the following commands:

- `make init` - Initialize development environment
- `make test` - Run tests
- `make test-cov` - Run tests with coverage
- `make lint` - Run linting checks
- `make format` - Format code
- `make build` - Build package
- `make clean` - Clean build artifacts
- `make release-check` - Run all pre-release checks
- `make docs` - Build documentation

### Project Structure

```
storytelling/
├── storytelling/           # Main package
│   ├── __init__.py        # Package initialization
│   ├── core.py            # Core functionality
│   └── cli.py             # Command line interface
├── tests/                 # Test files
├── scripts/               # Development scripts
│   ├── init.sh           # Environment initialization
│   └── release.sh        # Release automation
├── docs/                  # Documentation
├── pyproject.toml         # Package configuration
├── Makefile              # Development commands
└── README.md             # This file
```

### Code Quality

The project uses several tools to maintain code quality:

- **Black** - Code formatting
- **Ruff** - Linting and import sorting
- **MyPy** - Type checking
- **Pytest** - Testing framework
- **Pre-commit** - Git hooks for code quality

### Release Process

To create a new release:

```bash
# Run release script
./scripts/release.sh release patch  # or minor, major
./scripts/release.sh release 1.2.3  # specific version

# Or use make commands
make release-check  # Run all checks
make release-test   # Upload to test PyPI
make release        # Upload to production PyPI
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting: `make test lint`
5. Submit a pull request

## License

This project is licensed under the CC0-1.0 License - see the [LICENSE](LICENSE) file for details.

## Requirements

- Python 3.8+
- See `pyproject.toml` for detailed dependencies