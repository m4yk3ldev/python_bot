.DEFAULT_GOAL := help
.PHONY: help format

format: ## Format code that autopep8
	autopep8 --in-place --aggressive --aggressive --aggressive --aggressive *.py

lint: ## Linter to pylint
	pylint -E *.py

help: ## List available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'