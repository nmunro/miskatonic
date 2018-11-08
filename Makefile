.PHONY: env run deploy lint tests docs
.DEFAULT: env

env:
	@poetry install

run:
	@source .env && poetry run gunicorn miskatonic.app:app

test:
	@source .env && poetry run coverage run --branch -m unittest discover && poetry run coverage html

deploy:
	@git push -u heroku master

lint:
	@source .env && poetry run isort --virtual-env .venv miskatonic/*.py

docs:
	@sphinx-apidoc -o docs/source/ miskatonic/
	@cd docs && make html
