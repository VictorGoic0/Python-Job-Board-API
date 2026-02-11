"""
Pytest fixtures for Phase I tests.
Integration and API tests require PostgreSQL with database job_board_test (see context.md).
If the test DB is unavailable, those tests are skipped; unit tests run without DB.
"""
import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app import create_app
from app.extensions import db
from app.models.company import Company
from app.models.job import Job
from app.models.enums import JobType, ExperienceLevel, RemoteOption

# Session-wide: set by app fixture when DB connection fails (so db_session/client skip).
_db_unavailable = False


@pytest.fixture(scope="session")
def app(request):
    """Application with testing config (session scope). Creates tables if DB is reachable."""
    global _db_unavailable
    app = create_app("testing")
    with app.app_context():
        try:
            db.create_all()
        except OperationalError:
            _db_unavailable = True
    yield app


@pytest.fixture(scope="session")
def db_ready(request):
    """Skip if test DB was unavailable at session start (so API/integration tests are skipped)."""
    if _db_unavailable:
        pytest.skip("Test database unavailable (start Postgres, create job_board_test)")


@pytest.fixture(scope="function")
def client(app, db_ready):
    """Test client (function scope). Depends on db_ready so API tests skip when DB unavailable."""
    with app.test_client() as c:
        yield c


@pytest.fixture(scope="function")
def db_session(app):
    """Clean database session: truncates company and job before each test (function scope)."""
    if _db_unavailable:
        pytest.skip("Test database unavailable (start Postgres, create job_board_test)")
    with app.app_context():
        db.session.execute(text("TRUNCATE job, company RESTART IDENTITY CASCADE"))
        db.session.commit()
        yield db.session
        db.session.rollback()


@pytest.fixture
def sample_company(db_session):
    """A test company (depends on db_session)."""
    company = Company(
        name="Test Company",
        description="Test description",
        website="https://example.com",
        location="Test City",
    )
    db_session.add(company)
    db_session.commit()
    db_session.refresh(company)
    return company


@pytest.fixture
def sample_job(sample_company, db_session):
    """A test job for sample_company (depends on sample_company, db_session)."""
    job = Job(
        title="Test Job",
        description="Test job description",
        company_id=sample_company.id,
        location="Test City",
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.MID,
        remote_option=RemoteOption.REMOTE,
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)
    return job
