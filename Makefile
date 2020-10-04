.PHONY: setup setup_pipenv install update test test_mypy test_unit test_format format
PIPENV_VERBOSITY=-1

setup: setup_pipenv install

setup_pipenv:
	pip install pipenv

install:
	pipenv install --dev --skip-lock

update:
	pipenv update --dev
	pipenv clean
	pipenv run  pip list --outdated

test: test_mypy test_unit test_format

test_mypy:
	pipenv run mypy --config-file mypy.ini constrained_types tests

test_unit:
	pipenv run pytest tests -vv

test_format:
	pipenv run black --check tests constrained_types

format:
	pipenv run black tests constrained_types