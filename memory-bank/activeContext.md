# Active Context: Job Board API

## Current Focus

- **Phase**: Phase I (Core Setup & Basic CRUD).
- **Immediate focus**: PR #3 complete (repositories, services, DI). PR #4 (routes/blueprints) reverted; next is PR #4: create `app/routes/companies.py`, `app/routes/jobs.py`, and register blueprints in `app/__init__.py`.

## Recent Changes

- PR #3 completed: CompanyRepository, JobRepository (SQLAlchemy 2 style); CompanyService, JobService (@inject, StaleDataError → OptimisticLockException); _configure_injector binds repositories and services as singletons. PR #4 (companies_blp, jobs_blp, blueprint registration) was reverted so only PR #3 scope remains.
- Root `context.md` added: one-file summary of PR #1–#4 state for new/fresh sessions.

## Next Steps

1. PR #4: Create companies and jobs blueprints (4.1, 4.2), register with api (4.3). See `tasks-phase1.md` § 4.1–4.3 and root `context.md`.
2. When starting work: read `memory-bank/projectbrief.md` and `memory-bank/systemPatterns.md`; use `techContext.md` for setup; use root `context.md` for PR-by-PR state.

## Active Decisions / Open Questions

- None. Follow PRD and Phase I tasks as source of truth.
