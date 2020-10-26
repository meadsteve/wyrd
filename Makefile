.PHONY: setup setup_pipenv install update test test_mypy test_unit test_format format publish
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
	pipenv run mypy --config-file mypy.ini wyrd tests

test_unit:
	pipenv run pytest tests -vv

test_format:
	pipenv run black --check tests wyrd

format:
	pipenv run black tests wyrd

publish:
	./scripts/publish.sh