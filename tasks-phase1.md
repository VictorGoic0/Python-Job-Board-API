# Phase 1 Task Files: Core Setup & Basic CRUD

## PR #1: Project Setup, Docker, and Database Configuration

**References**: Phase I - Project Setup, Docker Setup, Configuration, Database Migrations

**Dependencies**: None (first PR)

**Description**: Set up the foundational Flask project structure with Docker containers for PostgreSQL and RabbitMQ, configure the application, and create the database migration system.

### Subtasks:

#### 1.1 Project Structure
- [x] Create root project directory `job-board-api/`
- [x] Create directory structure:
  - [x] `app/` (main application package)
  - [x] `app/models/`
  - [x] `app/schemas/`
  - [x] `app/repositories/`
  - [x] `app/services/`
  - [x] `app/routes/`
  - [x] `app/exceptions/`
  - [x] `app/utils/`
  - [x] `migrations/`
  - [x] `tests/`
  - [x] `docker/`
- [x] Create all `__init__.py` files in Python packages

#### 1.2 Dependencies and Configuration
- [x] Create `requirements.txt` with all dependencies (Flask, SQLAlchemy, Marshmallow, etc.)
- [x] Create `config.py` with Config classes (Development, Testing, Production)
- [x] Create `.env.example` file with environment variable templates
- [x] Create `.gitignore` file (Python, venv, Docker, IDE files)
- [x] Create `run_server.py` as application entry point

#### 1.3 Docker Configuration
- [x] Create `docker/Dockerfile` with Python 3.11 base image
- [x] Add PostgreSQL client installation to Dockerfile
- [x] Configure dependency caching layer in Dockerfile
- [x] Create `docker-compose.yml` with services:
  - [x] PostgreSQL service with health check
  - [x] RabbitMQ service with management UI
  - [x] Flask app service with volume mounts
  - [x] Celery worker service (placeholder for Phase IV)
  - [x] Celery beat service (placeholder for Phase IV)
- [x] Configure service dependencies and health checks
- [x] Set up named volumes for PostgreSQL data persistence

