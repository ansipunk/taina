.PHONY: help bootstrap migrate lint test outdated clean

VENV=.venv
PYTHON=$(VENV)/bin/python

help:
	@echo "Available targets:"
	@echo "  bootstrap - prepare virtual environment and install dependencies"
	@echo "  migrate   - create database and run schema migrations"
	@echo "  lint      - run static code analysis"
	@echo "  test      - run project tests"
	@echo "  outdated  - show outdated dependencies"
	@echo "  clean     - remove virtual environment and development artifacts"

bootstrap: $(PYTHON)
$(PYTHON):
	python -m venv $(VENV)
	$(VENV)/bin/python -m pip install pip==24.1.2 setuptools==70.3.0 wheel==0.43.0
	$(VENV)/bin/python -m pip install -e .[dev]

migrate: bootstrap
	sudo -u postgres psql -c "CREATE USER taina WITH PASSWORD 'taina';" || true
	sudo -u postgres psql -c "ALTER USER taina CREATEDB;" || true
	sudo -u postgres psql -c "CREATE DATABASE taina OWNER taina;" || true
	$(PYTHON) -m alembic upgrade head

dev: bootstrap
	$(PYTHON) -m uvicorn taina:app

lint: bootstrap
	$(PYTHON) -m ruff check --fix taina tests

test: bootstrap
	$(PYTHON) -m pytest

outdated: bootstrap
	$(PYTHON) -m pip list --outdated

clean:
	rm -rf $(VENV) htmlcov taina.egg-info .coverage .pytest_cache .ruff_cache
	find ./ -name "__pycache__" -type d | xargs rm -rf
