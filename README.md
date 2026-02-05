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

## Migrations

See [migrations/README.md](migrations/README.md). Summary: venv active, then `python migrations/run_migrations.py up` (or `status`, `down`).
