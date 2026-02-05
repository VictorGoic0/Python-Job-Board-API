# Active Context: Job Board API

## Current Focus

- **Phase**: Phase I (Core Setup & Basic CRUD).
- **Immediate focus**: PR #1 complete through 1.5 (migrations restructured to single initial schema + up/status/down). Task 1.6 (verification) documented; next is PR #2 (models, schemas, exceptions).

## Recent Changes

- Task 1.6 and docs updated: venv + pip install before migrations; migrations require venv (psycopg2). Docker app service serves on 5000 — do not run `flask run` locally when Docker app is up (address already in use). Use either Docker for the app or stop app container and run `flask run` locally.
- Root README added: setup (venv, deps, Docker, migrations), running app (Docker vs local), Swagger/RabbitMQ URLs.
- Migrations README: prerequisites (venv, pip install) before running migration commands.
- Docker: Postgres healthcheck uses `-d job_board`; Celery services under profile `celery` (not started by default).
- Migrations: single `001_initial_schema.sql` (+ `.down.sql`), runner with `up` / `status` / `down`, `schema_migrations` tracking.

## Next Steps

1. PR #2: models (enums, Company, Job), schemas, custom exceptions, error handlers.
2. PR #3: repositories, services, DI, blueprints (companies, jobs), full CRUD.
3. When starting work: read `memory-bank/projectbrief.md` and `memory-bank/systemPatterns.md`; use `techContext.md` for setup and constraints.

## Active Decisions / Open Questions

- None. Follow PRD and Phase I tasks as source of truth.
