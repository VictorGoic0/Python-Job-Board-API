"""Integration tests for CompanyRepository (real DB, test config)."""
import pytest

from app.extensions import db
from app.models.company import Company
from app.repositories.company_repository import CompanyRepository


@pytest.fixture
def repo(app):
    """CompanyRepository; requires app for db session."""
    with app.app_context():
        yield CompanyRepository()


def test_find_all_returns_all_companies(app, db_session, repo):
    with app.app_context():
        c1 = Company(name="A", location="Loc1")
        c2 = Company(name="B", location="Loc2")
        db.session.add_all([c1, c2])
        db.session.commit()
        result = repo.find_all()
        assert len(result) == 2
        names = {c.name for c in result}
        assert names == {"A", "B"}


def test_find_by_id_returns_company_when_exists(app, db_session, repo, sample_company):
    with app.app_context():
        result = repo.find_by_id(sample_company.id)
        assert result is not None
        assert result.id == sample_company.id
        assert result.name == sample_company.name


def test_find_by_id_returns_none_when_not_exists(app, db_session, repo):
    with app.app_context():
        result = repo.find_by_id(99999)
        assert result is None


def test_find_by_name_returns_company(app, db_session, repo, sample_company):
    with app.app_context():
        result = repo.find_by_name(sample_company.name)
        assert result is not None
        assert result.id == sample_company.id
        assert result.name == sample_company.name


def test_save_creates_new_company(app, db_session, repo):
    with app.app_context():
        company = Company(name="New Co", location="New City")
        saved = repo.save(company)
        assert saved.id is not None
        assert saved.name == "New Co"
        assert saved.location == "New City"
        found = repo.find_by_id(saved.id)
        assert found is not None
        assert found.name == "New Co"


def test_save_updates_existing_company(app, db_session, repo, sample_company):
    with app.app_context():
        sample_company.name = "Updated Name"
        sample_company.location = "Updated City"
        saved = repo.save(sample_company)
        assert saved.name == "Updated Name"
        assert saved.location == "Updated City"
        found = repo.find_by_id(sample_company.id)
        assert found.name == "Updated Name"
        assert found.location == "Updated City"


def test_delete_removes_company_from_database(app, db_session, repo, sample_company):
    with app.app_context():
        company_id = sample_company.id
        repo.delete(sample_company)
        assert repo.find_by_id(company_id) is None


def test_cascade_delete_deleting_company_deletes_associated_jobs(
    app, db_session, repo, sample_company, sample_job
):
    with app.app_context():
        from app.repositories.job_repository import JobRepository

        job_repo = JobRepository()
        job_id = sample_job.id
        company_id = sample_company.id
        assert job_repo.find_by_id(job_id) is not None
        repo.delete(sample_company)
        assert repo.find_by_id(company_id) is None
        assert job_repo.find_by_id(job_id) is None
