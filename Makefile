.PHONY: env run tests docs
.DEFAULT: env

env:
	@pipenv install --dev

run:
	@pipenv run gunicorn miskatonic.app:app

test:
	@pipenv run coverage run --branch -m unittest discover; pipenv run coverage html

lint:
	@pipenv run isort --virtual-env .venv miskatonic/*.py

docs:
	@sphinx-apidoc -o docs/source/ ../miskatonic/
	@cd docs && make html
