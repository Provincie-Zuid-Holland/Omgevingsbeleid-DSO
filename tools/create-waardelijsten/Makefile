.DEFAULT_GOAL := help
default: help;
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


create-gebiedsaanwijzingen:
	@python app/cmds.py create-gebiedsaanwijzingen

check: ## Check without fixing via Ruff
	python -m ruff check app/

check-fix: ## Fix issues found by Ruff
	python -m ruff check --fix app/

format: ## Format code via Ruff
	python -m ruff format app/

fix: check-fix format ## Fix and Format the code via Ruff
