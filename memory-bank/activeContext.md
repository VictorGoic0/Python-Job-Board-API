# Active Context: Job Board API

## Current Focus

- **Phase**: Phase I (Core Setup & Basic CRUD).
- **Immediate focus**: PR #2 complete (models, schemas, exceptions, error handlers, schema verification tests). Next is PR #3 (repositories, services, DI, blueprints, full CRUD).

## Recent Changes

- PR #2 completed: enums, Company/Job models (timezone-aware UTC via `app.utils.datetime_utils.utc_now`), company/job schemas (create/update/response), custom exceptions, global error handlers registered in `create_app`, `tests/unit/test_schemas.py` for schema validation and custom validators.
- `pytest.ini` added with `pythonpath = .` so `from app.*` works when running pytest from project root.
- README: added Tests section (where tests are, commands: `pytest`, `pytest tests/unit/ -v`, `pytest tests/unit/test_schemas.py -v`).

## Next Steps

1. PR #3: repositories (Company, Job), services with DI, blueprints (companies, jobs), Flask-Injector binding, full CRUD and validation.
2. When starting work: read `memory-bank/projectbrief.md` and `memory-bank/systemPatterns.md`; use `techContext.md` for setup and constraints.

## Active Decisions / Open Questions

- None. Follow PRD and Phase I tasks as source of truth.
