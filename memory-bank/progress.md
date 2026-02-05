# Progress: Job Board API

## What Works

- **PR #1**: Project structure, requirements, config, `.env.example`, `.gitignore`, `run_server.py`, Docker (Dockerfile, docker-compose: postgres, rabbitmq, app; celery under profile `celery`), app factory (extensions, create_app, CORS, Flask-Injector), migrations (001_initial_schema + down, run_migrations.py up/status/down, schema_migrations), verification (venv, Docker, migrations, Swagger).
- **PR #2**: Models (enums, Company, Job with utc_now), schemas (company + job create/update/response), custom exceptions, error handlers, tests/unit/test_schemas.py, pytest.ini.
- **PR #3**: CompanyRepository, JobRepository (SQLAlchemy 2, joinedload for Job); CompanyService, JobService (@inject, create/update/delete, StaleDataError → OptimisticLockException); _configure_injector (CompanyRepository, JobRepository, CompanyService, JobService as singletons). No routes yet (PR #4 reverted).
- **Docs**: PRD, tasks-phase1.md, memory bank, root README, migrations README, root `context.md` (PR-by-PR summary for fresh sessions).

## What's Left to Build

### Phase I (Current)

- [ ] PR #4: Company routes (companies_blp), Job routes (jobs_blp), blueprint registration in app/__init__.py; then 4.4/4.5 manual testing.
- [ ] Phase I acceptance: Docker up, DB connected, CRUD working, 400/404/409 handled, Swagger at `/swagger`.

### Phase II

- Search/filter, pagination, active jobs, deactivate endpoint.

### Phase III

- More tests; 80%+ coverage.

### Phase IV

- Auth, file upload, Application model, Celery (profile `celery`).

### Stretch

- Connection pooling, Redis, rate limiting, logging, Prometheus, etc.

## Current Status

- **Phase**: Phase I; PR #1, #2, #3 done; PR #4 next.
- **Blockers**: None.
- **Last updated**: Memory bank + root context.md (PR #3 complete, PR #4 reverted, next = routes).

## Known Issues

- None. If "address already in use" when running `flask run`, Docker app is already on 5000 — stop app container or use Docker for the app.
