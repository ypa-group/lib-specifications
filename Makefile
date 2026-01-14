.PHONY: test test-unit test-integration test-e2e test-all test-coverage test-watch test-lint help

# Default Python interpreter
PYTHON := python
PYTEST := pytest

# Test directories
TEST_DIR := tests
UNIT_DIR := $(TEST_DIR)/unit
INTEGRATION_DIR := $(TEST_DIR)/integration
E2E_DIR := $(TEST_DIR)/e2e

help: ## Show this help message
	@echo "Available test commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test: test-unit ## Run all unit tests (default)

test-unit: ## Run only unit tests
	$(PYTEST) $(UNIT_DIR) -m unit

test-integration: ## Run only integration tests
	$(PYTEST) $(INTEGRATION_DIR) -m integration

test-e2e: ## Run only end-to-end tests
	$(PYTEST) $(E2E_DIR) -m e2e

test-all: ## Run all tests (unit, integration, e2e)
	$(PYTEST) $(TEST_DIR)

test-coverage: ## Run tests with coverage report
	$(PYTEST) --cov=lib_specifications --cov-report=html --cov-report=term-missing $(TEST_DIR)
	@echo "Coverage report generated in htmlcov/index.html"

test-coverage-xml: ## Run tests with coverage report in XML format (for CI)
	$(PYTEST) --cov=lib_specifications --cov-report=xml --cov-report=term $(TEST_DIR)

test-fast: ## Run only fast tests (exclude slow markers)
	$(PYTEST) $(TEST_DIR) -m "not slow"

test-watch: ## Run tests in watch mode (requires pytest-watch)
	ptw $(TEST_DIR)

test-lint: ## Run linting on test files
	ruff check $(TEST_DIR) || true

test-debug: ## Run tests with debugging output
	$(PYTEST) $(TEST_DIR) -vv -s --pdb

test-parallel: ## Run tests in parallel (requires pytest-xdist)
	$(PYTEST) $(TEST_DIR) -n auto

test-specific: ## Run a specific test file (usage: make test-specific FILE=tests/unit/lib_specifications/core/test_base.py)
	$(PYTEST) $(FILE)

test-marker: ## Run tests with specific marker (usage: make test-marker MARKER=async)
	$(PYTEST) $(TEST_DIR) -m $(MARKER)

clean-test: ## Clean test artifacts
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .tox
	rm -rf dist
	rm -rf build

