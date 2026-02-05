# Project Context (for new Cursor window/session)

One-file summary so work can continue without re-reading the whole repo. See `memory-bank/` for full docs; `tasks-phase1.md` for the canonical task checklist.

---

## PR status (Phase I)

| PR | Scope | Status |
|----|--------|--------|
| **#1** | Project setup, Docker, migrations, app factory | **DONE** |
| **#2** | Models, schemas, exceptions, error handlers | **DONE** |
| **#3** | Repositories, services, DI (no routes) | **DONE** |
| **#4** | Controller layer (companies + jobs blueprints) | **DONE** (4.4 manual testing done; 4.5 optimistic locking deferred) |
| **#5** | Phase I testing suite | **In progress**: 5.1–5.7 done; 5.8–5.9 collaborative |

---

## Current PR: #5 (Testing) — details for new session

**What’s done (5.1–5.7)**  
- **5.1** Test config: `pytest.ini` (testpaths=tests, `--cov=app --cov-report=term-missing --cov-fail-under=80`). `tests/conftest.py` with session-scoped `app` (testing config, `db.create_all()` in app context), function-scoped `client`, `db_session` (truncates `job` then `company` before each test), `sample_company`, `sample_job` (depend on `db_session`).  
- **5.2–5.3** Unit tests: `tests/unit/test_company_service.py`, `test_job_service.py`. Repositories are **mocked** (MagicMock); services instantiated with `CompanyService(company_repository=mock)` / `JobService(job_repository=..., company_repository=...)`. No DB.  
- **5.4–5.5** Integration tests: `tests/integration/test_company_repository.py`, `test_job_repository.py`. Use **real DB** (TestingConfig → `job_board_test`). Each test runs inside `app.app_context()`; `db_session` fixture truncates tables so each test sees a clean DB. Repo fixtures yield `CompanyRepository()` / `JobRepository()` under app context.  
- **5.6–5.7** API tests: `tests/api/test_company_routes.py`, `test_job_routes.py`. Use `client` (Flask test client) and `db_session` / `sample_company` / `sample_job` where needed. Hit `/api/companies/`, `/api/jobs/` (with trailing slash). Assert status codes and JSON; no DB if you only run unit tests.

**What’s left (collaborative)**  
- **5.8** Run all tests (`pytest`), fix failures, run with coverage, verify ≥80%, commit.  
- **5.9** Phase I acceptance verification (Docker up, CRUD, errors, Swagger, etc. — checklist in tasks-phase1.md).

**Important for tests (new window)**  
1. **Test DB**  
   - Integration and API tests expect PostgreSQL with a database named **job_board_test** (same user/password as in `config.TestingConfig`: admin/admin123 by default).  
   - The project does **not** auto-create this DB. Create it manually (e.g. `CREATE DATABASE job_board_test;`) when you want integration/API tests to run.  
   - Schema: session-scoped `app` fixture calls `db.create_all()` once, so tables exist when any test that needs the DB runs.

2. **What needs DB vs not**  
   - **No DB**: `pytest tests/unit/` (schemas, company service, job service).  
   - **DB required**: `tests/integration/`, `tests/api/`. Run with `pytest tests/integration/ tests/api/` (or full `pytest`) when `job_board_test` exists and Postgres is up.

3. **Running tests**  
   - Activate venv: `source venv/bin/activate` (WSL/Linux).  
   - All tests: `pytest` or `pytest -v`.  
   - Unit only (no DB): `pytest tests/unit/ -v`.  
   - With coverage: `pytest` (addopts in pytest.ini); skip coverage: `pytest --no-cov`.

4. **Conftest flow**  
   - `app` (session): `create_app("testing")`, then `db.create_all()` in app context.  
   - `db_session` (function): inside app context, `TRUNCATE job, company RESTART IDENTITY CASCADE`, commit, yield `db.session`. So every test that uses `db_session` starts with empty company/job tables.  
   - API tests use `client` and often request `sample_company` / `sample_job`, which insert one company and one job; routes are tested against that data.

5. **Routes**  
   - Companies: `/api/companies/` (list/create), `/api/companies/<id>` (get/patch/delete).  
   - Jobs: `/api/jobs/`, `/api/jobs/<id>`.  
   - Services are constructor-injected into MethodView classes (Flask-Injector); not method-injected.

---

## Quick reference

| Item | Location / Command |
|------|--------------------|
| Task checklist | `tasks-phase1.md` |
| Scope & phases | `memory-bank/projectbrief.md` |
| Architecture | `memory-bank/systemPatterns.md` |
| Setup & stack | `memory-bank/techContext.md` |
| Migrations | `migrations/README.md`; `python migrations/run_migrations.py up` |
| Tests (no DB) | `pytest tests/unit/ -v` |
| Tests (with DB) | Create `job_board_test`, then `pytest` or `pytest tests/integration/ tests/api/` |
| App entry | `run_server.py`; Docker app on 5000 or `FLASK_APP=run_server flask run` |
| Swagger | http://localhost:5000/swagger |

---

## Optimistic locking (4.5)

`version` column exists on company and job; 409 handlers exist. The ORM does **not** use `version` in UPDATEs yet (no `version_id_col`). So PATCH does not return 409 when the row was changed elsewhere. 4.5 verification is deferred until version checking is implemented.
