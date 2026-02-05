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
- [ ] Create venv and install dependencies: `python3 -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`
- [ ] Start Docker Compose (postgres, rabbitmq, app): `docker-compose up -d`
- [ ] Verify PostgreSQL is running and accessible
- [ ] Verify RabbitMQ is running (management UI at http://localhost:15672)
- [ ] Run migrations locally (venv active, DATABASE_URL pointing at Postgres): `python migrations/run_migrations.py up`
- [ ] Verify tables created in PostgreSQL (e.g. `schema_migrations`, `company`, `job`)
- [ ] Verify Flask app: when Docker app service is running, the app is already served on port 5000 — do **not** run `flask run` locally or you get "address already in use". Use Docker for the app, or stop the app container and run `FLASK_APP=run_server flask run` locally.
- [ ] Access Swagger UI at http://localhost:5000/swagger

---

## PR #2: Models, Schemas, and Exception Handling

**References**: Phase I - Entity Models, Marshmallow Schemas (DTOs), Exception Handling

**Dependencies**: PR #1 must be completed

**Description**: Create SQLAlchemy models for Company and Job entities, define Marshmallow schemas for validation and serialization, and implement custom exception handling.

### Subtasks:

#### 2.1 Enums
- [ ] Create `app/models/enums.py`
- [ ] Define `JobType` enum (FULL_TIME, PART_TIME, CONTRACT, INTERNSHIP)
- [ ] Define `ExperienceLevel` enum (ENTRY, MID, SENIOR)
- [ ] Define `RemoteOption` enum (REMOTE, HYBRID, ONSITE)

#### 2.2 Company Model
- [ ] Create `app/models/company.py`
- [ ] Define `Company` SQLAlchemy model with fields:
  - [ ] id (BigInteger, primary key)
  - [ ] name (String, required)
  - [ ] description (Text, optional)
  - [ ] website (String, optional)
  - [ ] location (String, required)
  - [ ] created_at (DateTime, auto-generated)
  - [ ] updated_at (DateTime, auto-updated)
  - [ ] version (Integer, for optimistic locking)
- [ ] Add relationship to Job model (one-to-many with cascade delete)
- [ ] Add `__repr__` method

#### 2.3 Job Model
- [ ] Create `app/models/job.py`
- [ ] Define `Job` SQLAlchemy model with fields:
  - [ ] id (BigInteger, primary key)
  - [ ] title (String, required)
  - [ ] description (Text, required)
  - [ ] company_id (BigInteger, foreign key)
  - [ ] location (String, required)
  - [ ] salary_min (Numeric, optional)
  - [ ] salary_max (Numeric, optional)
  - [ ] job_type (Enum, required)
  - [ ] experience_level (Enum, required)
  - [ ] remote_option (Enum, required)
  - [ ] posted_date (DateTime, auto-generated)
  - [ ] expiry_date (DateTime, optional)
  - [ ] is_active (Boolean, default True)
  - [ ] application_url (String, optional)
  - [ ] created_at (DateTime, auto-generated)
  - [ ] updated_at (DateTime, auto-updated)
  - [ ] version (Integer, for optimistic locking)
- [ ] Add relationship to Company model (many-to-one)
- [ ] Add `__repr__` method

#### 2.4 Company Schemas
- [ ] Create `app/schemas/company_schema.py`
- [ ] Define `CompanySummarySchema` (minimal company info for embedding)
- [ ] Define `CompanySchema` (full company details)
- [ ] Define `CompanyCreateSchema` with validation:
  - [ ] name (required, length 1-255)
  - [ ] description (optional)
  - [ ] website (optional, must be valid URL)
  - [ ] location (required, length 1-255)
- [ ] Define `CompanyUpdateSchema` (all fields optional for PATCH)

#### 2.5 Job Schemas
- [ ] Create `app/schemas/job_schema.py`
- [ ] Define `JobSchema` (for list responses with embedded company)
- [ ] Define `JobDetailSchema` (extends JobSchema with full details)
- [ ] Define `JobCreateSchema` with validation:
  - [ ] All required fields with proper validators
  - [ ] Salary validation (min >= 0, max >= 0)
  - [ ] Enum validation for job_type, experience_level, remote_option
  - [ ] URL validation for application_url
  - [ ] Custom validator: salary_max >= salary_min
  - [ ] Custom validator: expiry_date must be in future
- [ ] Define `JobUpdateSchema` (all fields optional for PATCH)
  - [ ] Include same custom validators

#### 2.6 Custom Exceptions
- [ ] Create `app/exceptions/custom_exceptions.py`
- [ ] Define `JobNotFoundException` with job_id parameter
- [ ] Define `CompanyNotFoundException` with company_id parameter
- [ ] Define `OptimisticLockException`
- [ ] Define `AuthenticationException` (for Phase IV)
- [ ] Define `InvalidFileException` (for Phase IV)

#### 2.7 Global Error Handlers
- [ ] Create `app/utils/error_handlers.py`
- [ ] Define `register_error_handlers(app)` function
- [ ] Add handler for `JobNotFoundException` → 404
- [ ] Add handler for `CompanyNotFoundException` → 404
- [ ] Add handler for `ValidationError` (Marshmallow) → 400 with field errors
- [ ] Add handler for `OptimisticLockException` → 409
- [ ] Add handler for `StaleDataError` (SQLAlchemy) → 409
- [ ] Add handler for generic `Exception` → 500
- [ ] Register error handlers in `app/__init__.py`

#### 2.8 Testing and Verification
- [ ] Import models in Python shell to verify no syntax errors
- [ ] Verify SQLAlchemy can introspect models
- [ ] Test schema validation with valid data
- [ ] Test schema validation with invalid data (should raise ValidationError)
- [ ] Verify custom validators work (salary range, expiry date)

---

## PR #3: Repository Layer and Service Layer

**References**: Phase I - Repository Layer, Service Layer

**Dependencies**: PR #2 must be completed

**Description**: Implement the repository pattern for database operations and business logic services with dependency injection.

### Subtasks:

#### 3.1 Company Repository
- [ ] Create `app/repositories/company_repository.py`
- [ ] Define `CompanyRepository` class
- [ ] Implement `find_all()` → returns all companies
- [ ] Implement `find_by_id(company_id)` → returns company or None
- [ ] Implement `find_by_name(name)` → returns company or None
- [ ] Implement `save(company)` → saves and returns company (handles create/update)
- [ ] Implement `delete(company)` → deletes company

#### 3.2 Job Repository
- [ ] Create `app/repositories/job_repository.py`
- [ ] Define `JobRepository` class
- [ ] Implement `find_all()` → returns all jobs with company data (use joinedload)
- [ ] Implement `find_by_id(job_id)` → returns job with company or None (use joinedload)
- [ ] Implement `find_by_company_id(company_id)` → returns jobs for a company
- [ ] Implement `save(job)` → saves and returns job
- [ ] Implement `delete(job)` → deletes job

#### 3.3 Company Service
- [ ] Create `app/services/company_service.py`
- [ ] Define `CompanyService` class with `@inject` decorator
- [ ] Inject `CompanyRepository` in constructor
- [ ] Implement `get_all_companies()` → List[Company]
- [ ] Implement `get_company_by_id(company_id)` → Company (raises CompanyNotFoundException if not found)
- [ ] Implement `create_company(data: dict)` → Company
  - [ ] Create Company instance from data
  - [ ] Save via repository
  - [ ] Return created company
- [ ] Implement `update_company(company_id, data: dict)` → Company
  - [ ] Fetch existing company
  - [ ] Update only provided fields
  - [ ] Handle optimistic locking (catch StaleDataError)
  - [ ] Return updated company
- [ ] Implement `delete_company(company_id)` → None
  - [ ] Fetch company
  - [ ] Delete via repository

#### 3.4 Job Service
- [ ] Create `app/services/job_service.py`
- [ ] Define `JobService` class with `@inject` decorator
- [ ] Inject `JobRepository` and `CompanyRepository` in constructor
- [ ] Implement `get_all_jobs()` → List[Job]
- [ ] Implement `get_job_by_id(job_id)` → Job (raises JobNotFoundException if not found)
- [ ] Implement `create_job(data: dict)` → Job
  - [ ] Validate company exists (raise CompanyNotFoundException if not)
  - [ ] Convert string enums to enum types
  - [ ] Create Job instance
  - [ ] Set posted_date to current UTC time
  - [ ] Save via repository
  - [ ] Return created job
- [ ] Implement `update_job(job_id, data: dict)` → Job
  - [ ] Fetch existing job
  - [ ] Validate new company_id if provided
  - [ ] Convert string enums to enum types
  - [ ] Update only provided fields
  - [ ] Handle optimistic locking
  - [ ] Return updated job
- [ ] Implement `delete_job(job_id)` → None
  - [ ] Fetch job
  - [ ] Delete via repository

#### 3.5 Dependency Injection Configuration
- [ ] Update `app/__init__.py`
- [ ] Create `configure_injector(app)` function
- [ ] Configure injector bindings:
  - [ ] JobRepository → singleton
  - [ ] CompanyRepository → singleton
  - [ ] JobService → singleton
  - [ ] CompanyService → singleton
- [ ] Call `FlaskInjector(app=app, modules=[configure])`

#### 3.6 Testing and Verification
- [ ] Test repository methods directly in Python shell
- [ ] Create test company via repository
- [ ] Create test job via repository with company_id
- [ ] Verify foreign key constraint works (cascade delete)
- [ ] Test service methods in Python shell
- [ ] Verify CompanyNotFoundException is raised for invalid ID
- [ ] Verify JobNotFoundException is raised for invalid ID

---

## PR #4: Controller Layer (Routes/Blueprints)

**References**: Phase I - Controller Layer, API Endpoints

**Dependencies**: PR #3 must be completed

**Description**: Implement Flask-SMOREST blueprints for Company and Job CRUD endpoints with proper HTTP methods and status codes.

### Subtasks:

#### 4.1 Company Routes
- [ ] Create `app/routes/companies.py`
- [ ] Create `companies_blp` Blueprint with url_prefix='/api/companies'
- [ ] Define `CompanyList` MethodView class
  - [ ] Inject `CompanyService`
  - [ ] Implement `get()` method:
    - [ ] Call service.get_all_companies()
    - [ ] Return with 200 status
    - [ ] Use `@companies_blp.response(200, CompanySchema(many=True))`
  - [ ] Implement `post()` method:
    - [ ] Use `@companies_blp.arguments(CompanyCreateSchema)`
    - [ ] Call service.create_company(data)
    - [ ] Return with 201 status
    - [ ] Use `@companies_blp.response(201, CompanySchema)`
- [ ] Define `CompanyDetail` MethodView class
  - [ ] Inject `CompanyService`
  - [ ] Implement `get(company_id)` method:
    - [ ] Call service.get_company_by_id(company_id)
    - [ ] Return with 200 status
  - [ ] Implement `patch(company_data, company_id)` method:
    - [ ] Use `@companies_blp.arguments(CompanyUpdateSchema)`
    - [ ] Call service.update_company(company_id, data)
    - [ ] Return with 200 status
  - [ ] Implement `delete(company_id)` method:
    - [ ] Call service.delete_company(company_id)
    - [ ] Return empty string with 204 status
- [ ] Register routes with blueprint decorators

#### 4.2 Job Routes
- [ ] Create `app/routes/jobs.py`
- [ ] Create `jobs_blp` Blueprint with url_prefix='/api/jobs'
- [ ] Define `JobList` MethodView class
  - [ ] Inject `JobService`
  - [ ] Implement `get()` method:
    - [ ] Call service.get_all_jobs()
    - [ ] Return with 200 status
    - [ ] Use `@jobs_blp.response(200, JobSchema(many=True))`
  - [ ] Implement `post()` method:
    - [ ] Use `@jobs_blp.arguments(JobCreateSchema)`
    - [ ] Call service.create_job(data)
    - [ ] Return with 201 status
    - [ ] Use `@jobs_blp.response(201, JobSchema)`
- [ ] Define `JobDetail` MethodView class
  - [ ] Inject `JobService`
  - [ ] Implement `get(job_id)` method:
    - [ ] Call service.get_job_by_id(job_id)
    - [ ] Return with 200 status
    - [ ] Use `@jobs_blp.response(200, JobDetailSchema)`
  - [ ] Implement `patch(job_data, job_id)` method:
    - [ ] Use `@jobs_blp.arguments(JobUpdateSchema)`
    - [ ] Call service.update_job(job_id, data)
    - [ ] Return with 200 status
  - [ ] Implement `delete(job_id)` method:
    - [ ] Call service.delete_job(job_id)
    - [ ] Return empty string with 204 status
- [ ] Register routes with blueprint decorators

#### 4.3 Blueprint Registration
- [ ] Update `app/__init__.py`
- [ ] Import `jobs_blp` from app.routes.jobs
- [ ] Import `companies_blp` from app.routes.companies
- [ ] Register jobs blueprint with api: `api.register_blueprint(jobs_blp)`
- [ ] Register companies blueprint with api: `api.register_blueprint(companies_blp)`

#### 4.4 Manual Testing with curl/Postman
- [ ] Start the Flask application
- [ ] Test Company endpoints:
  - [ ] POST /api/companies (create company)
  - [ ] GET /api/companies (list all companies)
  - [ ] GET /api/companies/{id} (get specific company)
  - [ ] PATCH /api/companies/{id} (update company)
  - [ ] DELETE /api/companies/{id} (delete company)
- [ ] Test Job endpoints:
  - [ ] POST /api/jobs (create job with valid company_id)
  - [ ] GET /api/jobs (list all jobs with company data)
  - [ ] GET /api/jobs/{id} (get specific job with full details)
  - [ ] PATCH /api/jobs/{id} (update job)
  - [ ] DELETE /api/jobs/{id} (delete job)
- [ ] Test error cases:
  - [ ] POST with missing required fields → 400 with validation errors
  - [ ] GET with non-existent ID → 404
  - [ ] POST job with invalid company_id → 404 CompanyNotFoundException
  - [ ] PATCH with invalid data → 400
- [ ] Verify Swagger UI shows all endpoints at /swagger

#### 4.5 Test Optimistic Locking
- [ ] Create a job via API
- [ ] In database, manually update the version number
- [ ] Try to update the job via API
- [ ] Verify 409 Conflict response is returned

---

## PR #5: Phase I Testing Suite

**References**: Phase I - Acceptance Criteria, Phase III - Testing

**Dependencies**: PR #4 must be completed

**Description**: Create comprehensive test suite for Phase I functionality including unit tests for services, integration tests for repositories, and API tests for routes.

### Subtasks:

#### 5.1 Test Configuration
- [ ] Create `pytest.ini` with configuration:
  - [ ] testpaths = tests
  - [ ] python_files = test_*.py
  - [ ] coverage settings (--cov=app, --cov-fail-under=80)
- [ ] Create `tests/conftest.py`
- [ ] Define `app` fixture (session scope, testing config)
- [ ] Define `client` fixture (function scope, test client)
- [ ] Define `db_session` fixture (function scope, clean database)
- [ ] Define `sample_company` fixture (creates test company)
- [ ] Define `sample_job` fixture (creates test job with sample_company)

#### 5.2 Unit Tests - Company Service
- [ ] Create `tests/unit/test_company_service.py`
- [ ] Set up mock repositories in setup_method
- [ ] Test `get_all_companies()` returns list
- [ ] Test `get_company_by_id()` with existing company
- [ ] Test `get_company_by_id()` raises CompanyNotFoundException
- [ ] Test `create_company()` with valid data
- [ ] Test `update_company()` updates only provided fields
- [ ] Test `update_company()` raises CompanyNotFoundException
- [ ] Test `delete_company()` calls repository delete
- [ ] Test `delete_company()` raises CompanyNotFoundException

#### 5.3 Unit Tests - Job Service
- [ ] Create `tests/unit/test_job_service.py`
- [ ] Set up mock repositories in setup_method
- [ ] Test `get_all_jobs()` returns list
- [ ] Test `get_job_by_id()` with existing job
- [ ] Test `get_job_by_id()` raises JobNotFoundException
- [ ] Test `create_job()` with valid data
- [ ] Test `create_job()` raises CompanyNotFoundException for invalid company_id
- [ ] Test `update_job()` updates only provided fields
- [ ] Test `update_job()` validates new company_id
- [ ] Test `update_job()` raises JobNotFoundException
- [ ] Test `delete_job()` calls repository delete
- [ ] Test `delete_job()` raises JobNotFoundException

#### 5.4 Integration Tests - Company Repository
- [ ] Create `tests/integration/test_company_repository.py`
- [ ] Test `find_all()` returns all companies
- [ ] Test `find_by_id()` returns company when exists
- [ ] Test `find_by_id()` returns None when not exists
- [ ] Test `find_by_name()` returns company
- [ ] Test `save()` creates new company
- [ ] Test `save()` updates existing company
- [ ] Test `delete()` removes company from database
- [ ] Test cascade delete (deleting company deletes associated jobs)

#### 5.5 Integration Tests - Job Repository
- [ ] Create `tests/integration/test_job_repository.py`
- [ ] Test `find_all()` returns all jobs with company data
- [ ] Test `find_by_id()` returns job with company when exists
- [ ] Test `find_by_id()` returns None when not exists
- [ ] Test `find_by_company_id()` returns jobs for specific company
- [ ] Test `save()` creates new job
- [ ] Test `save()` updates existing job
- [ ] Test `delete()` removes job from database
- [ ] Test foreign key constraint (cannot create job with invalid company_id)

#### 5.6 API Tests - Company Routes
- [ ] Create `tests/api/test_company_routes.py`
- [ ] Test GET /api/companies returns 200 and list
- [ ] Test GET /api/companies/{id} returns 200 and company data
- [ ] Test GET /api/companies/{invalid_id} returns 404
- [ ] Test POST /api/companies with valid data returns 201
- [ ] Test POST /api/companies with invalid data returns 400
- [ ] Test POST /api/companies with missing fields returns 400
- [ ] Test PATCH /api/companies/{id} with valid data returns 200
- [ ] Test PATCH /api/companies/{id} updates only provided fields
- [ ] Test PATCH /api/companies/{invalid_id} returns 404
- [ ] Test DELETE /api/companies/{id} returns 204
- [ ] Test DELETE /api/companies/{invalid_id} returns 404

#### 5.7 API Tests - Job Routes
- [ ] Create `tests/api/test_job_routes.py`
- [ ] Test GET /api/jobs returns 200 and list with company data
- [ ] Test GET /api/jobs/{id} returns 200 and full job details
- [ ] Test GET /api/jobs/{invalid_id} returns 404
- [ ] Test POST /api/jobs with valid data returns 201
- [ ] Test POST /api/jobs with invalid company_id returns 404
- [ ] Test POST /api/jobs with missing required fields returns 400
- [ ] Test POST /api/jobs with invalid enum values returns 400
- [ ] Test POST /api/jobs with salary_max < salary_min returns 400
- [ ] Test POST /api/jobs with past expiry_date returns 400
- [ ] Test PATCH /api/jobs/{id} with valid data returns 200
- [ ] Test PATCH /api/jobs/{id} updates only provided fields
- [ ] Test PATCH /api/jobs/{invalid_id} returns 404
- [ ] Test DELETE /api/jobs/{id} returns 204
- [ ] Test DELETE /api/jobs/{invalid_id} returns 404

#### 5.8 Run Tests and Fix Issues
- [ ] Run all tests: `pytest`
- [ ] Verify all tests pass
- [ ] Run with coverage: `pytest --cov=app --cov-report=html`
- [ ] Verify coverage is >= 80%
- [ ] Review coverage report and add tests for uncovered code
- [ ] Fix any failing tests
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
