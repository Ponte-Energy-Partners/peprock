UV_NO_PROGRESS = 1

environment:
	uv sync --frozen
	uv run pre-commit install

bump_dependencies:
	uv sync --upgrade
	uv run pre-commit autoupdate --jobs 10
	uv pip list --outdated

check:
	uv run pre-commit run --all-files
	uv run pytest
