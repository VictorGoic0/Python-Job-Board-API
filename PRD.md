# Product Requirements Document: Job Board API (Flask/Python)

## Project Overview

A production-ready RESTful API for a job board platform built with Flask and Python. The system manages job postings with full CRUD operations, advanced search capabilities, and proper database relationships.

---

## Tech Stack

- **Language**: Python 3.11
- **Framework**: Flask 3.x
- **Database**: PostgreSQL (Dockerized)
- **ORM**: SQLAlchemy
- **Migrations**: Raw SQL with Python runner script
- **Validation**: Marshmallow
- **Task Queue**: Celery with RabbitMQ
- **Authentication**: Flask-JWT-Extended
- **API Docs**: Flask-SMOREST (OpenAPI/Swagger)
- **Dependency Injection**: Flask-Injector
- **Testing**: pytest (80% coverage goal)
- **Containerization**: Docker + Docker Compose

---

## Database Schema

```sql
-- Company Table
CREATE TABLE company (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    website VARCHAR(255),
    location VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 0
);

-- Job Table
CREATE TABLE job (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    company_id BIGINT NOT NULL REFERENCES company(id) ON DELETE CASCADE,
    location VARCHAR(255) NOT NULL,
    salary_min NUMERIC(10, 2),
    salary_max NUMERIC(10, 2),
    job_type VARCHAR(50) NOT NULL,
    experience_level VARCHAR(50) NOT NULL,
    remote_option VARCHAR(50) NOT NULL,
    posted_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    application_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 0
);

CREATE INDEX idx_job_company_id ON job(company_id);
CREATE INDEX idx_job_is_active ON job(is_active);
CREATE INDEX idx_job_posted_date ON job(posted_date);
```

---

## Project Structure

```
job-board-api/
├── app/
│   ├── __init__.py              # Application factory
│   ├── extensions.py            # Flask extensions
│   ├── models/                  # SQLAlchemy models
│   │   ├── company.py
│   │   ├── job.py
│   │   ├── user.py
│   │   ├── application.py
│   │   └── enums.py
│   ├── schemas/                 # Marshmallow schemas (DTOs)
│   │   ├── company_schema.py
│   │   ├── job_schema.py
│   │   ├── auth_schema.py
│   │   └── pagination_schema.py
│   ├── repositories/            # Data access layer
│   │   ├── company_repository.py
│   │   └── job_repository.py
│   ├── services/                # Business logic
│   │   ├── company_service.py
│   │   ├── job_service.py
│   │   ├── auth_service.py
│   │   └── file_storage_service.py
│   ├── routes/                  # Blueprints (controllers)
│   │   ├── companies.py
│   │   ├── jobs.py
│   │   └── auth.py
│   ├── exceptions/
│   │   └── custom_exceptions.py
│   └── utils/
│       ├── error_handlers.py
│       └── decorators.py
├── migrations/
│   ├── 001_create_company_table.sql
│   ├── 002_create_job_table.sql
│   └── run_migrations.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── api/
├── docker/
│   └── Dockerfile
├── docker-compose.yml
├── config.py
├── run.py
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```

---

## Phase I: Core Setup & Basic CRUD

### Dependencies (requirements.txt)

```txt
# Core
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Marshmallow==0.15.0
marshmallow-sqlalchemy==0.29.0
Flask-CORS==4.0.0
Flask-Injector==0.15.0
python-dotenv==1.0.0

# Database
psycopg2-binary==2.9.9
SQLAlchemy==2.0.23

# API Documentation
flask-smorest==0.42.3

# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-flask==1.3.0
```

### Docker Setup