#### 1.4 Flask Application Factory
- [x] Create `app/extensions.py` to initialize Flask extensions (db, ma, api)
- [x] Create `app/__init__.py` with `create_app()` factory function
- [x] Initialize SQLAlchemy in factory
- [x] Initialize Marshmallow in factory
- [x] Initialize Flask-SMOREST API in factory
- [x] Configure CORS
- [x] Set up Flask-Injector placeholder (will configure in PR #3)

#### 1.5 Database Migrations
- [x] Create `migrations/001_create_company_table.sql` with Company table schema
- [x] Create `migrations/002_create_job_table.sql` with Job table schema and indexes
- [x] Create `migrations/run_migrations.py` script:
  - [x] Parse DATABASE_URL from environment
  - [x] Connect to PostgreSQL
  - [x] Find and sort all .sql files
  - [x] Execute each migration in order
  - [x] Add error handling and rollback
  - [x] Add success/failure logging

#### 1.6 Testing and Verification
- [x] Create venv and install dependencies: `python3 -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`
- [x] Start Docker Compose (postgres, rabbitmq, app): `docker-compose up -d`
- [x] Verify PostgreSQL is running and accessible
- [x] Verify RabbitMQ is running (management UI at http://localhost:15672)
- [x] Run migrations locally (venv active, DATABASE_URL pointing at Postgres): `python migrations/run_migrations.py up`
- [x] Verify tables created in PostgreSQL (e.g. `schema_migrations`, `company`, `job`)
- [x] Verify Flask app: when Docker app service is running, the app is already served on port 5000 — do **not** run `flask run` locally or you get "address already in use". Use Docker for the app, or stop the app container and run `FLASK_APP=run_server flask run` locally.
- [x] Access Swagger UI at http://localhost:5000/swagger

---

## PR #2: Models, Schemas, and Exception Handling

**References**: Phase I - Entity Models, Marshmallow Schemas (DTOs), Exception Handling

**Dependencies**: PR #1 must be completed

**Description**: Create SQLAlchemy models for Company and Job entities, define Marshmallow schemas for validation and serialization, and implement custom exception handling.

### Subtasks:

#### 2.1 Enums
- [x] Create `app/models/enums.py`
- [x] Define `JobType` enum (FULL_TIME, PART_TIME, CONTRACT, INTERNSHIP)
- [x] Define `ExperienceLevel` enum (ENTRY, MID, SENIOR)
- [x] Define `RemoteOption` enum (REMOTE, HYBRID, ONSITE)

#### 2.2 Company Model
- [x] Create `app/models/company.py`
- [x] Define `Company` SQLAlchemy model with fields:
  - [x] id (BigInteger, primary key)
  - [x] name (String, required)
  - [x] description (Text, optional)
  - [x] website (String, optional)
  - [x] location (String, required)
  - [x] created_at (DateTime, auto-generated)
  - [x] updated_at (DateTime, auto-updated)
  - [x] version (Integer, for optimistic locking)
- [x] Add relationship to Job model (one-to-many with cascade delete)
- [x] Add `__repr__` method

#### 2.3 Job Model
- [x] Create `app/models/job.py`
- [x] Define `Job` SQLAlchemy model with fields:
  - [x] id (BigInteger, primary key)
  - [x] title (String, required)
  - [x] description (Text, required)
  - [x] company_id (BigInteger, foreign key)
  - [x] location (String, required)
  - [x] salary_min (Numeric, optional)
  - [x] salary_max (Numeric, optional)
  - [x] job_type (Enum, required)
  - [x] experience_level (Enum, required)
  - [x] remote_option (Enum, required)
  - [x] posted_date (DateTime, auto-generated)
  - [x] expiry_date (DateTime, optional)
  - [x] is_active (Boolean, default True)
  - [x] application_url (String, optional)
  - [x] created_at (DateTime, auto-generated)
  - [x] updated_at (DateTime, auto-updated)
  - [x] version (Integer, for optimistic locking)
- [x] Add relationship to Company model (many-to-one)
- [x] Add `__repr__` method

#### 2.4 Company Schemas
- [x] Create `app/schemas/company_schema.py`
- [x] Define `CompanySummarySchema` (minimal company info for embedding)
- [x] Define `CompanySchema` (full company details)
- [x] Define `CompanyCreateSchema` with validation:
  - [x] name (required, length 1-255)
  - [x] description (optional)
  - [x] website (optional, must be valid URL)
  - [x] location (required, length 1-255)
- [x] Define `CompanyUpdateSchema` (all fields optional for PATCH)

#### 2.5 Job Schemas
- [x] Create `app/schemas/job_schema.py`
- [x] Define `JobSchema` (for list responses with embedded company)
- [x] Define `JobDetailSchema` (extends JobSchema with full details)
- [x] Define `JobCreateSchema` with validation:
  - [x] All required fields with proper validators
  - [x] Salary validation (min >= 0, max >= 0)
  - [x] Enum validation for job_type, experience_level, remote_option
  - [x] URL validation for application_url
  - [x] Custom validator: salary_max >= salary_min
  - [x] Custom validator: expiry_date must be in future
- [x] Define `JobUpdateSchema` (all fields optional for PATCH)
  - [x] Include same custom validators

#### 2.6 Custom Exceptions
- [x] Create `app/exceptions/custom_exceptions.py`
- [x] Define `JobNotFoundException` with job_id parameter
- [x] Define `CompanyNotFoundException` with company_id parameter
- [x] Define `OptimisticLockException`
- [x] Define `AuthenticationException` (for Phase IV)
- [x] Define `InvalidFileException` (for Phase IV)

#### 2.7 Global Error Handlers
- [x] Create `app/utils/error_handlers.py`
- [x] Define `register_error_handlers(app)` function
- [x] Add handler for `JobNotFoundException` → 404
- [x] Add handler for `CompanyNotFoundException` → 404
- [x] Add handler for `ValidationError` (Marshmallow) → 400 with field errors
- [x] Add handler for `OptimisticLockException` → 409
- [x] Add handler for `StaleDataError` (SQLAlchemy) → 409
- [x] Add handler for generic `Exception` → 500
- [x] Register error handlers in `app/__init__.py`

#### 2.8 Testing and Verification
- [x] Import models in Python shell to verify no syntax errors
- [x] Verify SQLAlchemy can introspect models
- [x] Test schema validation with valid data
- [x] Test schema validation with invalid data (should raise ValidationError)
- [x] Verify custom validators work (salary range, expiry date)

---

## PR #3: Repository Layer and Service Layer

**References**: Phase I - Repository Layer, Service Layer

**Dependencies**: PR #2 must be completed

**Description**: Implement the repository pattern for database operations and business logic services with dependency injection.

### Subtasks:

#### 3.1 Company Repository
- [x] Create `app/repositories/company_repository.py`
- [x] Define `CompanyRepository` class
- [x] Implement `find_all()` → returns all companies
- [x] Implement `find_by_id(company_id)` → returns company or None
- [x] Implement `find_by_name(name)` → returns company or None
- [x] Implement `save(company)` → saves and returns company (handles create/update)
- [x] Implement `delete(company)` → deletes company

#### 3.2 Job Repository
- [x] Create `app/repositories/job_repository.py`
- [x] Define `JobRepository` class
- [x] Implement `find_all()` → returns all jobs with company data (use joinedload)
- [x] Implement `find_by_id(job_id)` → returns job with company or None (use joinedload)
- [x] Implement `find_by_company_id(company_id)` → returns jobs for a company
- [x] Implement `save(job)` → saves and returns job
- [x] Implement `delete(job)` → deletes job

#### 3.3 Company Service
- [x] Create `app/services/company_service.py`
- [x] Define `CompanyService` class with `@inject` decorator
- [x] Inject `CompanyRepository` in constructor
- [x] Implement `get_all_companies()` → List[Company]
- [x] Implement `get_company_by_id(company_id)` → Company (raises CompanyNotFoundException if not found)
- [x] Implement `create_company(data: dict)` → Company
  - [x] Create Company instance from data
  - [x] Save via repository
  - [x] Return created company
- [x] Implement `update_company(company_id, data: dict)` → Company
  - [x] Fetch existing company
  - [x] Update only provided fields
  - [x] Handle optimistic locking (catch StaleDataError)
  - [x] Return updated company
- [x] Implement `delete_company(company_id)` → None
  - [x] Fetch company
  - [x] Delete via repository

#### 3.4 Job Service
- [x] Create `app/services/job_service.py`
- [x] Define `JobService` class with `@inject` decorator
- [x] Inject `JobRepository` and `CompanyRepository` in constructor
- [x] Implement `get_all_jobs()` → List[Job]
- [x] Implement `get_job_by_id(job_id)` → Job (raises JobNotFoundException if not found)
- [x] Implement `create_job(data: dict)` → Job
  - [x] Validate company exists (raise CompanyNotFoundException if not)
  - [x] Convert string enums to enum types
  - [x] Create Job instance
  - [x] Set posted_date to current UTC time
  - [x] Save via repository
  - [x] Return created job
- [x] Implement `update_job(job_id, data: dict)` → Job
  - [x] Fetch existing job
  - [x] Validate new company_id if provided
  - [x] Convert string enums to enum types
  - [x] Update only provided fields
  - [x] Handle optimistic locking
  - [x] Return updated job
- [x] Implement `delete_job(job_id)` → None
  - [x] Fetch job
  - [x] Delete via repository

#### 3.5 Dependency Injection Configuration
- [x] Update `app/__init__.py`
- [x] Create `configure_injector(app)` function
- [x] Configure injector bindings:
  - [x] JobRepository → singleton
  - [x] CompanyRepository → singleton
  - [x] JobService → singleton
  - [x] CompanyService → singleton
- [x] Call `FlaskInjector(app=app, modules=[configure])`

#### 3.6 Testing and Verification
- [x] Test repository methods directly in Python shell
- [x] Create test company via repository
- [x] Create test job via repository with company_id
- [x] Verify foreign key constraint works (cascade delete)
- [x] Test service methods in Python shell
- [x] Verify CompanyNotFoundException is raised for invalid ID
- [x] Verify JobNotFoundException is raised for invalid ID

---

## PR #4: Controller Layer (Routes/Blueprints)

**References**: Phase I - Controller Layer, API Endpoints

**Dependencies**: PR #3 must be completed

**Description**: Implement Flask-SMOREST blueprints for Company and Job CRUD endpoints with proper HTTP methods and status codes.

**Decisions** (documented for consistency):
- **Company list response**: Use `CompanySchema(many=True)` for both list and single company (same schema; typical convention).
- **Blueprint URL prefix**: Use full path so routes are under `/api/` — `url_prefix='/api/companies'` and `url_prefix='/api/jobs'` (PRD § Controller Layer and endpoint list; `Api()` in extensions has no extra prefix).

### Subtasks:

#### 4.1 Company Routes
- [x] Create `app/routes/companies.py`
- [x] Create `companies_blp` Blueprint with url_prefix='/api/companies'
- [x] Define `CompanyList` MethodView class
  - [x] Inject `CompanyService`
  - [x] Implement `get()` method:
    - [x] Call service.get_all_companies()
    - [x] Return with 200 status
    - [x] Use `@companies_blp.response(200, CompanySchema(many=True))`
  - [x] Implement `post()` method:
    - [x] Use `@companies_blp.arguments(CompanyCreateSchema)`
    - [x] Call service.create_company(data)
    - [x] Return with 201 status
    - [x] Use `@companies_blp.response(201, CompanySchema)`
- [x] Define `CompanyDetail` MethodView class
  - [x] Inject `CompanyService`
  - [x] Implement `get(company_id)` method:
    - [x] Call service.get_company_by_id(company_id)
    - [x] Return with 200 status
  - [x] Implement `patch(company_data, company_id)` method:
    - [x] Use `@companies_blp.arguments(CompanyUpdateSchema)`
    - [x] Call service.update_company(company_id, data)
    - [x] Return with 200 status
  - [x] Implement `delete(company_id)` method:
    - [x] Call service.delete_company(company_id)
    - [x] Return empty string with 204 status
- [x] Register routes with blueprint decorators

#### 4.2 Job Routes
- [x] Create `app/routes/jobs.py`
- [x] Create `jobs_blp` Blueprint with url_prefix='/api/jobs'
- [x] Define `JobList` MethodView class
  - [x] Inject `JobService`
  - [x] Implement `get()` method:
    - [x] Call service.get_all_jobs()
    - [x] Return with 200 status
    - [x] Use `@jobs_blp.response(200, JobSchema(many=True))`
  - [x] Implement `post()` method:
    - [x] Use `@jobs_blp.arguments(JobCreateSchema)`
    - [x] Call service.create_job(data)
    - [x] Return with 201 status
    - [x] Use `@jobs_blp.response(201, JobSchema)`
- [x] Define `JobDetail` MethodView class
  - [x] Inject `JobService`
  - [x] Implement `get(job_id)` method:
    - [x] Call service.get_job_by_id(job_id)
    - [x] Return with 200 status
    - [x] Use `@jobs_blp.response(200, JobDetailSchema)`
  - [x] Implement `patch(job_data, job_id)` method:
    - [x] Use `@jobs_blp.arguments(JobUpdateSchema)`
    - [x] Call service.update_job(job_id, data)
    - [x] Return with 200 status
  - [x] Implement `delete(job_id)` method:
    - [x] Call service.delete_job(job_id)
    - [x] Return empty string with 204 status
- [x] Register routes with blueprint decorators

#### 4.3 Blueprint Registration
- [x] Update `app/__init__.py`
- [x] Import `jobs_blp` from app.routes.jobs
- [x] Import `companies_blp` from app.routes.companies
- [x] Register jobs blueprint with api: `api.register_blueprint(jobs_blp)`
- [x] Register companies blueprint with api: `api.register_blueprint(companies_blp)`

#### 4.4 Manual Testing with curl/Postman
- [x] Start the Flask application
- [x] Test Company endpoints:
  - [x] POST /api/companies (create company)
  - [x] GET /api/companies (list all companies)
  - [x] GET /api/companies/{id} (get specific company)
  - [x] PATCH /api/companies/{id} (update company)
  - [x] DELETE /api/companies/{id} (delete company)
- [x] Test Job endpoints:
  - [x] POST /api/jobs (create job with valid company_id)
  - [x] GET /api/jobs (list all jobs with company data)
  - [x] GET /api/jobs/{id} (get specific job with full details)
  - [x] PATCH /api/jobs/{id} (update job)
  - [x] DELETE /api/jobs/{id} (delete job)
- [x] Test error cases:
  - [x] POST with missing required fields → 400 with validation errors
  - [x] GET with non-existent ID → 404
  - [x] POST job with invalid company_id → 404 CompanyNotFoundException
  - [x] PATCH with invalid data → 400
- [x] Verify Swagger UI shows all endpoints at /swagger

#### 4.5 Test Optimistic Locking
- [ ] Create a job via API
- [ ] In database, manually update the version number
- [ ] Try to update the job via API
- [ ] Verify 409 Conflict response is returned

**Note (current state):** Optimistic locking is **not yet implemented**. The `version` column exists on `company` and `job`, and the app has error handlers for `StaleDataError` → 409, but the ORM/repository does **not** use `version` in the UPDATE (no `version_id_col` or `WHERE version = ?`). So PATCH succeeds even when the DB row’s version was changed; 409 will not occur until we add version checking (e.g. SQLAlchemy `version_id_col` or an explicit version check in the repository). 4.5 verification is deferred until that is implemented.

---

## PR #5: Phase I Testing Suite

**References**: Phase I - Acceptance Criteria, Phase III - Testing

**Dependencies**: PR #4 must be completed

**Description**: Create comprehensive test suite for Phase I functionality including unit tests for services, integration tests for repositories, and API tests for routes.

### Subtasks:

#### 5.1 Test Configuration
- [x] Create `pytest.ini` with configuration:
  - [x] testpaths = tests
  - [x] python_files = test_*.py
  - [x] coverage settings (--cov=app, --cov-fail-under=80)
- [x] Create `tests/conftest.py`
- [x] Define `app` fixture (session scope, testing config)
- [x] Define `client` fixture (function scope, test client)
- [x] Define `db_session` fixture (function scope, clean database)
- [x] Define `sample_company` fixture (creates test company)
- [x] Define `sample_job` fixture (creates test job with sample_company)

#### 5.2 Unit Tests - Company Service
- [x] Create `tests/unit/test_company_service.py`
- [x] Set up mock repositories in setup_method
- [x] Test `get_all_companies()` returns list
- [x] Test `get_company_by_id()` with existing company
- [x] Test `get_company_by_id()` raises CompanyNotFoundException
- [x] Test `create_company()` with valid data
- [x] Test `update_company()` updates only provided fields
- [x] Test `update_company()` raises CompanyNotFoundException
- [x] Test `delete_company()` calls repository delete
- [x] Test `delete_company()` raises CompanyNotFoundException

#### 5.3 Unit Tests - Job Service
- [x] Create `tests/unit/test_job_service.py`
- [x] Set up mock repositories in setup_method
- [x] Test `get_all_jobs()` returns list
- [x] Test `get_job_by_id()` with existing job
- [x] Test `get_job_by_id()` raises JobNotFoundException
- [x] Test `create_job()` with valid data
- [x] Test `create_job()` raises CompanyNotFoundException for invalid company_id
- [x] Test `update_job()` updates only provided fields
- [x] Test `update_job()` validates new company_id
- [x] Test `update_job()` raises JobNotFoundException
- [x] Test `delete_job()` calls repository delete
- [x] Test `delete_job()` raises JobNotFoundException

#### 5.4 Integration Tests - Company Repository
- [x] Create `tests/integration/test_company_repository.py`
- [x] Test `find_all()` returns all companies
- [x] Test `find_by_id()` returns company when exists
- [x] Test `find_by_id()` returns None when not exists
- [x] Test `find_by_name()` returns company
- [x] Test `save()` creates new company
- [x] Test `save()` updates existing company
- [x] Test `delete()` removes company from database
- [x] Test cascade delete (deleting company deletes associated jobs)

#### 5.5 Integration Tests - Job Repository
- [x] Create `tests/integration/test_job_repository.py`
- [x] Test `find_all()` returns all jobs with company data
- [x] Test `find_by_id()` returns job with company when exists
- [x] Test `find_by_id()` returns None when not exists
- [x] Test `find_by_company_id()` returns jobs for specific company
- [x] Test `save()` creates new job
- [x] Test `save()` updates existing job
- [x] Test `delete()` removes job from database
- [x] Test foreign key constraint (cannot create job with invalid company_id)

#### 5.6 API Tests - Company Routes
- [x] Create `tests/api/test_company_routes.py`
- [x] Test GET /api/companies returns 200 and list
- [x] Test GET /api/companies/{id} returns 200 and company data
- [x] Test GET /api/companies/{invalid_id} returns 404
- [x] Test POST /api/companies with valid data returns 201
- [x] Test POST /api/companies with invalid data returns 400
- [x] Test POST /api/companies with missing fields returns 400
- [x] Test PATCH /api/companies/{id} with valid data returns 200
- [x] Test PATCH /api/companies/{id} updates only provided fields
- [x] Test PATCH /api/companies/{invalid_id} returns 404
- [x] Test DELETE /api/companies/{id} returns 204
- [x] Test DELETE /api/companies/{invalid_id} returns 404

#### 5.7 API Tests - Job Routes
- [x] Create `tests/api/test_job_routes.py`
- [x] Test GET /api/jobs returns 200 and list with company data
- [x] Test GET /api/jobs/{id} returns 200 and full job details
- [x] Test GET /api/jobs/{invalid_id} returns 404
- [x] Test POST /api/jobs with valid data returns 201
- [x] Test POST /api/jobs with invalid company_id returns 404
- [x] Test POST /api/jobs with missing required fields returns 400
- [x] Test POST /api/jobs with invalid enum values returns 400
- [x] Test POST /api/jobs with salary_max < salary_min returns 400
- [x] Test POST /api/jobs with past expiry_date returns 400
- [x] Test PATCH /api/jobs/{id} with valid data returns 200
- [x] Test PATCH /api/jobs/{id} updates only provided fields
- [x] Test PATCH /api/jobs/{invalid_id} returns 404
- [x] Test DELETE /api/jobs/{id} returns 204
- [x] Test DELETE /api/jobs/{invalid_id} returns 404

#### 5.8 Run Tests and Fix Issues
- [x] Run all tests: `pytest` (without test DB: 25 pass, 41 skipped; with `job_board_test`: all 66 run)
- [x] Verify all tests pass (no errors; skips only when DB unavailable — see README for creating `job_board_test`)
- [ ] Run with coverage: `pytest` (addopts in pytest.ini); full coverage ≥80% requires test DB
- [ ] Verify coverage is >= 80% (run after creating `job_board_test`)
- [ ] Review coverage report and add tests for uncovered code (if below 80%)
- [x] Fix any failing tests (conftest updated to skip integration/API when DB unavailable)
- [ ] Commit test suite

#### 5.9 Phase I Acceptance Criteria Verification
- [ ] Docker Compose successfully starts PostgreSQL, RabbitMQ, and Flask app
- [ ] Flask application connects to database
- [ ] All 5 CRUD endpoints work for both Job and Company
- [ ] GET /api/jobs returns jobs with joined company data
- [ ] GET /api/jobs/{id} returns full job details with company
- [ ] POST creates job with valid company_id foreign key
- [ ] PATCH updates only provided fields
- [ ] DELETE removes job from database
- [ ] Validation errors return 400 with field-specific messages
- [ ] Not found errors return 404 with clear message
- [ ] Concurrent updates properly handled with 409 response
- [ ] Unknown errors return 500 with generic message
- [ ] Database relationships enforce referential integrity
- [ ] Timestamps (created_at, updated_at) auto-populate
- [ ] Swagger UI accessible at /swagger

---

## Phase I Completion Checklist

- [ ] All 5 PRs completed and merged
- [ ] Application runs successfully with `docker-compose up`
- [ ] All tests pass with >= 80% coverage
- [ ] Manual testing of all endpoints successful
- [ ] Swagger documentation accessible and accurate
- [ ] README.md updated with setup instructions
- [ ] Ready to proceed to Phase II
