fmt:
	pipenv run isort .
	pipenv run black .

lint:
	pipenv run flake8 .
	pipenv run mypy .

test:
	pipenv run python -m pytest -vv tests

test-cov:
	pipenv run python -m pytest -vv tests --cov --cov-report=html

install-dev:
	pip install -e .
