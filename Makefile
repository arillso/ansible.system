.PHONY: help lint lint-ansible lint-yaml lint-python format test build clean install-dev

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

lint: lint-ansible lint-yaml lint-python ## Run all linters

lint-ansible: ## Run ansible-lint
	@echo "Running ansible-lint..."
	@ansible-lint --force-color

lint-yaml: ## Run yamllint
	@echo "Running yamllint..."
	@yamllint .

lint-python: ## Run Python linters (ruff, black)
	@if [ -n "$$(find plugins/ -name '*.py' 2>/dev/null)" ]; then \
		echo "Running ruff..."; \
		ruff check plugins/; \
		echo "Running black..."; \
		black --check plugins/; \
	else \
		echo "No Python plugins found, skipping..."; \
	fi

format: ## Auto-format Python code
	@if [ -n "$$(find plugins/ -name '*.py' 2>/dev/null)" ]; then \
		echo "Formatting with black..."; \
		black plugins/; \
		echo "Sorting imports with ruff..."; \
		ruff check --fix --select I plugins/; \
	else \
		echo "No Python plugins found, skipping..."; \
	fi

test: ## Run tests
	@echo "Running pytest..."
	@pytest tests/unit/

build: ## Build collection
	@echo "Building collection..."
	@ansible-galaxy collection build --force

clean: ## Clean build artifacts
	@echo "Cleaning build artifacts..."
	@rm -rf *.tar.gz
	@rm -rf .ansible/
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

install-dev: ## Install development dependencies
	@echo "Installing development dependencies..."
	@pip install -r requirements.txt

.DEFAULT_GOAL := help