**docker-compose.yml**:

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:15-alpine
    container_name: job_board_db
    environment:
      POSTGRES_DB: job_board
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 10s
      timeout: 5s
      retries: 5

  rabbitmq:
    image: rabbitmq:3.12-management-alpine
    container_name: job_board_rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin123
    ports:
      - "5672:5672"
      - "15672:15672"
    healthcheck:
      test: ["CMD-SHELL", "rabbitmq-diagnostics -q ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    build:
      context: .
      dockerfile: docker/Dockerfile
    container_name: job_board_app
    environment:
      FLASK_ENV: development
      DATABASE_URL: postgresql://admin:admin123@postgres:5432/job_board
      CELERY_BROKER_URL: amqp://admin:admin123@rabbitmq:5672//
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    depends_on:
      postgres:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    command: flask run --host=0.0.0.0 --debug

  celery-worker:
    build:
      context: .
      dockerfile: docker/Dockerfile
    container_name: job_board_celery
    environment:
      DATABASE_URL: postgresql://admin:admin123@postgres:5432/job_board
      CELERY_BROKER_URL: amqp://admin:admin123@rabbitmq:5672//
    depends_on:
      - postgres
      - rabbitmq
    command: celery -A app.tasks.celery worker --loglevel=info

  celery-beat:
    build:
      context: .
      dockerfile: docker/Dockerfile
    container_name: job_board_beat
    environment:
      DATABASE_URL: postgresql://admin:admin123@postgres:5432/job_board
      CELERY_BROKER_URL: amqp://admin:admin123@rabbitmq:5672//
    depends_on:
      - postgres
      - rabbitmq
    command: celery -A app.tasks.celery beat --loglevel=info

volumes:
  postgres_data:
```

**docker/Dockerfile**:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
```

### Configuration (config.py)

```python
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://admin:admin123@localhost:5432/job_board'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API Documentation
    API_TITLE = 'Job Board API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_SWAGGER_UI_PATH = '/swagger'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Celery
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'amqp://admin:admin123@localhost:5672//'
    CELERY_RESULT_BACKEND = 'rpc://'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:admin123@localhost:5432/job_board_test'
    SQLALCHEMY_ECHO = False

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

### Models

**app/models/enums.py**:

```python
import enum

class JobType(enum.Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    INTERNSHIP = "INTERNSHIP"

class ExperienceLevel(enum.Enum):
    ENTRY = "ENTRY"
    MID = "MID"
    SENIOR = "SENIOR"

class RemoteOption(enum.Enum):
    REMOTE = "REMOTE"
    HYBRID = "HYBRID"
    ONSITE = "ONSITE"
```

**app/models/company.py**:

```python
from datetime import datetime
from app.extensions import db

class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    website = db.Column(db.String(255))
    location = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=0, nullable=False)

    jobs = db.relationship('Job', back_populates='company', cascade='all, delete-orphan', lazy='dynamic')
```

**app/models/job.py**:

```python
from datetime import datetime
from app.extensions import db
from app.models.enums import JobType, ExperienceLevel, RemoteOption

class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company_id = db.Column(db.BigInteger, db.ForeignKey('company.id', ondelete='CASCADE'), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    salary_min = db.Column(db.Numeric(10, 2))
    salary_max = db.Column(db.Numeric(10, 2))
    job_type = db.Column(db.Enum(JobType), nullable=False)
    experience_level = db.Column(db.Enum(ExperienceLevel), nullable=False)
    remote_option = db.Column(db.Enum(RemoteOption), nullable=False)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expiry_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    application_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=0, nullable=False)

    company = db.relationship('Company', back_populates='jobs')
```

### Migrations

**migrations/run_migrations.py**:

```python
import os
import sys
import psycopg2
from pathlib import Path

def get_db_connection():
    db_url = os.getenv('DATABASE_URL', 'postgresql://admin:admin123@localhost:5432/job_board')
    parts = db_url.replace('postgresql://', '').split('@')
    user_pass = parts[0].split(':')
    host_port_db = parts[1].split('/')
    host_port = host_port_db[0].split(':')

    return psycopg2.connect(
        user=user_pass[0],
        password=user_pass[1],
        host=host_port[0],
        port=host_port[1],
        database=host_port_db[1]
    )

def run_migrations():
    migrations_dir = Path(__file__).parent
    migration_files = sorted(migrations_dir.glob('*.sql'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        for migration_file in migration_files:
            print(f"Running migration: {migration_file.name}")
            with open(migration_file, 'r') as f:
                cursor.execute(f.read())
                conn.commit()
            print(f"✓ Completed: {migration_file.name}")
        print("\n✓ All migrations completed!")
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Migration failed: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    run_migrations()
```

### Application Factory (app/**init**.py)

```python
from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import singleton

from app.extensions import db, ma, api
from config import config

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    CORS(app)

    # Register blueprints
    from app.routes.jobs import jobs_blp
    from app.routes.companies import companies_blp

    api.register_blueprint(jobs_blp)
    api.register_blueprint(companies_blp)

    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Setup dependency injection
    configure_injector(app)

    return app

def configure_injector(app):
    from app.repositories.job_repository import JobRepository
    from app.repositories.company_repository import CompanyRepository
    from app.services.job_service import JobService
    from app.services.company_service import CompanyService

    def configure(binder):
        binder.bind(JobRepository, to=JobRepository, scope=singleton)
        binder.bind(CompanyRepository, to=CompanyRepository, scope=singleton)
        binder.bind(JobService, to=JobService, scope=singleton)
        binder.bind(CompanyService, to=CompanyService, scope=singleton)

    FlaskInjector(app=app, modules=[configure])
```

### Layered Architecture

**Repository Layer** (app/repositories/job_repository.py):

```python
from typing import List, Optional
from sqlalchemy.orm import joinedload
from app.extensions import db
from app.models.job import Job

class JobRepository:
    def find_all(self) -> List[Job]:
        return Job.query.options(joinedload(Job.company)).all()

    def find_by_id(self, job_id: int) -> Optional[Job]:
        return Job.query.options(joinedload(Job.company)).get(job_id)

    def save(self, job: Job) -> Job:
        db.session.add(job)
        db.session.commit()
        db.session.refresh(job)
        return job

    def delete(self, job: Job) -> None:
        db.session.delete(job)
        db.session.commit()
```

**Service Layer** (app/services/job_service.py):

```python
from typing import List
from injector import inject
from app.repositories.job_repository import JobRepository
from app.repositories.company_repository import CompanyRepository
from app.models.job import Job
from app.models.enums import JobType, ExperienceLevel, RemoteOption
from app.exceptions.custom_exceptions import JobNotFoundException, CompanyNotFoundException

class JobService:
    @inject
    def __init__(self, job_repository: JobRepository, company_repository: CompanyRepository):
        self.job_repository = job_repository
        self.company_repository = company_repository

    def get_all_jobs(self) -> List[Job]:
        return self.job_repository.find_all()

    def get_job_by_id(self, job_id: int) -> Job:
        job = self.job_repository.find_by_id(job_id)
        if not job:
            raise JobNotFoundException(job_id)
        return job

    def create_job(self, data: dict) -> Job:
        company = self.company_repository.find_by_id(data['company_id'])
        if not company:
            raise CompanyNotFoundException(data['company_id'])

        job = Job(
            title=data['title'],
            description=data['description'],
            company_id=data['company_id'],
            location=data['location'],
            salary_min=data.get('salary_min'),
            salary_max=data.get('salary_max'),
            job_type=JobType[data['job_type']],
            experience_level=ExperienceLevel[data['experience_level']],
            remote_option=RemoteOption[data['remote_option']],
            expiry_date=data.get('expiry_date'),
            application_url=data.get('application_url')
        )
        return self.job_repository.save(job)

    def update_job(self, job_id: int, data: dict) -> Job:
        job = self.get_job_by_id(job_id)

        for key, value in data.items():
            if key in ['job_type', 'experience_level', 'remote_option']:
                setattr(job, key, eval(key.title().replace('_', ''))[value])
            elif hasattr(job, key):
                setattr(job, key, value)

        return self.job_repository.save(job)

    def delete_job(self, job_id: int) -> None:
        job = self.get_job_by_id(job_id)
        self.job_repository.delete(job)
```

**Controller Layer** (app/routes/jobs.py):

```python
from flask.views import MethodView
from flask_smorest import Blueprint
from injector import inject
from app.services.job_service import JobService
from app.schemas.job_schema import JobSchema, JobDetailSchema, JobCreateSchema, JobUpdateSchema

jobs_blp = Blueprint('jobs', 'jobs', url_prefix='/api/jobs', description='Job operations')

@jobs_blp.route('/')
class JobList(MethodView):
    @inject
    def __init__(self, job_service: JobService):
        self.job_service = job_service

    @jobs_blp.response(200, JobSchema(many=True))
    def get(self):
        """Get all jobs"""
        return self.job_service.get_all_jobs()

    @jobs_blp.arguments(JobCreateSchema)
    @jobs_blp.response(201, JobSchema)
    def post(self, job_data):
        """Create a new job"""
        return self.job_service.create_job(job_data)

@jobs_blp.route('/<int:job_id>')
class JobDetail(MethodView):
    @inject
    def __init__(self, job_service: JobService):
        self.job_service = job_service

    @jobs_blp.response(200, JobDetailSchema)
    def get(self, job_id):
        """Get job by ID"""
        return self.job_service.get_job_by_id(job_id)

    @jobs_blp.arguments(JobUpdateSchema)
    @jobs_blp.response(200, JobSchema)
    def patch(self, job_data, job_id):
        """Update job"""
        return self.job_service.update_job(job_id, job_data)

    @jobs_blp.response(204)
    def delete(self, job_id):
        """Delete job"""
        self.job_service.delete_job(job_id)
        return ''
```

### Exception Handling

**app/exceptions/custom_exceptions.py**:

```python
class JobNotFoundException(Exception):
    def __init__(self, job_id: int):
        super().__init__(f"Job not found with id: {job_id}")

class CompanyNotFoundException(Exception):
    def __init__(self, company_id: int):
        super().__init__(f"Company not found with id: {company_id}")

class OptimisticLockException(Exception):
    pass

class AuthenticationException(Exception):
    pass

class InvalidFileException(Exception):
    pass
```

**app/utils/error_handlers.py**:

```python
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.orm.exc import StaleDataError
from app.exceptions.custom_exceptions import *

def register_error_handlers(app):
    @app.errorhandler(JobNotFoundException)
    def handle_job_not_found(error):
        return jsonify({'message': str(error), 'status': 404}), 404

    @app.errorhandler(CompanyNotFoundException)
    def handle_company_not_found(error):
        return jsonify({'message': str(error), 'status': 404}), 404

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({'message': 'Validation failed', 'status': 400, 'errors': error.messages}), 400

    @app.errorhandler(OptimisticLockException)
    @app.errorhandler(StaleDataError)
    def handle_optimistic_lock(error):
        return jsonify({'message': 'Resource modified by another user', 'status': 409}), 409

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        return jsonify({'message': 'An unexpected error occurred', 'status': 500}), 500
```

### Validation Schemas

**app/schemas/job_schema.py**:

```python
from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from datetime import datetime

class JobCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = fields.String(required=True)
    company_id = fields.Integer(required=True)
    location = fields.String(required=True)
    salary_min = fields.Decimal(as_string=True, allow_none=True, validate=validate.Range(min=0))
    salary_max = fields.Decimal(as_string=True, allow_none=True, validate=validate.Range(min=0))
    job_type = fields.String(required=True, validate=validate.OneOf(['FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERNSHIP']))
    experience_level = fields.String(required=True, validate=validate.OneOf(['ENTRY', 'MID', 'SENIOR']))
    remote_option = fields.String(required=True, validate=validate.OneOf(['REMOTE', 'HYBRID', 'ONSITE']))
    expiry_date = fields.DateTime(allow_none=True)
    application_url = fields.URL(allow_none=True)

    @validates_schema
    def validate_salary(self, data, **kwargs):
        if data.get('salary_min') and data.get('salary_max'):
            if data['salary_max'] < data['salary_min']:
                raise ValidationError('salary_max must be >= salary_min')

    @validates_schema
    def validate_expiry(self, data, **kwargs):
        if data.get('expiry_date') and data['expiry_date'] <= datetime.utcnow():
            raise ValidationError('expiry_date must be in the future')

class JobUpdateSchema(Schema):
    # All fields optional for PATCH
    title = fields.String(validate=validate.Length(min=1, max=255))
    description = fields.String()
    # ... other fields as optional
```

### Phase I Acceptance Criteria

- [ ] Docker Compose starts all services (Postgres, RabbitMQ, Flask)
- [ ] Application connects to database
- [ ] All CRUD endpoints functional (GET, POST, PATCH, DELETE)
- [ ] Validation errors return 400 with field details
- [ ] Not found errors return 404
- [ ] Optimistic locking handles concurrent updates (409)
- [ ] Swagger UI accessible at /swagger
- [ ] Foreign key constraints enforced
- [ ] Timestamps auto-populate

---

## Phase II: Advanced Routes

### Search & Filtering

**Update app/repositories/job_repository.py**:

```python
from sqlalchemy import or_

class JobRepository:
    # ... existing methods ...

    def search_jobs(self, keyword=None, location=None, company_id=None,
                   job_type=None, experience_level=None, remote_option=None,
                   min_salary=None, max_salary=None, is_active=True,
                   page=1, per_page=20):
        query = Job.query.options(joinedload(Job.company))

        if keyword:
            query = query.filter(or_(
                Job.title.ilike(f"%{keyword}%"),
                Job.description.ilike(f"%{keyword}%")
            ))
        if location:
            query = query.filter(Job.location.ilike(f"%{location}%"))
        if company_id:
            query = query.filter(Job.company_id == company_id)
        if job_type:
            query = query.filter(Job.job_type == job_type)
        if experience_level:
            query = query.filter(Job.experience_level == experience_level)
        if remote_option:
            query = query.filter(Job.remote_option == remote_option)
        if min_salary:
            query = query.filter(Job.salary_max >= min_salary)
        if max_salary:
            query = query.filter(Job.salary_min <= max_salary)
        if is_active is not None:
            query = query.filter(Job.is_active == is_active)

        return query.paginate(page=page, per_page=per_page, error_out=False)

    def find_active_jobs(self, page=1, per_page=20):
        from datetime import datetime
        now = datetime.utcnow()
        return Job.query.options(joinedload(Job.company)).filter(
            Job.is_active == True,
            or_(Job.expiry_date == None, Job.expiry_date > now)
        ).paginate(page=page, per_page=per_page, error_out=False)
```

### New Endpoints

**Add to app/routes/jobs.py**:

```python
from flask import request

@jobs_blp.route('/search')
class JobSearch(MethodView):
    @inject
    def __init__(self, job_service: JobService):
        self.job_service = job_service

    @jobs_blp.response(200)
    def get(self):
        """Search jobs with filters"""
        params = {
            'keyword': request.args.get('keyword'),
            'location': request.args.get('location'),
            'company_id': request.args.get('company_id', type=int),
            'job_type': request.args.get('job_type'),
            'experience_level': request.args.get('experience_level'),
            'remote_option': request.args.get('remote_option'),
            'min_salary': request.args.get('min_salary', type=float),
            'max_salary': request.args.get('max_salary', type=float),
            'page': request.args.get('page', default=1, type=int),
            'per_page': min(request.args.get('per_page', default=20, type=int), 100)
        }
        return self.job_service.search_jobs(**params)

@jobs_blp.route('/active')
class ActiveJobs(MethodView):
    @inject
    def __init__(self, job_service: JobService):
        self.job_service = job_service

    @jobs_blp.response(200)
    def get(self):
        """Get active, non-expired jobs"""
        page = request.args.get('page', default=1, type=int)
        per_page = min(request.args.get('per_page', default=20, type=int), 100)
        return self.job_service.get_active_jobs(page, per_page)

@jobs_blp.route('/<int:job_id>/deactivate')
class DeactivateJob(MethodView):
    @inject
    def __init__(self, job_service: JobService):
        self.job_service = job_service

    @jobs_blp.response(200)
    def post(self, job_id):
        """Deactivate job (soft delete)"""
        self.job_service.deactivate_job(job_id)
        return {'message': 'Job successfully deactivated', 'job_id': job_id}
```

### Phase II Acceptance Criteria

- [ ] Search endpoint works with all filter combinations
- [ ] Pagination works correctly
- [ ] Active jobs endpoint returns only active, non-expired jobs
- [ ] Deactivate sets is_active to false
- [ ] Page size capped at 100
- [ ] Empty results return empty page, not 404

---

## Phase III: Testing

### Test Configuration (tests/conftest.py)

```python
import pytest
from app import create_app
from app.extensions import db
from app.models.company import Company
from app.models.job import Job
from app.models.enums import JobType, ExperienceLevel, RemoteOption

@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def db_session(app):
    with app.app_context():
        db.session.query(Job).delete()
        db.session.query(Company).delete()
        db.session.commit()
        yield db.session
        db.session.rollback()

@pytest.fixture
def sample_company(db_session):
    company = Company(name='Test Co', location='NYC')
    db_session.add(company)
    db_session.commit()
    return company

@pytest.fixture
def sample_job(db_session, sample_company):
    job = Job(
        title='Software Engineer',
        description='Build things',
        company_id=sample_company.id,
        location='NYC',
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.MID,
        remote_option=RemoteOption.HYBRID
    )
    db_session.add(job)
    db_session.commit()
    return job
```

### Test Examples

**Unit Test (tests/unit/test_job_service.py)**:

```python
from unittest.mock import Mock
import pytest
from app.services.job_service import JobService
from app.exceptions.custom_exceptions import JobNotFoundException

def test_get_job_by_id_not_found():
    job_repo = Mock()
    company_repo = Mock()
    job_repo.find_by_id.return_value = None

    service = JobService(job_repo, company_repo)

    with pytest.raises(JobNotFoundException):
        service.get_job_by_id(999)
```

**Integration Test (tests/integration/test_job_repository.py)**:

```python
def test_search_jobs_by_keyword(db_session, sample_company):
    from app.repositories.job_repository import JobRepository

    job = Job(title='Python Developer', description='Python needed',
              company_id=sample_company.id, location='NYC',
              job_type=JobType.FULL_TIME, experience_level=ExperienceLevel.MID,
              remote_option=RemoteOption.HYBRID)
    db_session.add(job)
    db_session.commit()

    repo = JobRepository()
    result = repo.search_jobs(keyword='Python')

    assert result.total == 1
    assert result.items[0].title == 'Python Developer'
```

**API Test (tests/api/test_job_routes.py)**:

```python
import json

def test_get_all_jobs(client, sample_job):
    response = client.get('/api/jobs')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_create_job_invalid_data(client):
    response = client.post('/api/jobs',
        data=json.dumps({'title': ''}),
        content_type='application/json')
    assert response.status_code == 400
```

### Running Tests

**pytest.ini**:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = --verbose --cov=app --cov-report=html --cov-fail-under=80
```

Commands:

```bash
pytest                          # Run all tests
pytest --cov=app               # With coverage
pytest tests/unit/             # Unit tests only
```

### Phase III Acceptance Criteria

- [ ] Unit tests for all service methods
- [ ] Integration tests for repository queries
- [ ] API tests for all endpoints
- [ ] Tests cover happy path and error cases
- [ ] 80%+ test coverage achieved
- [ ] All tests pass consistently

---

## Phase IV: Advanced Features

### 1. Authentication

**User Model (app/models/user.py)**:

```python
from datetime import datetime
import bcrypt
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # ADMIN, RECRUITER, JOB_SEEKER
    enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
```

**JWT Setup (add to app/**init**.py)**:

```python
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app(config_name='development'):
    # ... existing code ...
    jwt.init_app(app)

    from app.routes.auth import auth_blp
    api.register_blueprint(auth_blp)
```

**Auth Routes (app/routes/auth.py)**:

```python
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User

auth_blp = Blueprint('auth', 'auth', url_prefix='/api/auth')

@auth_blp.route('/register')
class Register(MethodView):
    def post(self):
        # Registration logic
        pass

@auth_blp.route('/login')
class Login(MethodView):
    def post(self):
        # Login and return JWT
        pass

@auth_blp.route('/me')
class CurrentUser(MethodView):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        # Return user info
        pass
```

**Role-based Access (app/utils/decorators.py)**:

```python
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def role_required(*required_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('role') not in required_roles:
                return jsonify({'message': 'Insufficient permissions'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
```

### 2. File Upload

**File Storage Service (app/services/file_storage_service.py)**:

```python
import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

class FileStorageService:
    def __init__(self, upload_dir='./uploads/resumes'):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    def save_file(self, file) -> str:
        if not self.allowed_file(file.filename):
            raise Exception("File type not allowed")

        filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}"
        filepath = os.path.join(self.upload_dir, filename)
        file.save(filepath)
        return filepath

    def allowed_file(self, filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

### 3. Application Entity

**Application Model (app/models/application.py)**:

```python
from datetime import datetime
from app.extensions import db

class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.BigInteger, primary_key=True)
    job_id = db.Column(db.BigInteger, db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    resume_path = db.Column(db.String(500))
    cover_letter = db.Column(db.Text)
    status = db.Column(db.String(50), default='PENDING')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    version = db.Column(db.Integer, default=0)

    __table_args__ = (db.UniqueConstraint('job_id', 'user_id'),)
```

### 4. Celery Tasks

**Celery App (app/celery_app.py)**:

```python
from celery import Celery
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )

    celery.conf.beat_schedule = {
        'expire-old-jobs': {
            'task': 'app.tasks.expire_old_jobs',
            'schedule': crontab(hour=2, minute=0),
        },
    }

    return celery
```

**Tasks (app/tasks.py)**:

```python
from datetime import datetime
from app.celery_app import make_celery
from app import create_app
from app.extensions import db
from app.models.job import Job

app = create_app()
celery = make_celery(app)

@celery.task(name='app.tasks.expire_old_jobs')
def expire_old_jobs():
    with app.app_context():
        now = datetime.utcnow()
        expired = Job.query.filter(
            Job.is_active == True,
            Job.expiry_date != None,
            Job.expiry_date < now
        ).all()

        for job in expired:
            job.is_active = False

        db.session.commit()
        return len(expired)
```

### Phase IV Acceptance Criteria

- [ ] Users can register and login
- [ ] JWT tokens issued and validated
- [ ] Role-based access control works
- [ ] File upload validates type and size
- [ ] Users can apply to jobs
- [ ] Duplicate applications prevented
- [ ] Celery task expires old jobs daily
- [ ] All services containerized and running

---

## API Endpoints Summary

### Jobs

- `GET /api/jobs` - List all jobs (paginated)
- `GET /api/jobs/{id}` - Get job details
- `POST /api/jobs` - Create job (auth: ADMIN, RECRUITER)
- `PATCH /api/jobs/{id}` - Update job (auth: ADMIN, RECRUITER)
- `DELETE /api/jobs/{id}` - Delete job (auth: ADMIN, RECRUITER)
- `GET /api/jobs/search` - Search with filters
- `GET /api/jobs/active` - Active jobs only
- `POST /api/jobs/{id}/deactivate` - Soft delete

### Companies

- `GET /api/companies` - List all companies
- `GET /api/companies/{id}` - Get company details
- `POST /api/companies` - Create company (auth: ADMIN, RECRUITER)
- `PATCH /api/companies/{id}` - Update company
- `DELETE /api/companies/{id}` - Delete company

### Auth

- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login (returns JWT)
- `GET /api/auth/me` - Current user info (auth required)

### Applications (Phase IV)

- `POST /api/applications` - Apply to job (auth required)
- `GET /api/applications/my-applications` - User's applications
- `GET /api/applications/job/{id}` - Applications for job (recruiter)
- `PATCH /api/applications/{id}/status` - Update status (recruiter)

---

## Development Workflow

### Setup

```bash
# Clone and setup
git clone <repo>
cd job-board-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start services
docker-compose up -d

# Run migrations
python migrations/run_migrations.py

# Start app
flask run
```

### Development

```bash
# Run app with hot-reload
docker-compose up

# Run tests
pytest

# Run Celery worker (separate terminal)
celery -A app.tasks.celery worker --loglevel=info

# Run Celery beat (separate terminal)
celery -A app.tasks.celery beat --loglevel=info
```

### Access Points

- API: http://localhost:5000
- Swagger UI: http://localhost:5000/swagger
- RabbitMQ Management: http://localhost:15672 (admin/admin123)

---

## Stretch Goals

1. **Connection Pooling**: Configure SQLAlchemy connection pool settings
2. **Caching**: Add Redis for caching frequently accessed data
3. **Rate Limiting**: Implement API rate limiting with Flask-Limiter
4. **Logging**: Structured logging with correlation IDs
5. **Monitoring**: Add Prometheus metrics
6. **Email Notifications**: Send emails on application status changes
7. **Full-text Search**: PostgreSQL full-text search or Elasticsearch
8. **API Versioning**: Version the API (v1, v2)
9. **CI/CD Pipeline**: GitHub Actions for automated testing
10. **Documentation**: Comprehensive README and API docs

---

## Timeline Estimate

- **Phase I**: 3-4 days (Setup + CRUD)
- **Phase II**: 2-3 days (Advanced routes)
- **Phase III**: 2-3 days (Testing)
- **Phase IV**: 4-5 days (Auth + Files + Celery)

**Total**: 11-15 days

---

## Success Metrics

- All endpoints functional and tested
- 80%+ test coverage
- No N+1 query problems (use joinedload)
- API response time < 200ms for simple queries
- All services running in Docker
- Swagger docs complete and accurate
- Clean separation of concerns (layered architecture)

---

## Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [Marshmallow Docs](https://marshmallow.readthedocs.io/)
- [Flask-SMOREST](https://flask-smorest.readthedocs.io/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [pytest Documentation](https://docs.pytest.org/)

---
