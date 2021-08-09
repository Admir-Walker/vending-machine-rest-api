# Vending Machine Rest API

Rest API for a vending machine that allows users with a 'seller' role to add, update or remove products, while users with a 'buyer role' can deposit coins into the machine and make purchases.

`Important note`: .env file is published for demo purposes only to ease application setup.

## Tech
Rest API use a number of open source projects to work properly:

- [Flask] - Lightweight web application framework.
- [Flask-Bcrypt] - Flask extension that provides bcrypt hashing utilities.
- [Flask-Migrate] - Flask extension that handles SQLAlchemy database migrations using Alembic.
- [Flask-RESTful] - Flask extension that adds support for quickly building REST APIs. 
- [Flask-SQLAlchemy] - Flask extension that adds support for SQLAlchemy to your application.
- [marshmallow] - ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes
- [PyJWT] - Python library which allows you to encode and decode JSON Web Tokens (JWT).
- [pytest] - Testing framework.
- [webargs] - Python library for parsing and validating HTTP request objects.
- [python-dotenv] - Python-dotenv reads key-value pairs from a .env file and can set them as environment variables.
## Installation
### Installation using Docker

The easiest way to install, navigate to the project root and type in your preferred terminal:
```sh
$ docker-compose up
```

Verify the installation by navigating to link below in your preferred browser.

```sh
http://127.0.0.1:8000/
```

### Installation without Docker
Vending Machine Rest API requires:
- [Python](https://www.python.org/) 3.8.2+ to run.
- [PostgreSQL](https://www.postgresql.org/)

When you meet specified requirements, it's necessary to manually create two postgres databases named `vending_machine` and `vending_machine_test`.

After database creation, modify .env file to make sure your database credentials are
#### Installation on MacOS/Linux
Navigate to the project root and type in your preferred terminal:
```sh
$ make all
```
This command will install the required dependencies, run migrations and flask application

Verify the installation by navigating to link below in your preferred browser.

```sh
http://127.0.0.1:5000/
```

#### Installation on Windows

Navigate to the project root and type in your preferred terminal:
```sh
> py -3 -m venv venv
> venv\Scripts\activate
> pip install -r requirements.txt
> flask db init
> flask db migrate -m 'Initial migration'
> flask db upgrade
> flask run
```

Verify the installation by navigating to link below in your preferred browser.

```sh
http://127.0.0.1:5000/
```
## Testing

Before testing, make sure you installed application successfully.

### Testing using Docker

Navigate to the project root and type in your preferred terminal:
```sh
$ docker-compose exec web coverage run -m pytest
```

### Testing without Docker

#### Testing on MacOS/Linux
To run tests navigate to the project root and type in your preferred terminal:
```sh
$ make coverage
```
#### Testing on Windows
To run tests navigate to the project root and type in your preferred terminal:
```sh
> venv\Scripts\activate
> coverage run -m pytest
> coverage report
```

[Flask]: https://flask.palletsprojects.com/
[Flask-Bcrypt]: https://flask-bcrypt.readthedocs.io/en/latest/
[Flask-Migrate]: https://flask-migrate.readthedocs.io/en/latest/
[Flask-RESTful]: https://flask-restful.readthedocs.io/en/latest/
[Flask-SQLAlchemy]: https://flask-sqlalchemy.palletsprojects.com/
[marshmallow]: https://marshmallow.readthedocs.io/en/stable/
[PyJWT]: https://pyjwt.readthedocs.io/en/stable/
[pytest]: https://pytest.org
[python-dotenv]: https://pypi.org/project/python-dotenv/
[webargs]: https://webargs.readthedocs.io/en/latest/
