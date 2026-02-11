# Phase 2 Task Files: Advanced Routes

## PR #1: Search & Filter Endpoint with Pagination

**References**: Phase II - Search & Filter Endpoint, Pagination

**Dependencies**: Phase I must be completed

**Description**: Implement comprehensive job search functionality with multiple filter parameters and pagination support. This includes keyword search, location filtering, company filtering, job type/experience/remote filters, and salary range filtering.

### Subtasks:

#### 1.1 Update Job Repository with Search Method
- [ ] Open `app/repositories/job_repository.py`
- [ ] Import `or_` from sqlalchemy
- [ ] Add `search_jobs()` method with parameters:
  - [ ] keyword (optional string)
  - [ ] location (optional string)
  - [ ] company_id (optional int)
  - [ ] job_type (optional JobType enum)
  - [ ] experience_level (optional ExperienceLevel enum)
  - [ ] remote_option (optional RemoteOption enum)
  - [ ] min_salary (optional float)
  - [ ] max_salary (optional float)
  - [ ] is_active (boolean, default True)
  - [ ] page (int, default 1)
  - [ ] per_page (int, default 20)
- [ ] Start with base query: `Job.query.options(joinedload(Job.company))`
- [ ] Add keyword filter:
  - [ ] Use `or_` to search in title OR description
  - [ ] Use `ilike` for case-insensitive search
  - [ ] Format: `f"%{keyword}%"`
- [ ] Add location filter (case-insensitive partial match)
- [ ] Add company_id filter (exact match)
- [ ] Add job_type filter (exact match)
- [ ] Add experience_level filter (exact match)
- [ ] Add remote_option filter (exact match)
- [ ] Add min_salary filter (check if job.salary_max >= min_salary)
- [ ] Add max_salary filter (check if job.salary_min <= max_salary)
- [ ] Add is_active filter
- [ ] Return paginated results: `query.paginate(page=page, per_page=per_page, error_out=False)`

#### 1.2 Create Pagination Schema
- [ ] Create `app/schemas/pagination_schema.py`
- [ ] Define `PaginationSchema` with fields:
  - [ ] page (Integer)
  - [ ] per_page (Integer)
  - [ ] total (Integer)
  - [ ] pages (Integer)
  - [ ] has_prev (Boolean)
  - [ ] has_next (Boolean)
  - [ ] prev_num (Integer, allow_none=True)
  - [ ] next_num (Integer, allow_none=True)
- [ ] Define `PaginatedJobSchema` with fields:
  - [ ] items (List of JobSchema)
  - [ ] pagination (Nested PaginationSchema)

#### 1.3 Add Search Method to Job Service
- [ ] Open `app/services/job_service.py`
- [ ] Add `search_jobs()` method with same parameters as repository
- [ ] Convert string enum parameters to enum types:
  - [ ] `JobType[job_type]` if job_type provided
  - [ ] `ExperienceLevel[experience_level]` if experience_level provided
  - [ ] `RemoteOption[remote_option]` if remote_option provided
- [ ] Call `self.job_repository.search_jobs()` with converted parameters
- [ ] Get pagination object from repository
- [ ] Return dictionary with:
  - [ ] 'items': pagination.items
  - [ ] 'pagination': dict with page, per_page, total, pages, has_prev, has_next, prev_num, next_num

#### 1.4 Create Search Endpoint in Job Routes
- [ ] Open `app/routes/jobs.py`
- [ ] Import `request` from flask
- [ ] Create new `JobSearch` MethodView class
- [ ] Inject `JobService` in constructor
- [ ] Implement `get()` method:
  - [ ] Extract query parameters from request.args:
    - [ ] keyword (string)
    - [ ] location (string)
    - [ ] company_id (int)
    - [ ] job_type (string)
    - [ ] experience_level (string)
    - [ ] remote_option (string)
    - [ ] min_salary (float)
    - [ ] max_salary (float)
    - [ ] is_active (boolean, default True)
    - [ ] page (int, default 1)
    - [ ] per_page (int, default 20, max 100)
  - [ ] Enforce max per_page: `min(request.args.get('per_page', 20, type=int), 100)`
  - [ ] Call `job_service.search_jobs()` with all parameters
  - [ ] Return result
- [ ] Add route decorator: `@jobs_blp.route('/search')`
- [ ] Add response decorator: `@jobs_blp.response(200, PaginatedJobSchema)`

#### 1.5 Update Dependency Injection
- [ ] Open `app/__init__.py`
- [ ] Import `PaginatedJobSchema` from app.schemas.pagination_schema
- [ ] Verify JobService is properly injected (should already be configured)

