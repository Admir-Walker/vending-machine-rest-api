.ONESHELL:
.PHONY: all

create:
	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt

db:
	. venv/bin/activate
	flask db init
	flask db migrate -m 'Initial migration'
	flask db upgrade

migrate:
	. venv/bin/activate 
	flask db migrate 
	flask db upgrade

run:
	. venv/bin/activate
	flask run

test:
	. venv/bin/activate
	pytest

all: create db run