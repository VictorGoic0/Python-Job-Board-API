# Product Context: Job Board API

## Why This Project Exists

Provides a backend API for job board platforms: employers post jobs, job seekers search and apply. The API is the single source of truth for jobs, companies, users, and applications.

## Problems It Solves

- **Publishers/recruiters**: Create and manage company profiles and job postings; control visibility (active/expired, deactivate).
- **Job seekers**: Discover jobs via search and filters; apply with resume/cover letter; track application status.
- **Integrators**: Consume a stable, documented REST API (OpenAPI/Swagger) with consistent errors and pagination.

## How It Should Work

1. **Companies**: CRUD for companies (name, description, website, location). Jobs belong to a company; deleting a company cascades to its jobs.
2. **Jobs**: Full CRUD; required fields (title, description, company_id, location, job_type, experience_level, remote_option); optional salary range, expiry, application_url. Search by keyword, location, company, type/level/remote, salary; pagination; “active only” and “deactivate” semantics.
3. **Auth**: Register/login; JWT access (and optional refresh); roles (ADMIN, RECRUITER, JOB_SEEKER) for access control.
4. **Applications**: Job seekers apply to jobs (resume upload, cover letter); unique per job per user; status workflow; recruiters list/update status.
5. **Background**: Celery task (e.g. daily) marks expired jobs inactive.

## User Experience Goals

- **API consumers**: Predictable JSON, clear 4xx/5xx and validation messages, pagination, Swagger that matches behavior.
- **Developers**: Layered codebase, dependency injection, tests (unit, integration, API), single-command Docker run and migrations.
