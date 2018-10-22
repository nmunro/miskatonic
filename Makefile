.PHONY: env run tests docs
.DEFAULT: env

env:
	@pipenv install --dev

run:
	@pipenv run flask run

test:
	@pipenv run coverage run --branch -m unittest discover; pipenv run coverage html

lint:
	@pipenv run isort --virtual-env .venv miskatonic/*.py; pipenv run coala all

docs:
	@sphinx-apidoc -o docs/source/ ../miskatonic/
	@cd docs && make html
