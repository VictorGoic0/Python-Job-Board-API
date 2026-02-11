# Phase 3 Task Files: Authentication, Applications, Files, and Background Tasks

## PR #1: Authentication and Authorization

**References**: Phase IV - Authentication & Authorization

**Dependencies**: Phase I and II must be completed

**Description**: Implement JWT-based authentication system with user registration, login, role-based access control, and protect existing endpoints based on user roles.

### Subtasks:

#### 1.1 Add Authentication Dependencies
- [ ] Add to `requirements.txt`:
  - [ ] Flask-JWT-Extended==4.5.3
  - [ ] bcrypt==4.1.2
- [ ] Run `pip install -r requirements.txt`

#### 1.2 Update Configuration for JWT
- [ ] Open `config.py`
- [ ] Add JWT configuration to Config class:
  - [ ] JWT_SECRET_KEY (from env or default)
  - [ ] JWT_ACCESS_TOKEN_EXPIRES (timedelta of 1 hour)
  - [ ] JWT_REFRESH_TOKEN_EXPIRES (timedelta of 30 days)
- [ ] Import timedelta at top of file

#### 1.3 Create User Model
- [ ] Create `app/models/user.py`
- [ ] Import bcrypt and datetime
- [ ] Define UserRole constants class:
  - [ ] ADMIN = 'ADMIN'
  - [ ] RECRUITER = 'RECRUITER'
  - [ ] JOB_SEEKER = 'JOB_SEEKER'
- [ ] Define User model with fields:
  - [ ] id (BigInteger, primary key)
  - [ ] email (String 255, unique, required)
  - [ ] password_hash (String 255, required)
  - [ ] full_name (String 255, required)
  - [ ] role (String 50, required)
  - [ ] enabled (Boolean, default True, required)
  - [ ] created_at (DateTime, auto-generated)
  - [ ] updated_at (DateTime, auto-updated)
- [ ] Add `set_password(password)` method:
  - [ ] Hash password with bcrypt.hashpw()
  - [ ] Store as password_hash
- [ ] Add `check_password(password)` method:
  - [ ] Compare with bcrypt.checkpw()
  - [ ] Return boolean
- [ ] Add `__repr__` method

#### 1.4 Create User Table Migration
- [ ] Create `migrations/003_create_user_table.sql`
- [ ] Write SQL to create users table with all fields
- [ ] Add unique constraint on email
- [ ] Create index on email
- [ ] Run migration: `python migrations/run_migrations.py`

#### 1.5 Create Auth Schemas
- [ ] Create `app/schemas/auth_schema.py`
- [ ] Define `UserRegisterSchema`:
  - [ ] email (Email, required)
  - [ ] password (String, required, min length 8)
  - [ ] full_name (String, required, length 1-255)
  - [ ] role (String, required, OneOf ADMIN/RECRUITER/JOB_SEEKER)
- [ ] Define `UserLoginSchema`:
  - [ ] email (Email, required)
  - [ ] password (String, required)
- [ ] Define `UserSchema` (for responses):
  - [ ] id (Integer, dump_only)
  - [ ] email (Email)
  - [ ] full_name (String)
  - [ ] role (String)
  - [ ] enabled (Boolean)
  - [ ] created_at (DateTime, dump_only)

#### 1.6 Create User Repository
- [ ] Create `app/repositories/user_repository.py`
- [ ] Define UserRepository class
- [ ] Implement `find_by_id(user_id)` → Optional[User]
- [ ] Implement `find_by_email(email)` → Optional[User]
- [ ] Implement `save(user)` → User
- [ ] Implement `find_all()` → List[User]

#### 1.7 Create Auth Service
- [ ] Create `app/services/auth_service.py`
- [ ] Import User, UserRepository, JWT functions
- [ ] Define AuthService class
- [ ] Inject UserRepository
- [ ] Implement `register_user(email, password, full_name, role)` → User:
  - [ ] Check if email already exists
  - [ ] Raise AuthenticationException if exists
  - [ ] Create new User instance
  - [ ] Call user.set_password(password)
  - [ ] Save via repository
  - [ ] Return user
- [ ] Implement `login_user(email, password)` → dict:
  - [ ] Find user by email
  - [ ] Raise AuthenticationException if not found
  - [ ] Check password with user.check_password()
  - [ ] Raise AuthenticationException if wrong password
  - [ ] Check if user.enabled
  - [ ] Raise AuthenticationException if disabled
  - [ ] Create access_token with user.id and role claim
  - [ ] Create refresh_token with user.id
  - [ ] Return dict with access_token, refresh_token, user
- [ ] Implement `get_user_by_id(user_id)` → Optional[User]:
  - [ ] Call repository.find_by_id()

#### 1.8 Initialize JWT in Application
- [ ] Open `app/extensions.py`
- [ ] Import JWTManager from flask_jwt_extended
- [ ] Create jwt instance: `jwt = JWTManager()`
- [ ] Open `app/__init__.py`
- [ ] Import jwt from extensions
- [ ] Initialize jwt in create_app: `jwt.init_app(app)`

#### 1.9 Create Auth Routes
- [ ] Create `app/routes/auth.py`
- [ ] Import necessary modules (MethodView, Blueprint, JWT decorators, schemas)
- [ ] Create auth_blp Blueprint (url_prefix='/api/auth')
- [ ] Define Register MethodView:
  - [ ] Inject AuthService
  - [ ] Implement post() method:
    - [ ] Use UserRegisterSchema for arguments
    - [ ] Call auth_service.register_user()
    - [ ] Return user with 201 status
    - [ ] Use UserSchema for response
- [ ] Define Login MethodView:
  - [ ] Inject AuthService
  - [ ] Implement post() method:
    - [ ] Use UserLoginSchema for arguments
    - [ ] Call auth_service.login_user()
    - [ ] Return dict with tokens and user
    - [ ] Return with 200 status
- [ ] Define CurrentUser MethodView:
  - [ ] Inject AuthService
  - [ ] Implement get() method:
    - [ ] Add @jwt_required() decorator
    - [ ] Get user_id from get_jwt_identity()
    - [ ] Call auth_service.get_user_by_id()
    - [ ] Return user with UserSchema
- [ ] Register routes: /register, /login, /me

#### 1.10 Register Auth Blueprint
- [ ] Open `app/__init__.py`
- [ ] Import auth_blp from app.routes.auth
- [ ] Register blueprint: `api.register_blueprint(auth_blp)`

#### 1.11 Update Dependency Injection
- [ ] Open `app/__init__.py`
- [ ] Import UserRepository and AuthService
- [ ] Add to configure function:
  - [ ] Bind UserRepository to singleton
  - [ ] Bind AuthService to singleton

#### 1.12 Create Role-Based Access Decorator
- [ ] Create `app/utils/decorators.py`
- [ ] Import wraps, verify_jwt_in_request, get_jwt, jsonify
- [ ] Define `role_required(*required_roles)` decorator:
  - [ ] Create wrapper function
  - [ ] Call verify_jwt_in_request()
  - [ ] Get claims with get_jwt()
  - [ ] Get user_role from claims
  - [ ] Check if user_role in required_roles
  - [ ] Return 403 if not authorized
  - [ ] Return original function if authorized

#### 1.13 Protect Job Endpoints
- [ ] Open `app/routes/jobs.py`
- [ ] Import jwt_required and role_required
- [ ] Update JobList post() method:
  - [ ] Add @jwt_required() decorator
  - [ ] Add @role_required('ADMIN', 'RECRUITER') decorator
- [ ] Update JobDetail patch() method:
  - [ ] Add @jwt_required() decorator
  - [ ] Add @role_required('ADMIN', 'RECRUITER') decorator
- [ ] Update JobDetail delete() method:
  - [ ] Add @jwt_required() decorator
  - [ ] Add @role_required('ADMIN', 'RECRUITER') decorator
- [ ] Update DeactivateJob post() method:
  - [ ] Add @jwt_required() decorator
  - [ ] Add @role_required('ADMIN', 'RECRUITER') decorator
- [ ] Keep GET endpoints public (no auth required)

#### 1.14 Protect Company Endpoints
- [ ] Open `app/routes/companies.py`
- [ ] Import jwt_required and role_required
- [ ] Update CompanyList post() method:
  - [ ] Add @jwt_required() decorator
  - [ ] Add @role_required('ADMIN', 'RECRUITER') decorator
- [ ] Update CompanyDetail patch() method:
  - [ ] Add @jwt_required() decorator
  - [ ] Add @role_required('ADMIN', 'RECRUITER') decorator
- [ ] Update CompanyDetail delete() method:
  - [ ] Add @jwt_required() decorator
  - [ ] Add @role_required('ADMIN', 'RECRUITER') decorator
- [ ] Keep GET endpoints public (no auth required)

#### 1.15 Manual Testing - Authentication
- [ ] Test user registration:
  - [ ] POST /api/auth/register with valid data (all roles)
  - [ ] Verify returns 201 with user data (no password in response)
  - [ ] Try duplicate email → verify 400 error
  - [ ] Try invalid email format → verify 400 validation error
  - [ ] Try short password (<8 chars) → verify 400 validation error
- [ ] Test user login:
  - [ ] POST /api/auth/login with valid credentials
  - [ ] Verify returns 200 with access_token and refresh_token
  - [ ] Try wrong password → verify 401 error
  - [ ] Try non-existent email → verify 401 error
- [ ] Test current user endpoint:
  - [ ] GET /api/auth/me without token → verify 401 error
  - [ ] GET /api/auth/me with valid token → verify 200 with user data
  - [ ] Try with expired token → verify 401 error
- [ ] Test protected job endpoints:
  - [ ] POST /api/jobs without token → verify 401 error
  - [ ] POST /api/jobs with JOB_SEEKER token → verify 403 forbidden
  - [ ] POST /api/jobs with RECRUITER token → verify 201 success
  - [ ] POST /api/jobs with ADMIN token → verify 201 success
- [ ] Test public endpoints still work:
  - [ ] GET /api/jobs → verify 200 (no auth needed)
  - [ ] GET /api/jobs/search → verify 200 (no auth needed)
- [ ] Verify Swagger UI shows auth endpoints and security schemes

---

## PR #2: Application Entity and Endpoints

**References**: Phase IV - Application Entity

**Dependencies**: PR #1 (Authentication) must be completed

**Description**: Create the Application entity that allows job seekers to apply to jobs, and recruiters to view applications for their company's jobs. Includes duplicate application prevention.

### Subtasks:

#### 2.1 Create Application Model
- [ ] Create `app/models/application.py`
- [ ] Import datetime, db, and relationship models
- [ ] Define ApplicationStatus constants class:
  - [ ] PENDING = 'PENDING'
  - [ ] REVIEWING = 'REVIEWING'
  - [ ] INTERVIEWED = 'INTERVIEWED'
  - [ ] ACCEPTED = 'ACCEPTED'
  - [ ] REJECTED = 'REJECTED'
- [ ] Define Application model with fields:
  - [ ] id (BigInteger, primary key)
  - [ ] job_id (BigInteger, foreign key to job)
  - [ ] user_id (BigInteger, foreign key to users)
  - [ ] resume_path (String 500, optional)
  - [ ] cover_letter (Text, optional)
  - [ ] status (String 50, default PENDING, required)
  - [ ] applied_at (DateTime, auto-generated, required)
  - [ ] version (Integer, for optimistic locking)
- [ ] Add relationships:
  - [ ] job (relationship to Job, backref='applications')
  - [ ] user (relationship to User, backref='applications')
- [ ] Add unique constraint on (job_id, user_id)
- [ ] Add `__repr__` method

#### 2.2 Create Application Table Migration
- [ ] Create `migrations/004_create_application_table.sql`
- [ ] Write SQL to create application table with all fields
- [ ] Add foreign keys to job and users tables (with CASCADE)
- [ ] Add unique constraint on (job_id, user_id)
- [ ] Create indexes on job_id and user_id
- [ ] Run migration: `python migrations/run_migrations.py`

#### 2.3 Create Application Schemas
- [ ] Create `app/schemas/application_schema.py`
- [ ] Import necessary modules
- [ ] Define `ApplicationCreateSchema`:
  - [ ] job_id (Integer, required)
  - [ ] cover_letter (String, optional)
  - [ ] Note: resume will be handled separately via file upload
- [ ] Define `ApplicationSchema` (for responses):
  - [ ] id (Integer, dump_only)
  - [ ] job_id (Integer)
  - [ ] user_id (Integer)
  - [ ] resume_path (String, allow_none)
  - [ ] cover_letter (String, allow_none)
  - [ ] status (String)
  - [ ] applied_at (DateTime, dump_only)
  - [ ] Include nested JobSchema for job details
  - [ ] Include nested UserSchema for user details
- [ ] Define `ApplicationStatusUpdateSchema`:
  - [ ] status (String, required, OneOf valid status values)

#### 2.4 Create Application Repository
- [ ] Create `app/repositories/application_repository.py`
- [ ] Define ApplicationRepository class
- [ ] Implement `find_by_id(application_id)` → Optional[Application]
- [ ] Implement `find_by_user_id(user_id)` → List[Application]:
  - [ ] Use joinedload for job and user relationships
- [ ] Implement `find_by_job_id(job_id)` → List[Application]:
  - [ ] Use joinedload for job and user relationships
- [ ] Implement `find_by_user_and_job(user_id, job_id)` → Optional[Application]
- [ ] Implement `save(application)` → Application
- [ ] Implement `delete(application)` → None

#### 2.5 Create Application Service
- [ ] Create `app/services/application_service.py`
- [ ] Inject ApplicationRepository, JobRepository, UserRepository
- [ ] Implement `create_application(user_id, job_id, cover_letter, resume_path=None)` → Application:
  - [ ] Verify job exists (raise JobNotFoundException)
  - [ ] Verify user exists (raise UserNotFoundException)
  - [ ] Check if job is active and not expired
  - [ ] Raise exception if job not available
  - [ ] Check for duplicate application
  - [ ] Raise exception if already applied
  - [ ] Create Application instance
  - [ ] Save via repository
  - [ ] Return application
- [ ] Implement `get_my_applications(user_id)` → List[Application]:
  - [ ] Call repository.find_by_user_id()
- [ ] Implement `get_applications_for_job(job_id, requesting_user_id)` → List[Application]:
  - [ ] Verify requesting user is ADMIN or RECRUITER
  - [ ] If RECRUITER, verify they own the company for this job
  - [ ] Call repository.find_by_job_id()
- [ ] Implement `update_application_status(application_id, status, requesting_user_id)` → Application:
  - [ ] Get application
  - [ ] Verify requesting user is ADMIN or RECRUITER
  - [ ] If RECRUITER, verify they own the company
  - [ ] Update status
  - [ ] Save via repository
- [ ] Implement `withdraw_application(application_id, user_id)` → None:
  - [ ] Get application
  - [ ] Verify application belongs to user
  - [ ] Delete via repository

#### 2.6 Create Application Routes
- [ ] Create `app/routes/applications.py`
- [ ] Create applications_blp Blueprint (url_prefix='/api/applications')
- [ ] Define ApplicationCreate MethodView:
  - [ ] Add @jwt_required() decorator
  - [ ] Inject ApplicationService
  - [ ] Implement post() method:
    - [ ] Get user_id from get_jwt_identity()
    - [ ] Use ApplicationCreateSchema for arguments
    - [ ] Call service.create_application()
    - [ ] Return application with 201 status
- [ ] Define MyApplications MethodView:
  - [ ] Route: /my-applications
  - [ ] Add @jwt_required() decorator
  - [ ] Inject ApplicationService
  - [ ] Implement get() method:
    - [ ] Get user_id from get_jwt_identity()
    - [ ] Call service.get_my_applications()
    - [ ] Return list with 200 status
- [ ] Define JobApplications MethodView:
  - [ ] Route: /job/<int:job_id>
  - [ ] Add @jwt_required() decorator
  - [ ] Add @role_required('ADMIN', 'RECRUITER') decorator
  - [ ] Inject ApplicationService
  - [ ] Implement get(job_id) method:
    - [ ] Get user_id from get_jwt_identity()
    - [ ] Call service.get_applications_for_job()
    - [ ] Return list with 200 status
- [ ] Define ApplicationStatusUpdate MethodView:
  - [ ] Route: /<int:application_id>/status
  - [ ] Add @jwt_required() decorator
  - [ ] Add @role_required('ADMIN', 'RECRUITER') decorator
  - [ ] Inject ApplicationService
  - [ ] Implement patch(status_data, application_id) method:
    - [ ] Get user_id from get_jwt_identity()
    - [ ] Call service.update_application_status()
    - [ ] Return updated application with 200 status
- [ ] Define ApplicationWithdraw MethodView:
  - [ ] Route: /<int:application_id>
  - [ ] Add @jwt_required() decorator
  - [ ] Inject ApplicationService
  - [ ] Implement delete(application_id) method:
    - [ ] Get user_id from get_jwt_identity()
    - [ ] Call service.withdraw_application()
    - [ ] Return 204 no content

#### 2.7 Register Application Blueprint
- [ ] Open `app/__init__.py`
- [ ] Import applications_blp from app.routes.applications
- [ ] Register blueprint: `api.register_blueprint(applications_blp)`

#### 2.8 Update Dependency Injection
- [ ] Open `app/__init__.py`
- [ ] Import ApplicationRepository and ApplicationService
- [ ] Add to configure function:
  - [ ] Bind ApplicationRepository to singleton
  - [ ] Bind ApplicationService to singleton

#### 2.9 Manual Testing - Applications
- [ ] Create test data (companies, jobs, users)
- [ ] Test create application:
  - [ ] Login as JOB_SEEKER
  - [ ] POST /api/applications with valid job_id
  - [ ] Verify returns 201 with application data
  - [ ] Try to apply to same job again → verify duplicate error
  - [ ] Try to apply to inactive job → verify error
  - [ ] Try to apply to expired job → verify error
  - [ ] Try without auth → verify 401 error
- [ ] Test get my applications:
  - [ ] GET /api/applications/my-applications with JOB_SEEKER token
  - [ ] Verify returns list of user's applications
  - [ ] Verify includes job details
- [ ] Test get applications for job (recruiter):
  - [ ] Login as RECRUITER
  - [ ] GET /api/applications/job/{job_id} for their company's job
  - [ ] Verify returns list of applications for that job
  - [ ] Try to access applications for another company's job → verify 403
  - [ ] Try as JOB_SEEKER → verify 403
- [ ] Test update application status:
  - [ ] Login as RECRUITER
  - [ ] PATCH /api/applications/{id}/status to REVIEWING
  - [ ] Verify status updated
  - [ ] Try as JOB_SEEKER → verify 403
- [ ] Test withdraw application:
  - [ ] Login as JOB_SEEKER who applied
  - [ ] DELETE /api/applications/{id}
  - [ ] Verify returns 204
  - [ ] Verify application deleted
  - [ ] Try to withdraw another user's application → verify 403

---

## PR #3: File Upload (Resume Storage)

**References**: Phase IV - File Upload

**Dependencies**: PR #2 (Applications) must be completed

**Description**: Implement file upload functionality for resume storage with validation for file types and sizes. Integrate with the application creation process.

### Subtasks:

#### 3.1 Create File Storage Service
- [ ] Create `app/services/file_storage_service.py`
- [ ] Import os, uuid, werkzeug utilities
- [ ] Define constants:
  - [ ] ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
  - [ ] MAX_FILE_SIZE = 5 * 1024 * 1024 (5MB)
- [ ] Define FileStorageService class
- [ ] Add `__init__(upload_dir='./uploads/resumes')`:
  - [ ] Store upload_dir
  - [ ] Create directory if not exists: `os.makedirs(upload_dir, exist_ok=True)`
- [ ] Implement `allowed_file(filename)` → bool:
  - [ ] Check if filename has extension
  - [ ] Check if extension in ALLOWED_EXTENSIONS
- [ ] Implement `save_file(file)` → str:
  - [ ] Validate file exists
  - [ ] Check file type with allowed_file()
  - [ ] Raise InvalidFileException if not allowed
  - [ ] Check file size (seek to end, tell, seek back to start)
  - [ ] Raise InvalidFileException if too large
  - [ ] Generate unique filename with uuid
  - [ ] Use secure_filename for sanitization
  - [ ] Combine: uuid + original extension
  - [ ] Save file to upload_dir
  - [ ] Return filepath
