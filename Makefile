.PHONY: help lint lint-ansible lint-yaml lint-python lint-markdown format test clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

lint: lint-ansible lint-yaml lint-python lint-markdown ## Run all linters

lint-ansible: ## Run ansible-lint
	@echo "Running ansible-lint..."
	@ansible-lint --force-color

lint-yaml: ## Run yamllint
	@echo "Running yamllint..."
	@yamllint .

lint-python: ## Run Python linters (ruff, black, isort, pylint)
	@echo "Running ruff..."
	@ruff check plugins/
	@echo "Running black..."
	@black --check plugins/
	@echo "Running isort..."
	@isort --check-only plugins/
	@echo "Running pylint..."
	@pylint plugins/**/*.py

lint-markdown: ## Run markdownlint
	@echo "Running markdownlint..."
	@docker run --rm -v "$(PWD):/workdir" davidanson/markdownlint-cli2:latest "**/*.md"

format: ## Auto-format Python code
	@echo "Formatting with black..."
	@black plugins/
	@echo "Sorting imports with isort..."
	@isort plugins/

test: ## Run ansible-test sanity
	@echo "Running ansible-test sanity..."
	@ansible-test sanity --docker --color

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
	@pip install ansible-core ansible-lint yamllint ruff black isort pylint

.DEFAULT_GOAL := help
