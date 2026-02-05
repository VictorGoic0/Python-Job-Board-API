# System Patterns: Job Board API

## Architecture

- **Layered**: Routes (controllers) → Services (business logic) → Repositories (data access) → Models (SQLAlchemy).
- **Dependency injection**: Flask-Injector; repositories and services bound in app factory, injected into route classes.
- **API surface**: Flask-SMOREST blueprints; OpenAPI 3.0.2; Swagger UI at `/swagger`.

## Key Technical Decisions

- **Database**: PostgreSQL; raw SQL migrations via Python runner (no Alembic in PRD); version column for optimistic locking.
- **Validation**: Marshmallow schemas (DTOs); used for request/response and validation errors (400 with field details).
- **Errors**: Custom exceptions (e.g. JobNotFoundException, CompanyNotFoundException); central error handlers (404, 400, 409, 500); StaleDataError → 409 for optimistic lock.
- **Async work**: Celery with RabbitMQ; app and workers share same codebase; beat for scheduled tasks (e.g. expire jobs).

## Design Patterns in Use

- **Repository**: Encapsulate all DB access; return domain objects or pagination objects.
- **Service**: Orchestrate repositories and business rules; raise domain exceptions.
- **Application factory**: `create_app(config_name)`; register blueprints, extensions, error handlers, injector.
- **Optimistic locking**: `version` on Company and Job; increment on update; conflict → 409.

## Component Relationships

- **app/routes**: Blueprints (jobs, companies, auth). MethodView classes; inject services; use SMOREST decorators for schema and responses.
- **app/services**: Inject repositories; implement create/update/delete/search; validate existence (e.g. company_id) and throw not-found.
- **app/repositories**: Use SQLAlchemy models; `joinedload` to avoid N+1 (e.g. Job.company).
- **app/models**: SQLAlchemy models + enums (JobType, ExperienceLevel, RemoteOption).
- **app/schemas**: Marshmallow request/response schemas; validation rules (length, one_of, salary range, expiry in future).
- **app/exceptions** + **app/utils/error_handlers**: Domain exceptions and Flask error handlers.

## Project Layout (from PRD)

```
app/
  __init__.py, extensions.py
  models/     (company, job, user, application, enums)
  schemas/    (company, job, auth, pagination)
  repositories/
  services/
  routes/     (companies, jobs, auth)
  exceptions/
  utils/      (error_handlers, decorators)
migrations/   (SQL files + run_migrations.py)
tests/        (conftest, unit, integration, api)
docker/       Dockerfile
docker-compose.yml, config.py, run.py, requirements.txt, pytest.ini, .env.example
```
