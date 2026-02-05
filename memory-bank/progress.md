# Progress: Job Board API

## What Works

- **PR #1**: Project structure, requirements, config, `.env.example`, `.gitignore`, `run_server.py`, Docker (Dockerfile, docker-compose: postgres, rabbitmq, app; celery-worker/beat under profile `celery`), app factory (extensions, create_app, CORS, Flask-Injector placeholder), migrations (single `001_initial_schema.sql` + down, runner with up/status/down, schema_migrations), verification (venv, Docker, migrations, Swagger).
- **PR #2**: Models (enums, Company, Job with `utc_now`), schemas (CompanySummary/Company/CompanyCreate/CompanyUpdate, Job/JobDetail/JobCreate/JobUpdate), custom exceptions, global error handlers, `tests/unit/test_schemas.py` (model import, schema validation, salary/expiry validators).
- **Docs**: PRD, tasks-phase1.md, memory bank, root README (setup, Docker vs local run, tests location and commands, migrations pointer), migrations README, `pytest.ini` (pythonpath = .).

## What's Left to Build

### Phase I (Current)

- [ ] PR #3: Repositories (Company, Job), services with DI, blueprints (companies, jobs), Flask-Injector binding, full CRUD and validation.
- [ ] Phase I acceptance: Docker up, DB connected, CRUD working, 400/404/409 handled, Swagger at `/swagger`, timestamps and FKs correct.

### Phase II

- Search/filter endpoint, pagination, active jobs, deactivate endpoint.

### Phase III

- More unit, integration, and API tests; 80%+ coverage.

### Phase IV

- Auth (User, JWT, roles), file upload, Application model and endpoints, Celery (add to requirements, `app.tasks.celery`, then `docker-compose --profile celery up`).

### Stretch (Optional)

- Connection pooling, Redis cache, rate limiting, structured logging, Prometheus, email on application status, full-text search, API versioning, CI/CD, README/API docs.

## Current Status

- **Phase**: Phase I; PR #1 and PR #2 done.
- **Blockers**: None.
- **Last updated**: Memory bank and README updated (PR #2 complete, tests location and commands).

## Known Issues

- None. If "address already in use" when running `flask run`, the Docker app container is already binding port 5000 — stop it or use Docker for the app.
