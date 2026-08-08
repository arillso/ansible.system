.PHONY: help lint lint-ansible lint-yaml lint-python format test test-unit test-molecule test-molecule-% build clean install-dev

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

lint: lint-ansible lint-yaml lint-python ## Run all linters

lint-ansible: ## Run ansible-lint (skipped when ansible-lint is missing; CI is the gate)
	@if ! command -v ansible-lint >/dev/null 2>&1; then \
		echo "SKIP: ansible-lint not installed"; \
	else \
		echo "Running ansible-lint..."; \
		ansible-lint --force-color; \
	fi

lint-yaml: ## Run yamllint
	@echo "Running yamllint..."
	@yamllint .

lint-python: ## Run Python linters (skipped when ruff/black are missing; CI is the gate)
	@if [ -z "$$(find plugins/ -name '*.py' 2>/dev/null)" ]; then \
		echo "No Python plugins found, skipping..."; \
	elif ! command -v ruff >/dev/null 2>&1; then \
		echo "SKIP: ruff not installed"; \
	elif ! command -v black >/dev/null 2>&1; then \
		echo "SKIP: black not installed"; \
	else \
		echo "Running ruff..."; \
		ruff check plugins/; \
		echo "Running black..."; \
		black --check plugins/; \
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

test: test-unit ## Run unit tests (alias for test-unit)

test-unit: ## Run pytest unit suite (skipped when pytest is missing; CI is the gate)
	@if ! command -v pytest >/dev/null 2>&1; then \
		echo "SKIP: pytest not installed"; \
	else \
		echo "Running pytest..."; \
		pytest tests/unit/; \
	fi

# Scenarios declaring the docker driver need a reachable daemon; the qemu (KVM)
# scenarios do not, so the daemon is checked per scenario, not globally.
define molecule_needs_docker
grep -qE '^[[:space:]]*name:[[:space:]]*docker[[:space:]]*$$' extensions/molecule/$(1)/molecule.yml
endef

test-molecule: ## Run every molecule scenario (slow; scenarios without their driver are skipped)
	@if ! command -v molecule >/dev/null 2>&1; then \
		echo "SKIP: molecule not installed"; \
	else \
		echo "Running every molecule scenario..."; \
		for s in $$(ls extensions/molecule | grep -v '^\.'); do \
			if $(call molecule_needs_docker,$$s) && ! docker info >/dev/null 2>&1; then \
				echo "SKIP $$s: docker daemon not available"; \
				continue; \
			fi; \
			echo "==> molecule test -s $$s"; \
			(cd extensions && molecule test -s $$s) || exit $$?; \
		done; \
	fi

test-molecule-%: ## Run a single molecule scenario (e.g. make test-molecule-access)
	@if ! command -v molecule >/dev/null 2>&1; then \
		echo "SKIP: molecule not installed"; \
	elif $(call molecule_needs_docker,$*) && ! docker info >/dev/null 2>&1; then \
		echo "SKIP: docker daemon not available"; \
	else \
		echo "Running molecule scenario: $*"; \
		cd extensions && molecule test -s $*; \
	fi

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
