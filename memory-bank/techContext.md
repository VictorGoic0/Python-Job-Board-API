# Tech Context: Job Board API

## Stack (from PRD)

| Layer | Choice |
|-------|--------|
| Language | Python 3.11 |
| Framework | Flask 3.x |
| Database | PostgreSQL (Dockerized) |
| ORM | SQLAlchemy 2.x |
| Migrations | Raw SQL + Python runner script |
| Validation | Marshmallow (Flask-Marshmallow, marshmallow-sqlalchemy) |
| API docs | Flask-SMOREST (OpenAPI/Swagger) |
| DI | Flask-Injector |
| Task queue | Celery, broker RabbitMQ |
| Auth | Flask-JWT-Extended (Phase IV) |
| Testing | pytest, pytest-cov, pytest-flask (80% coverage goal) |
| Containers | Docker, Docker Compose |

## Development Setup

- **Env**: `python -m venv venv`, `pip install -r requirements.txt`; use `.env` (see `.env.example`).
- **DB**: Docker Compose starts Postgres (port 5432) and RabbitMQ (5672, management 15672). Run `python migrations/run_migrations.py` to apply SQL migrations.
- **App**: `flask run` or Docker Compose app service (port 5000); Swagger at `http://localhost:5000/swagger`.
- **Tests**: `pytest`; use `TestingConfig` and test DB (e.g. `job_board_test`).

## Technical Constraints

- PostgreSQL and RabbitMQ required for full stack; test DB for pytest.
- Enums: JobType (FULL_TIME, PART_TIME, CONTRACT, INTERNSHIP), ExperienceLevel (ENTRY, MID, SENIOR), RemoteOption (REMOTE, HYBRID, ONSITE).
- Pagination: default page size 20, max 100; applied to list/search/active endpoints.
- File upload (Phase IV): allowed types (e.g. pdf, doc, docx), max size 5MB; stored under configurable path (e.g. uploads/resumes).

## Dependencies (Phase I snapshot from PRD)

- Flask 3.0.0, Flask-SQLAlchemy 3.1.1, Flask-Marshmallow 0.15.0, marshmallow-sqlalchemy 0.29.0
- Flask-CORS 4.0.0, Flask-Injector 0.15.0, python-dotenv 1.0.0
- psycopg2-binary 2.9.9, SQLAlchemy 2.0.23
- flask-smorest 0.42.3
- pytest 7.4.3, pytest-cov 4.1.0, pytest-flask 1.3.0

Exact versions should be pinned in `requirements.txt`; only add/change after checking compatibility with Python 3.11 and each other.
