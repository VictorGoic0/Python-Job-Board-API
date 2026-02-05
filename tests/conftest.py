"""
Pytest fixtures for Phase I tests.
Requires test DB to exist (e.g. job_board_test) and schema applied (migrations or create_all).
"""
import pytest
from sqlalchemy import text

from app import create_app
from app.extensions import db
from app.models.company import Company
from app.models.job import Job
from app.models.enums import JobType, ExperienceLevel, RemoteOption


@pytest.fixture(scope="session")
def app():
    """Application with testing config (session scope)."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
    yield app


@pytest.fixture(scope="function")
def client(app):
    """Test client (function scope)."""
    with app.test_client() as c:
        yield c


@pytest.fixture(scope="function")
def db_session(app):
    """Clean database session: truncates company and job before each test (function scope)."""
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
