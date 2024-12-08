environment:
	uv sync --frozen
	uv run pre-commit install

bump_dependencies:
	uv sync --upgrade
	uv run pre-commit autoupdate
	uv pip list --outdated

check:
	uv run pre-commit run --all-files
	uv run pytest
