"""Integration tests for JobRepository (real DB, test config)."""
import pytest
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.job import Job
from app.models.enums import JobType, ExperienceLevel, RemoteOption
from app.repositories.job_repository import JobRepository


@pytest.fixture
def repo(app):
    """JobRepository; requires app for db session."""
    with app.app_context():
        yield JobRepository()


def test_find_all_returns_all_jobs_with_company_data(app, db_session, repo, sample_job, sample_company):
    with app.app_context():
        result = repo.find_all()
        assert len(result) >= 1
        job = next(j for j in result if j.id == sample_job.id)
        assert job is not None
        assert job.company is not None
        assert job.company.id == sample_company.id
        assert job.company.name == sample_company.name


def test_find_by_id_returns_job_with_company_when_exists(
    app, db_session, repo, sample_job, sample_company
):
    with app.app_context():
        result = repo.find_by_id(sample_job.id)
        assert result is not None
        assert result.id == sample_job.id
        assert result.title == sample_job.title
        assert result.company is not None
        assert result.company.id == sample_company.id


def test_find_by_id_returns_none_when_not_exists(app, db_session, repo):
    with app.app_context():
        result = repo.find_by_id(99999)
        assert result is None


def test_find_by_company_id_returns_jobs_for_specific_company(
    app, db_session, repo, sample_company, sample_job
):
    with app.app_context():
        result = repo.find_by_company_id(sample_company.id)
        assert len(result) >= 1
        ids = [j.id for j in result]
        assert sample_job.id in ids
        for j in result:
            assert j.company_id == sample_company.id


def test_save_creates_new_job(app, db_session, repo, sample_company):
    with app.app_context():
        job = Job(
            title="New Job",
            description="New desc",
            company_id=sample_company.id,
            location="City",
            job_type=JobType.PART_TIME,
            experience_level=ExperienceLevel.ENTRY,
            remote_option=RemoteOption.ONSITE,
        )
        saved = repo.save(job)
        assert saved.id is not None
        assert saved.title == "New Job"
        found = repo.find_by_id(saved.id)
        assert found is not None
        assert found.title == "New Job"


def test_save_updates_existing_job(app, db_session, repo, sample_job):
    with app.app_context():
        sample_job.title = "Updated Title"
        sample_job.description = "Updated desc"
        saved = repo.save(sample_job)
        assert saved.title == "Updated Title"
        assert saved.description == "Updated desc"
        found = repo.find_by_id(sample_job.id)
        assert found.title == "Updated Title"
        assert found.description == "Updated desc"


def test_delete_removes_job_from_database(app, db_session, repo, sample_job):
    with app.app_context():
        job_id = sample_job.id
        repo.delete(sample_job)
        assert repo.find_by_id(job_id) is None


def test_foreign_key_constraint_cannot_create_job_with_invalid_company_id(app, db_session, repo):
    with app.app_context():
        job = Job(
            title="Orphan Job",
            description="Desc",
            company_id=99999,
            location="City",
            job_type=JobType.FULL_TIME,
            experience_level=ExperienceLevel.MID,
            remote_option=RemoteOption.REMOTE,
        )
        with pytest.raises(IntegrityError):
            repo.save(job)