#### 1.6 Manual Testing - Search Endpoint
- [ ] Restart Flask application
- [ ] Create test data (multiple jobs with different attributes)
- [ ] Test search with keyword only:
  - [ ] `GET /api/jobs/search?keyword=python`
  - [ ] Verify only jobs with "python" in title/description returned
- [ ] Test search with location:
  - [ ] `GET /api/jobs/search?location=New York`
  - [ ] Verify only jobs with "New York" in location returned
- [ ] Test search with company_id:
  - [ ] `GET /api/jobs/search?company_id=1`
  - [ ] Verify only jobs for that company returned
- [ ] Test search with job_type:
  - [ ] `GET /api/jobs/search?job_type=FULL_TIME`
  - [ ] Verify only FULL_TIME jobs returned
- [ ] Test search with experience_level:
  - [ ] `GET /api/jobs/search?experience_level=SENIOR`
  - [ ] Verify only SENIOR jobs returned
- [ ] Test search with remote_option:
  - [ ] `GET /api/jobs/search?remote_option=REMOTE`
  - [ ] Verify only REMOTE jobs returned
- [ ] Test search with salary range:
  - [ ] `GET /api/jobs/search?min_salary=80000`
  - [ ] Verify only jobs with salary_max >= 80000 returned
  - [ ] `GET /api/jobs/search?max_salary=120000`
  - [ ] Verify only jobs with salary_min <= 120000 returned
- [ ] Test multiple filters combined:
  - [ ] `GET /api/jobs/search?keyword=engineer&location=NYC&job_type=FULL_TIME`
  - [ ] Verify all filters applied correctly
- [ ] Test pagination:
  - [ ] `GET /api/jobs/search?page=1&per_page=5`
  - [ ] Verify returns first 5 results
  - [ ] Verify pagination metadata (total, pages, has_next, etc.)
  - [ ] `GET /api/jobs/search?page=2&per_page=5`
  - [ ] Verify returns next 5 results
- [ ] Test empty results:
  - [ ] `GET /api/jobs/search?keyword=nonexistentjob`
  - [ ] Verify returns empty list, not 404
  - [ ] Verify pagination shows total=0
- [ ] Test invalid enum values:
  - [ ] `GET /api/jobs/search?job_type=INVALID`
  - [ ] Verify returns 400 error
- [ ] Test per_page limit:
  - [ ] `GET /api/jobs/search?per_page=200`
  - [ ] Verify capped at 100
- [ ] Verify Swagger UI updated with new endpoint

---

## PR #2: Active Jobs Endpoint

**References**: Phase II - Active Jobs Endpoint

**Dependencies**: PR #1 must be completed

**Description**: Create an endpoint that returns only jobs that are currently active and not expired. This filters out both inactive jobs (is_active=false) and jobs past their expiry_date.

### Subtasks:

#### 2.1 Add Active Jobs Repository Method
- [ ] Open `app/repositories/job_repository.py`
- [ ] Import `datetime` from datetime
- [ ] Import `and_` from sqlalchemy
- [ ] Add `find_active_jobs()` method with parameters:
  - [ ] page (int, default 1)
  - [ ] per_page (int, default 20)
- [ ] Get current time: `now = datetime.utcnow()`
- [ ] Build query with filters:
  - [ ] Start with: `Job.query.options(joinedload(Job.company))`
  - [ ] Filter: `Job.is_active == True`
  - [ ] Filter: `or_(Job.expiry_date == None, Job.expiry_date > now)`
  - [ ] Combine with `and_`
- [ ] Return paginated results: `query.paginate(page=page, per_page=per_page, error_out=False)`

#### 2.2 Add Active Jobs Service Method
- [ ] Open `app/services/job_service.py`
- [ ] Add `get_active_jobs()` method with parameters:
  - [ ] page (int, default 1)
  - [ ] per_page (int, default 20)
- [ ] Call `self.job_repository.find_active_jobs(page, per_page)`
- [ ] Get pagination object
- [ ] Return dictionary with items and pagination metadata (same format as search)

#### 2.3 Create Active Jobs Endpoint
- [ ] Open `app/routes/jobs.py`
- [ ] Create new `ActiveJobs` MethodView class
- [ ] Inject `JobService` in constructor
- [ ] Implement `get()` method:
  - [ ] Extract page from request.args (default 1)
  - [ ] Extract per_page from request.args (default 20, max 100)
  - [ ] Call `job_service.get_active_jobs(page, per_page)`
  - [ ] Return result
