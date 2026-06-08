.PHONY: install run test

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest
