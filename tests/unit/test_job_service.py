"""Unit tests for JobService with mocked JobRepository and CompanyRepository."""
import pytest
from unittest.mock import MagicMock

from app.exceptions.custom_exceptions import CompanyNotFoundException, JobNotFoundException
from app.models.enums import ExperienceLevel, JobType, RemoteOption
from app.services.job_service import JobService


@pytest.fixture
def mock_job_repository():
    return MagicMock()


@pytest.fixture
def mock_company_repository():
    return MagicMock()


@pytest.fixture
def job_service(mock_job_repository, mock_company_repository):
    return JobService(
        job_repository=mock_job_repository,
        company_repository=mock_company_repository,
    )


@pytest.fixture
def sample_company_mock():
    company = MagicMock()
    company.id = 1
    return company


@pytest.fixture
def sample_job_mock(sample_company_mock):
    job = MagicMock()
    job.id = 1
    job.title = "Test Job"
    job.description = "Desc"
    job.company_id = 1
    job.location = "City"
    job.job_type = JobType.FULL_TIME
    job.experience_level = ExperienceLevel.MID
    job.remote_option = RemoteOption.REMOTE
    job.version = 0
    return job


def test_get_all_jobs_returns_list(job_service, mock_job_repository, sample_job_mock):
    mock_job_repository.find_all.return_value = [sample_job_mock]
    result = job_service.get_all_jobs()
    assert result == [sample_job_mock]
    mock_job_repository.find_all.assert_called_once()


def test_get_job_by_id_with_existing_job(
    job_service, mock_job_repository, sample_job_mock
):
    mock_job_repository.find_by_id.return_value = sample_job_mock
    result = job_service.get_job_by_id(1)
    assert result is sample_job_mock
    mock_job_repository.find_by_id.assert_called_once_with(1)


def test_get_job_by_id_raises_job_not_found_exception(
    job_service, mock_job_repository
):
    mock_job_repository.find_by_id.return_value = None
    with pytest.raises(JobNotFoundException) as exc_info:
        job_service.get_job_by_id(999)
    assert exc_info.value.job_id == 999


def test_create_job_with_valid_data(
    job_service, mock_job_repository, mock_company_repository,
    sample_company_mock, sample_job_mock
):
    mock_company_repository.find_by_id.return_value = sample_company_mock
    mock_job_repository.save.return_value = sample_job_mock
    data = {
        "title": "New Job",
        "description": "New desc",
        "company_id": 1,
        "location": "City",
        "job_type": "FULL_TIME",
        "experience_level": "MID",
        "remote_option": "REMOTE",
    }
    result = job_service.create_job(data)
    mock_company_repository.find_by_id.assert_called_once_with(1)
    mock_job_repository.save.assert_called_once()
    saved_job = mock_job_repository.save.call_args[0][0]
    assert saved_job.title == "New Job"
    assert saved_job.description == "New desc"
    assert saved_job.company_id == 1
    assert saved_job.location == "City"
    assert saved_job.job_type == JobType.FULL_TIME
    assert saved_job.experience_level == ExperienceLevel.MID
    assert saved_job.remote_option == RemoteOption.REMOTE
    assert result is sample_job_mock


def test_create_job_raises_company_not_found_for_invalid_company_id(
    job_service, mock_company_repository
):
    mock_company_repository.find_by_id.return_value = None
    data = {
        "title": "Job",
        "description": "Desc",
        "company_id": 999,
        "location": "City",
        "job_type": "FULL_TIME",
        "experience_level": "MID",
        "remote_option": "REMOTE",
    }
    with pytest.raises(CompanyNotFoundException) as exc_info:
        job_service.create_job(data)
    assert exc_info.value.company_id == 999


def test_update_job_updates_only_provided_fields(
    job_service, mock_job_repository, sample_job_mock
):
    mock_job_repository.find_by_id.return_value = sample_job_mock
    mock_job_repository.save.return_value = sample_job_mock
    result = job_service.update_job(1, {"title": "Updated Title"})
    assert sample_job_mock.title == "Updated Title"
    mock_job_repository.save.assert_called_once_with(sample_job_mock)
    assert result is sample_job_mock


def test_update_job_validates_new_company_id(
    job_service, mock_job_repository, mock_company_repository, sample_job_mock
):
    mock_job_repository.find_by_id.return_value = sample_job_mock
    mock_company_repository.find_by_id.return_value = None
    with pytest.raises(CompanyNotFoundException) as exc_info:
        job_service.update_job(1, {"company_id": 999})
    assert exc_info.value.company_id == 999


def test_update_job_raises_job_not_found_exception(
    job_service, mock_job_repository
):
    mock_job_repository.find_by_id.return_value = None
    with pytest.raises(JobNotFoundException):
        job_service.update_job(999, {"title": "X"})


def test_delete_job_calls_repository_delete(
    job_service, mock_job_repository, sample_job_mock
):
    mock_job_repository.find_by_id.return_value = sample_job_mock
    job_service.delete_job(1)
    mock_job_repository.find_by_id.assert_called_once_with(1)
    mock_job_repository.delete.assert_called_once_with(sample_job_mock)


def test_delete_job_raises_job_not_found_exception(
    job_service, mock_job_repository
):
    mock_job_repository.find_by_id.return_value = None
    with pytest.raises(JobNotFoundException):
        job_service.delete_job(999)
