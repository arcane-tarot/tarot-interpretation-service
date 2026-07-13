venv:
	python3 -m venv .venv

install: venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

format:
	.venv/bin/black app tests

lint:
	.venv/bin/black --check app tests
	.venv/bin/flake8 app tests

test:
	.venv/bin/pytest -vv

run:
	.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

docker-build:
	docker build -t tarot-interpretation-service .

