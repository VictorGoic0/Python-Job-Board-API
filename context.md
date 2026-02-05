# Project Context (for new/fresh sessions)

One-file summary of recent PR context so work can continue seamlessly. See `memory-bank/` for full docs; `tasks-phase1.md` for the canonical task checklist.

---

## PR #1: Project Setup, Docker, Database — **DONE**

- **Scope**: Structure, config, Docker, migrations, app factory.
- **Delivered**: `app/` layout with `models/`, `schemas/`, `repositories/`, `services/`, `routes/`, `exceptions/`, `utils/`; `requirements.txt`, `config.py`, `.env.example`, `.gitignore`, `run_server.py`; `docker/Dockerfile`, `docker-compose.yml` (postgres, rabbitmq, app; celery under profile `celery`); `app/extensions.py` (db, ma, api), `create_app()` with CORS and Flask-Injector placeholder; migrations: `001_initial_schema.sql` + `.down.sql`, `run_migrations.py` with `up` / `status` / `down`, `schema_migrations` table.
- **Conventions**: Venv + `pip install -r requirements.txt` before migrations. Docker app binds 5000 — don’t run `flask run` locally when app container is up. Migrations: `python migrations/run_migrations.py up` (venv active, Postgres running).

---

## PR #2: Models, Schemas, Exceptions — **DONE**

- **Scope**: SQLAlchemy models, Marshmallow schemas, custom exceptions, error handlers.
- **Delivered**: `app/models/enums.py` (JobType, ExperienceLevel, RemoteOption); `app/models/company.py`, `app/models/job.py` (timezone-aware UTC via `app.utils.datetime_utils.utc_now`); `app/schemas/company_schema.py` (CompanySummary, Company, CompanyCreate, CompanyUpdate); `app/schemas/job_schema.py` (JobSchema, JobDetailSchema, JobCreateSchema, JobUpdateSchema with salary/expiry validators); `app/exceptions/custom_exceptions.py`; `app/utils/error_handlers.py` registered in `create_app`; `tests/unit/test_schemas.py`; `pytest.ini` with `pythonpath = .`.
- **Conventions**: Models = persistence/domain; schemas = request validation + response serialization (used only in routes). Run tests: `pytest` or `pytest tests/unit/ -v` from project root with venv active.

---

## PR #3: Repositories, Services, DI — **DONE**

- **Scope**: Repository layer, service layer, dependency injection (no routes yet).
- **Delivered**: `app/repositories/company_repository.py` (find_all, find_by_id, find_by_name, save, delete — SQLAlchemy 2 style with `select()`); `app/repositories/job_repository.py` (find_all, find_by_id, find_by_company_id, save, delete — `joinedload(Job.company)`); `app/services/company_service.py` (CompanyService with @inject, CompanyRepository; get_all_companies, get_company_by_id, create_company, update_company with StaleDataError → OptimisticLockException, delete_company); `app/services/job_service.py` (JobService with @inject, JobRepository + CompanyRepository; get_all_jobs, get_job_by_id, create_job with company validation and enum conversion, update_job with company_id validation and StaleDataError handling, delete_job); `app/__init__.py` — `_configure_injector(app)` binds CompanyRepository, JobRepository, CompanyService, JobService as singletons. **No routes**: PR #4 (blueprints) was reverted; only services + injector are in place.
- **Conventions**: Repositories use `db.session.execute(select(...))`, `db.session.get(Model, id)`; services raise CompanyNotFoundException / JobNotFoundException / OptimisticLockException; error handlers map those to 404/409.

---

## PR #4: Controller Layer (Routes/Blueprints) — **NEXT**

- **Scope**: Flask-SMOREST blueprints for Company and Job CRUD, register with api.
- **Not yet done**: Create `app/routes/companies.py` (companies_blp, CompanyList get/post, CompanyDetail get/patch/delete, inject CompanyService); create `app/routes/jobs.py` (jobs_blp, JobList get/post, JobDetail get/patch/delete, inject JobService); in `app/__init__.py` import and `api.register_blueprint(companies_blp)`, `api.register_blueprint(jobs_blp)`.
- **Reference**: Full task list in `tasks-phase1.md` § 4.1, 4.2, 4.3; PRD controller layer and schema names (CompanySchema, JobSchema, JobDetailSchema, CompanyCreateSchema, JobCreateSchema, etc.).

---

## Quick reference

| Item | Location / Command |
|------|--------------------|
| Task checklist | `tasks-phase1.md` |
| Scope & phases | `memory-bank/projectbrief.md` |
| Architecture | `memory-bank/systemPatterns.md` |
| Setup & stack | `memory-bank/techContext.md` |
| Migrations | `migrations/README.md`; `python migrations/run_migrations.py up` |
| Tests | `tests/unit/`; `pytest` or `pytest tests/unit/ -v` (venv, from project root) |
| App entry | `run_server.py`; `FLASK_APP=run_server flask run` (or Docker app on 5000) |
| Swagger | http://localhost:5000/swagger (when app is running) |
