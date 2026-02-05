# Database Migrations

Raw SQL migrations with `up`, `status`, and `down`. Each migration is one file (e.g. `001_initial_schema.sql`). New tables or schema changes go in a new numbered file. Applied migrations are recorded in `schema_migrations`.

## Prerequisites

Activate the project venv and install dependencies so `psycopg2` is available:

```bash
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

PostgreSQL must be running (e.g. `docker-compose up -d postgres`). Set `DATABASE_URL` if it differs from the default (see Commands).

## Commands

From the project root (with venv active):

```bash
# Apply all pending migrations
python migrations/run_migrations.py up

# Show applied vs pending
python migrations/run_migrations.py status

# Roll back the last migration
python migrations/run_migrations.py down
```

Set `DATABASE_URL` if needed:

```bash
DATABASE_URL=postgresql://admin:admin123@localhost:5432/job_board_test python migrations/run_migrations.py up
```

## File layout

- **Up**: `001_initial_schema.sql`, `002_add_something.sql`, … (no `.down.sql` in the name). The script runs these in order and records each in `schema_migrations`.
- **Down**: `001_initial_schema.down.sql`, `002_add_something.down.sql`, … Run only when you use `down`; the script runs the last applied migration’s `.down.sql` and removes that row from `schema_migrations`.

Version is the numeric prefix (e.g. `001`). The script ignores `*.down.sql` when running `up`.

## Rollback

`down` rolls back exactly one migration (the most recently applied). It runs the matching `<stem>.down.sql` and deletes that version from `schema_migrations`. To roll back multiple steps, run `down` repeatedly or add a `down N` option later.
