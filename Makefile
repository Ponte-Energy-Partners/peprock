UV_NO_PROGRESS = 1

environment:
	uv sync --frozen
	@echo
	uv run pre-commit install

bump_dependencies:
	uv run pre-commit autoupdate --jobs 10
	@echo
	uv sync --upgrade
	uv pip list --outdated --strict

check:
	uv run pre-commit run --all-files
	@echo
	uv run pytest
