# Project Brief: Job Board API

## Purpose

Production-ready RESTful API for a job board platform. Manages job postings with full CRUD, advanced search, and proper database relationships.

## Scope

- **In scope**: REST API (Flask/Python), Company and Job entities, CRUD, search/filter, pagination, auth (JWT), applications, file upload (resumes), Celery tasks (job expiry), Docker deployment, 80%+ test coverage.
- **Out of scope**: Frontend UI, mobile apps, payment/billing, third-party job feeds (unless stretch).

## Goals

1. Deliver a complete, documented API that clients can integrate against.
2. Enforce clean layered architecture (routes → services → repositories → models).
3. Meet production standards: validation, error handling, optimistic locking, tests, containerization.
4. Expose OpenAPI/Swagger at `/swagger`.

## Phases (Source of Truth)

| Phase | Focus | Duration |
|-------|--------|----------|
| **I** | Core setup, Docker, Company/Job CRUD, migrations, error handling, Swagger | 3–4 days |
| **II** | Advanced routes: search, filters, pagination, active jobs, deactivate | 2–3 days |
| **III** | Testing: unit, integration, API tests, 80% coverage | 2–3 days |
| **IV** | Auth (JWT, roles), file upload, Application entity, Celery (expire jobs) | 4–5 days |

**Total estimate**: 11–15 days.

## Success Criteria

- All endpoints functional and tested.
- 80%+ test coverage.
- No N+1 queries (use joinedload).
- API response time < 200ms for simple queries.
- All services run in Docker.
- Swagger docs complete and accurate.
- Clear separation of concerns (layered architecture).

## Reference

- **PRD**: `PRD.md` (full product requirements).
- **Phase I tasks**: `tasks-phase1.md`.
