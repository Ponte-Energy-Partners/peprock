UV_NO_PROGRESS = 1

environment:
	uv sync --frozen
	@echo
	uv run prek install

bump_dependencies:
	uv run prek auto-update --no-progress
	@echo
	uv sync --upgrade
	uv pip list --outdated --strict

check:
	uv run prek run --all-files --no-progress
	@echo
	uv run pytest
