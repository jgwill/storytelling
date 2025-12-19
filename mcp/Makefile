# Makefile for storytelling-mcp package

PYTHON := python3
PIP := pip

.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "%-15s %s\n", $$1, $$2}'

.PHONY: install
install: ## Install mcp package in development mode
	$(PIP) install -e .

.PHONY: install-dev
install-dev: ## Install with dev dependencies
	$(PIP) install -e ".[dev,test]"

.PHONY: format
format: ## Format code
	black server.py
	ruff check --fix server.py

.PHONY: lint
lint: ## Run linting (black and ruff check)
	black --check server.py
	ruff check server.py

.PHONY: test
test: ## Run tests
	pytest tests

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf build dist *.egg-info .pytest_cache .coverage .mypy_cache .ruff_cache htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

.PHONY: build
build: clean ## Build mcp package
	$(PYTHON) -m build

.PHONY: release
release: build ## Build package for release (no tests, just build)
	@echo "✅ Build complete. Ready to publish."
	@echo ""
	@echo "📤 Next: twine upload dist/*"

.PHONY: release-check
release-check: lint ## Run checks before release
	@echo "✅ Pre-release checks passed"
