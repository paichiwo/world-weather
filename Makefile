ACTIVATE = source venv/bin/activate

lint:
	$(ACTIVATE) && isort .
	$(ACTIVATE) && black -S .
	$(ACTIVATE) && ruff .

test:
	$(ACTIVATE) && pytest
