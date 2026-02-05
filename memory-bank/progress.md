# Progress: Job Board API

## What Works

- **Documentation**: PRD and Phase I task breakdown (`tasks-phase1.md`) are in place.
- **Memory bank**: Initialized; six core files populated from PRD.
- **Codebase**: No application code yet; project directory has only PRD and tasks.

## What's Left to Build

### Phase I (Current)

- [ ] PR #1: Project structure, requirements, config, Docker (Postgres, RabbitMQ, app, Celery placeholders), app factory (extensions, CORS), migrations (SQL + runner), verification (Compose, migrate, Swagger).
- [ ] PR #2: Models (Company, Job, enums), Marshmallow schemas (company, job, pagination), custom exceptions, error handlers.
- [ ] PR #3: Repositories (Company, Job), services with DI, blueprints (companies, jobs), Flask-Injector binding, full CRUD and validation.
- [ ] Phase I acceptance: Docker up, DB connected, CRUD working, 400/404/409 handled, Swagger at `/swagger`, timestamps and FKs correct.

### Phase II

- Search/filter endpoint, pagination, active jobs, deactivate endpoint.

### Phase III

- Unit, integration, and API tests; 80%+ coverage; pytest config.

### Phase IV

- Auth (User, JWT, roles), file upload, Application model and endpoints, Celery task and beat for expiring jobs.

### Stretch (Optional)

- Connection pooling, Redis cache, rate limiting, structured logging, Prometheus, email on application status, full-text search, API versioning, CI/CD, README/API docs.

## Current Status

- **Phase**: Phase I not started (implementation).
- **Blockers**: None.
- **Last updated**: Memory bank initiation.

## Known Issues

- None (no code deployed yet).