- [ ] Implement `delete_file(filepath)` → None:
  - [ ] Check if file exists
  - [ ] Delete file with os.remove()

#### 3.2 Update Application Service for File Upload
- [ ] Open `app/services/application_service.py`
- [ ] Inject FileStorageService in constructor
- [ ] Update `create_application()` method signature:
  - [ ] Add optional file parameter
- [ ] In create_application():
  - [ ] If file provided, call file_storage_service.save_file(file)
  - [ ] Store returned filepath in application.resume_path
  - [ ] If no file, resume_path stays None

#### 3.3 Update Application Routes for File Upload
- [ ] Open `app/routes/applications.py`
- [ ] Import request from flask
- [ ] Update ApplicationCreate post() method:
  - [ ] Check if 'resume' file is in request.files
  - [ ] Get file from request.files['resume']
  - [ ] Pass file to service.create_application()
  - [ ] Keep existing cover_letter from JSON body
- [ ] Update to accept multipart/form-data

#### 3.4 Update Dependency Injection
- [ ] Open `app/__init__.py`
- [ ] Import FileStorageService
- [ ] Add to configure function:
  - [ ] Bind FileStorageService to singleton

#### 3.5 Create Uploads Directory
- [ ] Create directory structure: `./uploads/resumes/`
- [ ] Add `uploads/` to `.gitignore`
- [ ] Document in README

#### 3.6 Manual Testing - File Upload
- [ ] Test valid file upload:
  - [ ] POST /api/applications with resume PDF file
  - [ ] Verify file saved in uploads/resumes/
  - [ ] Verify application has resume_path
  - [ ] Verify filename is UUID-based (not original filename)
- [ ] Test invalid file type:
  - [ ] POST /api/applications with .exe file
  - [ ] Verify returns 400 InvalidFileException
- [ ] Test file too large:
  - [ ] POST /api/applications with 10MB PDF
  - [ ] Verify returns 400 InvalidFileException
- [ ] Test valid file types:
  - [ ] Try .pdf → verify success
  - [ ] Try .doc → verify success
  - [ ] Try .docx → verify success
- [ ] Test without file (optional resume):
  - [ ] POST /api/applications without resume
  - [ ] Verify application created with resume_path=None
- [ ] Test file security:
  - [ ] Upload file with malicious filename (../../../etc/passwd)
  - [ ] Verify filename sanitized and saved safely

---

## PR #4: Celery Background Tasks

**References**: Phase IV - Celery Tasks

**Dependencies**: PR #1 (Authentication) must be completed, RabbitMQ already running

**Description**: Set up Celery task queue with RabbitMQ broker and implement scheduled task to automatically expire old jobs daily.

### Subtasks:

#### 4.1 Add Celery Dependencies
- [ ] Add to `requirements.txt`:
  - [ ] celery==5.3.4
- [ ] Run `pip install -r requirements.txt`

#### 4.2 Create Celery Configuration
- [ ] Create `app/celery_app.py`
- [ ] Import Celery, crontab from celery
- [ ] Define `make_celery(app)` function:
  - [ ] Create Celery instance with app.import_name
  - [ ] Set broker from app.config['CELERY_BROKER_URL']
  - [ ] Set backend from app.config['CELERY_RESULT_BACKEND']
  - [ ] Update celery config with app.config
  - [ ] Configure beat_schedule with 'expire-old-jobs' task:
    - [ ] Task name: 'app.tasks.expire_old_jobs'
    - [ ] Schedule: crontab(hour=2, minute=0) # 2 AM daily
  - [ ] Create ContextTask class for app context
  - [ ] Return celery instance

#### 4.3 Create Celery Tasks
- [ ] Create `app/tasks.py`
- [ ] Import necessary modules (datetime, db, Job)
- [ ] Import create_app and make_celery
- [ ] Create app instance: `app = create_app()`
- [ ] Create celery instance: `celery = make_celery(app)`
- [ ] Define `@celery.task(name='app.tasks.expire_old_jobs')`:
  - [ ] Use `with app.app_context():` context manager
  - [ ] Get current time: `now = datetime.utcnow()`
  - [ ] Query for expired jobs:
    - [ ] Filter: is_active == True
    - [ ] Filter: expiry_date != None
    - [ ] Filter: expiry_date < now
  - [ ] Loop through expired jobs:
    - [ ] Set is_active = False
  - [ ] Commit changes: `db.session.commit()`
  - [ ] Log how many jobs expired
  - [ ] Return count of expired jobs

