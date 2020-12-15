PYTHON = $(shell which python3)
POETRY = $(shell which poetry)
PIP = $(shell which pip3)
DOCKER-COMPOSE = $(shell which docker-compose)

setlocalenv:
	cp app/app/local_settings.example.py app/app/local_settings.py

createvenv:
	$(PYTHON) -m venv .venv
	$(POETRY) run $(PIP) install --upgrade pip
	$(POETRY) ru-n poetry install

makemigrations:
	$(DOCKER-COMPOSE) run web python manage.py makemigrations

migrate:
	$(DOCKER-COMPOSE) run web python manage.py migrate

shell:
	$(DOCKER-COMPOSE) run web python manage.py shell

black:
	$(POETRY) run black app
