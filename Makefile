.PHONY: help bootstrap lint test outdated clean

VENV=.venv
PYTHON=$(VENV)/bin/python

help:
	@echo "Available targets:"
	@echo "  bootstrap - prepare virtual environment and install dependencies"
	@echo "  lint      - run static code analysis"
	@echo "  test      - run project tests"
	@echo "  outdated  - show outdated dependencies"
	@echo "  clean     - remove virtual environment and development artifacts"

bootstrap: $(PYTHON)
$(PYTHON):
	python -m venv $(VENV)
	$(VENV)/bin/python -m pip install pip==24.0 setuptools==70.0.0 wheel==0.43.0
	$(VENV)/bin/python -m pip install -e .[dev]

lint: bootstrap
	$(PYTHON) -m ruff check taina tests

test: bootstrap
	$(PYTHON) -m pytest

outdated: bootstrap
	$(PYTHON) -m pip list --outdated

clean:
	rm -rf $(VENV) taina.egg-info .pytest_cache .ruff_cache
	find ./ -name "__pycache__" -type d | xargs rm -rf
