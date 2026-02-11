# Job Board API

Flask REST API for a job board (companies, jobs). Phase I: core setup, Docker, migrations, app factory.

## Setup

1. **Venv and dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Copy env**
   ```bash
   cp .env.example .env
   ```
   Adjust `DATABASE_URL`, `FLASK_APP`, etc. if needed.

3. **Start Postgres and RabbitMQ (and optionally the app)**
   ```bash
   docker-compose up -d
   ```
   This starts postgres, rabbitmq, and the Flask app container. Celery worker/beat are behind the `celery` profile and are not started by default (Phase IV).

4. **Run migrations** (venv active, Postgres running)
   ```bash
   python migrations/run_migrations.py up
   ```

## Running the app

- **With Docker**: `docker-compose up -d` runs the app on port 5000. Do **not** run `flask run` locally at the same time or you get "address already in use".
- **Without Docker app**: Stop the app container (`docker-compose stop app`) and run locally:
  ```bash
  export FLASK_APP=run_server
  flask run
  ```
  Use the same `DATABASE_URL` (e.g. Postgres in Docker) so the app can connect.

Swagger UI: http://localhost:5000/swagger  
RabbitMQ management: http://localhost:15672 (admin / admin123)

## Tests

Tests live under `tests/`: `tests/unit/` (services, schemas), `tests/integration/` (repositories, DB), `tests/api/` (HTTP endpoints). Run with venv active from the project root:

```bash
pytest                    # all tests (needs test DB for integration/api)
pytest tests/unit/ -v     # unit only (no DB)
pytest tests/unit/test_schemas.py -v   # one file
```

**Test database:** Integration and API tests use PostgreSQL database `job_board_test` (same user/password as main DB). The project does not create it automatically. To run the full suite and get ≥80% coverage:

```bash
# With Docker Postgres running:
docker exec job_board_db psql -U admin -d postgres -c "CREATE DATABASE job_board_test;"
# Or from host (psql installed):
PGPASSWORD=admin123 psql -h localhost -U admin -d postgres -c "CREATE DATABASE job_board_test;"

pytest   # 66 tests, coverage report
```

Without `job_board_test`, `pytest` still runs: 25 unit tests pass and 41 integration/API tests are skipped.

`pytest.ini` sets `pythonpath = .` and coverage options (`--cov=app --cov-fail-under=80`).

## Migrations

See [migrations/README.md](migrations/README.md). Summary: venv active, then `python migrations/run_migrations.py up` (or `status`, `down`).
