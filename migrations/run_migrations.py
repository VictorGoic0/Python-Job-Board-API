#!/usr/bin/env python3
"""
Simple database migration runner for raw SQL migrations.
Uses psycopg2; reads DATABASE_URL from environment.
"""
import os
import sys
from pathlib import Path

import psycopg2

MIGRATIONS_DIR = Path(__file__).resolve().parent
DEFAULT_DB_URL = "postgresql://admin:admin123@localhost:5432/job_board"


def get_connection():
    db_url = os.environ.get("DATABASE_URL", DEFAULT_DB_URL)
    return psycopg2.connect(db_url)


def ensure_migrations_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version VARCHAR(10) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                applied_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
    conn.commit()


def get_applied_migrations(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT version, name FROM schema_migrations ORDER BY version")
        return {row[0]: row[1] for row in cur.fetchall()}


def get_migration_files():
    if not MIGRATIONS_DIR.exists():
        print(f"Migrations directory not found: {MIGRATIONS_DIR}", file=sys.stderr)
        sys.exit(1)

    migrations = []
    for path in MIGRATIONS_DIR.glob("*.sql"):
        if path.name.endswith(".down.sql"):
            continue
        version = path.stem.split("_")[0]
        migrations.append((version, path.stem, path))

    return sorted(migrations, key=lambda x: x[0])


def run_migration(conn, version, stem, filepath):
    print(f"  Running {filepath.name}...", end=" ")

    try:
        with conn.cursor() as cur:
            cur.execute(filepath.read_text())
            cur.execute(
                "INSERT INTO schema_migrations (version, name) VALUES (%s, %s)",
                (version, stem),
            )
        conn.commit()
        print("OK")
        return True
    except Exception as e:
        conn.rollback()
        print("FAIL")
        print(f"    Error: {e}", file=sys.stderr)
        return False


def cmd_up(conn):
    ensure_migrations_table(conn)
    applied = get_applied_migrations(conn)
    migrations = get_migration_files()

    pending = [(v, s, p) for v, s, p in migrations if v not in applied]

    if not pending:
        print("Database is up to date - no pending migrations")
        return

    print(f"Running {len(pending)} pending migration(s):")

    for version, stem, filepath in pending:
        if not run_migration(conn, version, stem, filepath):
            print("Migration failed, stopping.", file=sys.stderr)
            sys.exit(1)

    print(f"Successfully applied {len(pending)} migration(s)")


def cmd_status(conn):
    ensure_migrations_table(conn)
    applied = get_applied_migrations(conn)
    migrations = get_migration_files()

    print("Migration status:")
    print("-" * 60)

    if not migrations:
        print("  No migration files found")
        return

    for version, stem, filepath in migrations:
        status = "Applied" if version in applied else "Pending"
        print(f"  {version}: {filepath.name:<45} {status}")

    print("-" * 60)
    pending_count = len([v for v, _, _ in migrations if v not in applied])
    print(f"  Total: {len(migrations)} | Applied: {len(applied)} | Pending: {pending_count}")


def cmd_down(conn):
    ensure_migrations_table(conn)
    applied = get_applied_migrations(conn)
    if not applied:
        print("No applied migrations to roll back")
        return

    versions_sorted = sorted(applied.keys(), reverse=True)
    last_version = versions_sorted[0]
    stem = applied[last_version]
    down_path = MIGRATIONS_DIR / f"{stem}.down.sql"

    if not down_path.exists():
        print(f"No down migration for {stem}", file=sys.stderr)
        sys.exit(1)

    print(f"Rolling back {stem}...", end=" ")

    try:
        with conn.cursor() as cur:
            cur.execute(down_path.read_text())
            cur.execute("DELETE FROM schema_migrations WHERE version = %s", (last_version,))
        conn.commit()
        print("OK")
        print("Rollback complete")
    except Exception as e:
        conn.rollback()
        print("FAIL")
        print(f"  Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_migrations.py [up|down|status]")
        print()
        print("Commands:")
        print("  up      - Run all pending migrations")
        print("  status  - Show migration status")
        print("  down    - Roll back last migration")
        sys.exit(1)

    command = sys.argv[1].lower()

    try:
        conn = get_connection()
        try:
            if command == "up":
                cmd_up(conn)
            elif command == "status":
                cmd_status(conn)
            elif command == "down":
                cmd_down(conn)
            else:
                print(f"Unknown command: {command}", file=sys.stderr)
                sys.exit(1)
        finally:
            conn.close()
    except psycopg2.Error as e:
        print(f"Database error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