- [ ] Add route decorator: `@jobs_blp.route('/active')`
- [ ] Add response decorator: `@jobs_blp.response(200, PaginatedJobSchema)`

#### 2.4 Manual Testing - Active Jobs Endpoint
- [ ] Create test jobs with different states:
  - [ ] Job 1: is_active=True, expiry_date=None
  - [ ] Job 2: is_active=True, expiry_date=future date
  - [ ] Job 3: is_active=True, expiry_date=past date (expired)
  - [ ] Job 4: is_active=False, expiry_date=None
  - [ ] Job 5: is_active=False, expiry_date=future date
- [ ] Test `GET /api/jobs/active`:
  - [ ] Verify only Job 1 and Job 2 are returned
  - [ ] Verify Job 3 (expired) is NOT returned
  - [ ] Verify Job 4 and Job 5 (inactive) are NOT returned
- [ ] Test pagination:
  - [ ] `GET /api/jobs/active?page=1&per_page=1`
  - [ ] Verify returns only 1 active job
  - [ ] Verify pagination metadata correct
- [ ] Test with no active jobs:
  - [ ] Deactivate all jobs or set all to expired
  - [ ] `GET /api/jobs/active`
  - [ ] Verify returns empty list (not 404)
- [ ] Verify Swagger UI shows endpoint

---

## PR #3: Deactivate Job Endpoint (Soft Delete)

**References**: Phase II - Deactivate Job Endpoint

**Dependencies**: PR #1 must be completed (PR #2 optional but recommended)

**Description**: Implement soft delete functionality by adding an endpoint to deactivate jobs instead of hard deleting them. This sets is_active=false while preserving the job record in the database.

### Subtasks:

#### 3.1 Add Deactivate Method to Job Service
- [ ] Open `app/services/job_service.py`
- [ ] Add `deactivate_job()` method with parameter:
  - [ ] job_id (int)
- [ ] Call `self.get_job_by_id(job_id)` to fetch job
  - [ ] This will raise JobNotFoundException if not found
- [ ] Set `job.is_active = False`
- [ ] Try to save job via repository
- [ ] Catch `StaleDataError` and raise `OptimisticLockException`
- [ ] Return None (void method)

#### 3.2 Create Deactivate Endpoint
- [ ] Open `app/routes/jobs.py`
- [ ] Create new `DeactivateJob` MethodView class
- [ ] Inject `JobService` in constructor
- [ ] Implement `post(job_id)` method:
  - [ ] Call `job_service.deactivate_job(job_id)`
  - [ ] Return JSON response: `{'message': 'Job successfully deactivated', 'job_id': job_id}`
  - [ ] Return with 200 status
- [ ] Add route decorator: `@jobs_blp.route('/<int:job_id>/deactivate')`
- [ ] Add response decorator: `@jobs_blp.response(200)`

#### 3.3 Manual Testing - Deactivate Endpoint
- [ ] Create an active job (is_active=True)
- [ ] Note the job_id
- [ ] Test deactivate:
  - [ ] `POST /api/jobs/{job_id}/deactivate`
  - [ ] Verify returns 200 with success message
  - [ ] Verify message includes job_id
- [ ] Verify job is deactivated:
  - [ ] `GET /api/jobs/{job_id}`
  - [ ] Verify is_active is now False
  - [ ] Job still exists in database (not deleted)
- [ ] Verify deactivated job doesn't show in active jobs:
  - [ ] `GET /api/jobs/active`
  - [ ] Verify the deactivated job is NOT in the list
- [ ] Test with non-existent job_id:
  - [ ] `POST /api/jobs/99999/deactivate`
  - [ ] Verify returns 404 JobNotFoundException
- [ ] Test idempotency (deactivate already deactivated job):
  - [ ] `POST /api/jobs/{job_id}/deactivate` (on already deactivated job)
  - [ ] Verify returns 200 (should succeed, job already inactive)
- [ ] Verify Swagger UI shows endpoint

---

## PR #4: Add Pagination to Existing List Endpoints

**References**: Phase II - Pagination on Existing Endpoints

**Dependencies**: PR #1 must be completed

**Description**: Update the existing GET /api/jobs and GET /api/companies endpoints to support pagination instead of returning all records at once.

### Subtasks:

#### 4.1 Update Job Repository for Pagination
- [ ] Open `app/repositories/job_repository.py`
- [ ] Modify `find_all()` method to accept pagination parameters:
  - [ ] Add page parameter (int, default 1)
  - [ ] Add per_page parameter (int, default 20)
