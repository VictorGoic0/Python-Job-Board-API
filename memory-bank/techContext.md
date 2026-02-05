# Tech Context: Job Board API

## Stack (from PRD)

| Layer | Choice |
|-------|--------|
| Language | Python 3.11 |
| Framework | Flask 3.x |
| Database | PostgreSQL (Dockerized) |
| ORM | SQLAlchemy 2.x |
| Migrations | Raw SQL + Python runner (up/status/down, schema_migrations) |
| Validation | Marshmallow (Flask-Marshmallow, marshmallow-sqlalchemy) |
| API docs | Flask-SMOREST (OpenAPI/Swagger) |
| DI | Flask-Injector |
| Task queue | Celery, broker RabbitMQ (Phase IV; Compose profile `celery`) |
| Auth | Flask-JWT-Extended (Phase IV) |
| Testing | pytest, pytest-cov, pytest-flask (80% coverage goal) |
| Containers | Docker, Docker Compose |

## Development Setup

1. **Venv and deps**: `python3 -m venv venv`, activate, `pip install -r requirements.txt`. Use `.env` (see `.env.example`).
2. **DB**: Docker Compose starts Postgres (5432) and RabbitMQ (5672, management 15672). Run migrations with venv active: `python migrations/run_migrations.py up`.
3. **App**: Either (a) Docker app service (`docker-compose up -d` → app on 5000) or (b) local `FLASK_APP=run_server flask run`. Do not run both; Docker app binds 5000 and causes "address already in use" if you also run `flask run`.
4. **Swagger**: http://localhost:5000/swagger (when app is running via Docker or locally).
5. **Tests**: `tests/unit/` (services, schemas), `tests/integration/` (repositories), `tests/api/` (endpoints). Run from project root with venv active: `pytest` (all), `pytest tests/unit/ -v` (unit only). `pytest.ini` sets `pythonpath = .` so `app` imports work. Use `TestingConfig` and test DB (e.g. `job_board_test`) for integration/API tests.

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

Exact versions pinned in `requirements.txt`; only add/change after checking compatibility with Python 3.11 and each other.
