# Display command list
default:
	@just --list

# Format code
fmt:
	pipenv run isort .
	pipenv run black .

# Lint code
lint:
	pipenv run flake8 .
	pipenv run mypy .

# Test
test:
	pipenv run python -m pytest -vv tests

# Test with pdb postmortem
test-debug:
	pipenv run python -m pytest -vv tests --pdb

# Test with coverage (html)
test-cov:
	pipenv run python -m pytest -vv tests --cov --cov-report=html

# Test with coverage (terminal)
test-cov-term:
	pipenv run python -m pytest -vv tests --cov --cov-report=term

# Test with coverage (for CI)
test-cov-ci:
	pipenv run python -m pytest -vv tests --cov --cov-report=xml --junit-xml pytest.xml

# Install in development mode
install-dev:
	pip install -e .