- [ ] Change return from `.all()` to `.paginate(page=page, per_page=per_page, error_out=False)`
- [ ] Keep joinedload for company data

#### 4.2 Update Company Repository for Pagination
- [ ] Open `app/repositories/company_repository.py`
- [ ] Modify `find_all()` method to accept pagination parameters:
  - [ ] Add page parameter (int, default 1)
  - [ ] Add per_page parameter (int, default 20)
- [ ] Change return from `.all()` to `.paginate(page=page, per_page=per_page, error_out=False)`

#### 4.3 Update Job Service for Pagination
- [ ] Open `app/services/job_service.py`
- [ ] Modify `get_all_jobs()` method to accept pagination parameters:
  - [ ] Add page parameter (int, default 1)
  - [ ] Add per_page parameter (int, default 20)
- [ ] Call repository with pagination parameters
- [ ] Get pagination object
- [ ] Return dictionary with items and pagination metadata (same format as search)

#### 4.4 Update Company Service for Pagination
- [ ] Open `app/services/company_service.py`
- [ ] Modify `get_all_companies()` method to accept pagination parameters:
  - [ ] Add page parameter (int, default 1)
  - [ ] Add per_page parameter (int, default 20)
- [ ] Call repository with pagination parameters
- [ ] Get pagination object
- [ ] Return dictionary with items and pagination metadata

#### 4.5 Create Paginated Company Schema
- [ ] Open `app/schemas/pagination_schema.py` (or create if needed)
- [ ] Define `PaginatedCompanySchema` with fields:
  - [ ] items (List of CompanySchema)
  - [ ] pagination (Nested PaginationSchema)

#### 4.6 Update Job Routes for Pagination
- [ ] Open `app/routes/jobs.py`
- [ ] Find `JobList` class `get()` method
- [ ] Extract query parameters:
  - [ ] page from request.args (default 1)
  - [ ] per_page from request.args (default 20, max 100)
- [ ] Pass page and per_page to `job_service.get_all_jobs()`
- [ ] Update response decorator to use `PaginatedJobSchema`

#### 4.7 Update Company Routes for Pagination
- [ ] Open `app/routes/companies.py`
- [ ] Find `CompanyList` class `get()` method
- [ ] Extract query parameters:
  - [ ] page from request.args (default 1)
  - [ ] per_page from request.args (default 20, max 100)
- [ ] Pass page and per_page to `company_service.get_all_companies()`
- [ ] Update response decorator to use `PaginatedCompanySchema`

#### 4.8 Manual Testing - Paginated Endpoints
- [ ] Create at least 25 jobs and 25 companies for testing
- [ ] Test GET /api/jobs with pagination:
  - [ ] `GET /api/jobs` (no params, should default to page 1, per_page 20)
  - [ ] Verify returns first 20 jobs
  - [ ] Verify pagination metadata correct (total, pages, has_next=true)
  - [ ] `GET /api/jobs?page=2`
  - [ ] Verify returns next 20 jobs
  - [ ] `GET /api/jobs?per_page=10`
  - [ ] Verify returns 10 jobs per page
  - [ ] `GET /api/jobs?page=3&per_page=5`
  - [ ] Verify pagination works with both parameters
- [ ] Test GET /api/companies with pagination:
  - [ ] Same tests as above for companies endpoint
- [ ] Test edge cases:
  - [ ] `GET /api/jobs?page=999` (beyond last page)
  - [ ] Verify returns empty list (not 404)
  - [ ] `GET /api/jobs?per_page=200`
  - [ ] Verify capped at 100
  - [ ] `GET /api/jobs?page=0`
  - [ ] Verify defaults to page 1
  - [ ] `GET /api/jobs?per_page=-5`
  - [ ] Verify defaults to 20
- [ ] Verify Swagger UI updated for both endpoints

---

## Phase II Completion Checklist

- [ ] All 4 PRs completed and merged
- [ ] Search endpoint works with all filter combinations
- [ ] Search handles null/missing parameters correctly
- [ ] Active jobs endpoint returns only active, non-expired jobs
- [ ] Deactivate endpoint sets is_active to false
- [ ] Pagination works on all list endpoints (jobs, companies, search, active)
- [ ] Page size limits enforced (max 100)
- [ ] Empty search results return empty page, not 404
- [ ] Invalid enum values return 400 with clear message
- [ ] All manual testing passed
- [ ] Swagger documentation updated
- [ ] Ready to proceed to Phase III
