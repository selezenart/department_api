# Department API

A REST API for managing company departments and their employees, built with Flask. Each department tracks its staff and recalculates the average salary whenever employees join or leave.

## Features

- **Departments.** Full CRUD. A department's average salary updates automatically as its staff changes.
- **Employees.** Full CRUD, including moving an employee between departments and changing salaries.
- **Authentication.** Register with `/register`. Log in with `/login` using HTTP Basic auth to get a JWT, which is valid for one hour. Protected endpoints read the token from the `X-API-KEY` header.
- **Validation and serialization.** Handled by marshmallow schemas.
- **Database.** Schema managed with Flask-Migrate (Alembic) migrations.
- **Tests and CI.** pytest suite with coverage and pycodestyle linting, run on Travis CI.
- **Deployment.** Dockerfile and `heroku.yml` for container deployment with Gunicorn.

## Tech stack

Python · Flask · Flask-RESTful · SQLAlchemy · marshmallow · PyJWT · PostgreSQL · Alembic · pytest · Docker · Travis CI

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/departments` | List departments |
| GET | `/departments/<uuid>` | Get one department |
| POST | `/departments` | Create a department |
| PUT / PATCH | `/departments/<uuid>` | Update the title or staff |
| GET | `/employees` | List employees |
| GET | `/employees/<uuid>` | Get one employee |
| POST | `/employees` | Create an employee |
| PUT / PATCH | `/employees/<uuid>` | Update an employee |
| DELETE | `/employees/<uuid>` | Delete an employee |
| POST | `/register` | Create a user |
| GET | `/login` | Get a JWT (HTTP Basic auth) |
| GET | `/smoke` | Health check |

## Project structure

```
app/
├── models/      # SQLAlchemy models: Departament, Employee, User
├── schemas/     # marshmallow schemas
├── services/    # database access logic
├── resources/   # Flask-RESTful endpoints + auth
└── routes.py    # URL registration
migrations/      # Alembic migrations
tests/           # pytest suite
```

## Run locally

```bash
git clone https://github.com/selezenart/department_api.git
cd department_api
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
flask run
```

By default the app uses the bundled SQLite database in `data/app.db`. To use PostgreSQL, set the environment variables and apply the migrations:

```bash
export DATABASE_URL=postgresql://user:password@localhost:5432/departments
export SECRET_KEY=change-me
flask db upgrade
```

Or run it in Docker:

```bash
docker build -t department-api .
docker run -p 5000:5000 department-api
```

Run the tests with:

```bash
python -m pytest tests/
```
