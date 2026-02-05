# Progress: Job Board API

## What Works

- **PR #1 (through 1.5)**: Project structure, requirements, config, `.env.example`, `.gitignore`, `run_server.py`, Docker (Dockerfile, docker-compose: postgres, rabbitmq, app; celery-worker/beat under profile `celery`), app factory (extensions, create_app, CORS, Flask-Injector placeholder), migrations (single `001_initial_schema.sql` + down, runner with up/status/down, schema_migrations).
- **Docs**: PRD, tasks-phase1.md, memory bank, root README (setup, Docker vs local run), migrations README (prerequisites, commands).
- **Verification flow**: Venv + pip install → Docker up → run migrations (venv) → app via Docker on 5000 (or stop app container and use local `flask run`). Swagger at /swagger.

## What's Left to Build

### Phase I (Current)

- [ ] Task 1.6: Confirm venv, Docker, migrations, Swagger per updated checklist.
- [ ] PR #2: Models (Company, Job, enums), Marshmallow schemas (company, job, pagination), custom exceptions, error handlers.
- [ ] PR #3: Repositories (Company, Job), services with DI, blueprints (companies, jobs), Flask-Injector binding, full CRUD and validation.
- [ ] Phase I acceptance: Docker up, DB connected, CRUD working, 400/404/409 handled, Swagger at `/swagger`, timestamps and FKs correct.

### Phase II

- Search/filter endpoint, pagination, active jobs, deactivate endpoint.

### Phase III

- Unit, integration, and API tests; 80%+ coverage; pytest config.

### Phase IV

- Auth (User, JWT, roles), file upload, Application model and endpoints, Celery (add to requirements, `app.tasks.celery`, then `docker-compose --profile celery up`).

### Stretch (Optional)

- Connection pooling, Redis cache, rate limiting, structured logging, Prometheus, email on application status, full-text search, API versioning, CI/CD, README/API docs.

## Current Status

- **Phase**: Phase I; PR #1 done (1.1–1.5), 1.6 documented and aligned with current setup.
- **Blockers**: None.
- **Last updated**: Task 1.6 and docs/memory bank updated (venv, migrations, Docker vs local run).

## Known Issues

- None. If "address already in use" when running `flask run`, the Docker app container is already binding port 5000 — stop it or use Docker for the app.
