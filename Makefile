# Makefile for storytelling package

# Variables
PYTHON := python3
PIP := pip
PACKAGE_NAME := storytelling
SRC_DIR := storytelling
TESTS_DIR := tests
DOCS_DIR := docs

# Default target
.PHONY: help
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development setup
.PHONY: init
init: ## Initialize development environment
	@echo "Initializing development environment..."
	$(PYTHON) -m pip install --upgrade pip setuptools wheel
	$(PIP) install -e ".[dev,test,docs]"
	pre-commit install

.PHONY: install
install: ## Install package in development mode
	$(PIP) install -e .

.PHONY: install-dev
install-dev: ## Install package with development dependencies
	$(PIP) install -e ".[dev,test,docs]"

# Code quality
.PHONY: format
format: ## Format code with black and ruff
	black $(SRC_DIR) $(TESTS_DIR)
	ruff check --fix $(SRC_DIR) $(TESTS_DIR)

.PHONY: lint
lint: ## Run linting checks
	black --check $(SRC_DIR) $(TESTS_DIR)
	ruff check $(SRC_DIR) $(TESTS_DIR)
	mypy $(SRC_DIR)

.PHONY: type-check
type-check: ## Run type checking with mypy
	mypy $(SRC_DIR)

# Testing
.PHONY: test
test: ## Run tests
	PYTHONPATH=$(PWD) pytest $(TESTS_DIR)

.PHONY: test-cov
test-cov: ## Run tests with coverage
	pytest --cov=$(SRC_DIR) --cov-report=html --cov-report=term-missing $(TESTS_DIR)

.PHONY: test-fast
test-fast: ## Run tests excluding slow tests
	pytest -m "not slow" $(TESTS_DIR)

# Building and packaging
.PHONY: build
build: clean ## Build package
	$(PYTHON) -m build

.PHONY: check-build
check-build: build ## Check build artifacts
	twine check dist/*

# Documentation
.PHONY: docs
docs: ## Build documentation
	@if [ -d "$(DOCS_DIR)" ]; then \
		cd $(DOCS_DIR) && make html; \
	else \
		echo "Documentation directory not found. Run 'make docs-init' first."; \
	fi

.PHONY: docs-init
docs-init: ## Initialize documentation structure
	mkdir -p $(DOCS_DIR)
	@echo "Documentation structure created. You can now add Sphinx configuration."

.PHONY: docs-serve
docs-serve: docs ## Serve documentation locally
	@if [ -d "$(DOCS_DIR)/_build/html" ]; then \
		cd $(DOCS_DIR)/_build/html && $(PYTHON) -m http.server 8000; \
	else \
		echo "Documentation not built. Run 'make docs' first."; \
	fi

# Cleaning
.PHONY: clean
clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

.PHONY: clean-all
clean-all: clean ## Clean all artifacts including virtual environment
	rm -rf .venv/
	rm -rf .tox/

# Release
.PHONY: release-check
release-check: lint test build check-build ## Run all checks before release
	@echo "All checks passed! Ready for release."

.PHONY: release-test
release-test: release-check ## Upload to test PyPI
	twine upload --repository testpypi dist/*

.PHONY: release
release: release-check ## Upload to PyPI
	twine upload dist/*

# Development utilities
.PHONY: run
run: ## Run the CLI application
	PYTHONPATH=$(PWD) $(PYTHON) -m $(PACKAGE_NAME) --help || true

.PHONY: shell
shell: ## Start Python shell with package imported
	$(PYTHON) -c "import $(PACKAGE_NAME); print('Package $(PACKAGE_NAME) imported'); import IPython; IPython.start_ipython()"

.PHONY: requirements
requirements: ## Generate requirements.txt from pyproject.toml
	$(PIP) freeze > requirements.txt

.PHONY: update-deps
update-deps: ## Update all dependencies
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install --upgrade -e ".[dev,test,docs]"

# CI/CD helpers
.PHONY: ci-test
ci-test: ## Run tests in CI environment
	pytest --cov=$(SRC_DIR) --cov-report=xml $(TESTS_DIR)

.PHONY: ci-lint
ci-lint: ## Run linting in CI environment
	black --check $(SRC_DIR) $(TESTS_DIR)
	ruff check $(SRC_DIR) $(TESTS_DIR)
	mypy $(SRC_DIR)

# Git helpers
.PHONY: git-tag
git-tag: ## Create git tag from package version
	@VERSION=$$($(PYTHON) -c "import $(PACKAGE_NAME); print($(PACKAGE_NAME).__version__)"); \
	git tag -a "v$$VERSION" -m "Release v$$VERSION"; \
	echo "Created tag v$$VERSION"

.PHONY: status
status: ## Show project status
	@echo "=== Project Status ==="
	@echo "Package: $(PACKAGE_NAME)"
	@VERSION=$$($(PYTHON) -c "import $(PACKAGE_NAME); print($(PACKAGE_NAME).__version__)"); \
	echo "Version: $$VERSION"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Git status:"
	@git status --short
	@echo "=== Dependencies ==="
	@$(PIP) list | grep -E "($(PACKAGE_NAME)|pytest|black|ruff|mypy)"