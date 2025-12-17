# Makefile for storytelling package

PYTHON := python3
PIP := pip

.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "%-15s %s\n", $$1, $$2}'

.PHONY: install
install: ## Install package in development mode
	$(PIP) install -e .

.PHONY: install-dev
install-dev: ## Install with dev dependencies
	$(PIP) install -e ".[dev,test]"

.PHONY: format
format: ## Format code
	black storytelling tests
	ruff check --fix storytelling tests

.PHONY: lint
lint: ## Run linting
	black --check storytelling tests
	ruff check storytelling tests

.PHONY: test
test: ## Run tests
	pytest tests

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf build dist *.egg-info .pytest_cache .coverage .mypy_cache .ruff_cache htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

.PHONY: build
build: clean ## Build package
	$(PYTHON) -m build

.PHONY: check
check: lint test ## Run lint and tests
	@echo "✓ All checks passed"
