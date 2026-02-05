# Active Context: Job Board API

## Current Focus

- **Phase**: Phase I (Core Setup & Basic CRUD).
- **Immediate focus**: PR #5 — Phase I testing suite. Tasks 5.1–5.7 are **done** (test config, unit tests for services, integration tests for repositories, API tests for company/job routes). Remaining: 5.8 (run all tests, fix issues, coverage), 5.9 (Phase I acceptance verification). These are collaborative/manual.

## Recent Changes

- PR #5: Implemented 5.1 (pytest.ini + conftest with app, client, db_session, sample_company, sample_job); 5.2–5.3 (unit tests for CompanyService, JobService with mocked repos); 5.4–5.5 (integration tests for CompanyRepository, JobRepository with real DB); 5.6–5.7 (API tests for company and job routes). Test DB (job_board_test) is **not** auto-created; user will create it after PRs. Root `context.md` created for new Cursor sessions.

## Next Steps

1. PR #5 remaining: 5.8 (run `pytest`, verify pass, coverage ≥80%, fix failures); 5.9 (Phase I acceptance checklist). Then Phase I completion checklist.
2. When starting work: read `memory-bank/projectbrief.md`, `memory-bank/systemPatterns.md`; use root `context.md` for PR/test setup summary.

## Active Decisions / Open Questions

- None. Follow PRD and Phase I tasks as source of truth.