#### 4.4 Verify Celery Services in Docker Compose
- [ ] Open `docker-compose.yml`
- [ ] Verify celery-worker service exists:
  - [ ] Uses same Dockerfile as app
  - [ ] Same environment variables
  - [ ] Command: `celery -A app.tasks.celery worker --loglevel=info`
  - [ ] Depends on postgres and rabbitmq
- [ ] Verify celery-beat service exists:
  - [ ] Uses same Dockerfile as app
  - [ ] Same environment variables
  - [ ] Command: `celery -A app.tasks.celery beat --loglevel=info`
  - [ ] Depends on postgres and rabbitmq

#### 4.5 Create Manual Task Trigger (Optional)
- [ ] Create route to manually trigger expire jobs (for testing)
- [ ] Add endpoint: POST /api/admin/expire-jobs
- [ ] Require ADMIN role
- [ ] Call expire_old_jobs.delay() to queue task
- [ ] Return task_id

#### 4.6 Manual Testing - Celery Tasks
- [ ] Start all services: `docker-compose up`
- [ ] Verify Celery worker starts without errors
- [ ] Verify Celery beat starts without errors
- [ ] Check worker logs: `docker-compose logs celery-worker`
- [ ] Check beat logs: `docker-compose logs celery-beat`
- [ ] Create test jobs with past expiry dates:
  - [ ] Job 1: expiry_date = 1 day ago, is_active=True
  - [ ] Job 2: expiry_date = 2 days ago, is_active=True
  - [ ] Job 3: expiry_date = 1 week from now, is_active=True
- [ ] Manually trigger task (if endpoint created):
  - [ ] POST /api/admin/expire-jobs
  - [ ] Check worker logs for task execution
- [ ] Or manually execute in Python shell:
  - [ ] Import and call expire_old_jobs.delay()
- [ ] Verify expired jobs:
  - [ ] Check Job 1 and Job 2 now have is_active=False
  - [ ] Check Job 3 still has is_active=True (not expired yet)
- [ ] Test scheduled execution:
  - [ ] Wait for scheduled time (or temporarily change crontab for testing)
  - [ ] Verify task runs automatically
  - [ ] Check beat logs for scheduled task firing
  - [ ] Check worker logs for task execution
- [ ] Verify task idempotency:
  - [ ] Run task multiple times on same data
  - [ ] Verify no errors or duplicate processing

#### 4.7 Add Celery Documentation
- [ ] Update README.md with Celery information:
  - [ ] How to start Celery worker manually (if not using Docker)
  - [ ] How to start Celery beat manually (if not using Docker)
  - [ ] How to check task status
  - [ ] How to monitor RabbitMQ (management UI)
- [ ] Document scheduled tasks:
  - [ ] expire_old_jobs runs daily at 2 AM
  - [ ] What the task does (sets is_active=False for expired jobs)

---

## Phase III Completion Checklist

- [ ] All 4 PRs completed and merged
- [ ] Users can register and login (JWT tokens issued)
- [ ] Role-based access control enforced on protected endpoints
- [ ] Public endpoints (GET jobs, companies, search) still accessible without auth
- [ ] Users can apply to jobs with optional resume upload
- [ ] Duplicate applications prevented (unique constraint)
- [ ] Recruiters can view applications for their company's jobs only
- [ ] Application status can be updated by recruiters
- [ ] File upload validates file type (.pdf, .doc, .docx only)
- [ ] File upload validates file size (max 5MB)
- [ ] Files stored with secure UUID-based filenames
- [ ] Celery worker and beat running in Docker
- [ ] Scheduled task expires old jobs daily at 2 AM
- [ ] Manual testing of Celery task successful
- [ ] All manual testing passed
- [ ] Swagger documentation updated with all new endpoints
- [ ] Ready to proceed to Phase IV (comprehensive testing)
