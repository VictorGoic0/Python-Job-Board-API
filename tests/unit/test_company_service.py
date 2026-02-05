"""Unit tests for CompanyService with mocked CompanyRepository."""
import pytest
from unittest.mock import MagicMock

from app.exceptions.custom_exceptions import CompanyNotFoundException
from app.services.company_service import CompanyService


@pytest.fixture
def mock_company_repository():
    return MagicMock()


@pytest.fixture
def company_service(mock_company_repository):
    return CompanyService(company_repository=mock_company_repository)


@pytest.fixture
def sample_company_mock():
    company = MagicMock()
    company.id = 1
    company.name = "Test Co"
    company.description = "Desc"
    company.website = "https://example.com"
    company.location = "City"
    company.version = 0
    return company


def test_get_all_companies_returns_list(company_service, mock_company_repository, sample_company_mock):
    mock_company_repository.find_all.return_value = [sample_company_mock]
    result = company_service.get_all_companies()
    assert result == [sample_company_mock]
    mock_company_repository.find_all.assert_called_once()


def test_get_company_by_id_with_existing_company(
    company_service, mock_company_repository, sample_company_mock
):
    mock_company_repository.find_by_id.return_value = sample_company_mock
    result = company_service.get_company_by_id(1)
    assert result is sample_company_mock
    mock_company_repository.find_by_id.assert_called_once_with(1)


def test_get_company_by_id_raises_company_not_found_exception(
    company_service, mock_company_repository
):
    mock_company_repository.find_by_id.return_value = None
    with pytest.raises(CompanyNotFoundException) as exc_info:
        company_service.get_company_by_id(999)
    assert exc_info.value.company_id == 999


def test_create_company_with_valid_data(company_service, mock_company_repository, sample_company_mock):
    mock_company_repository.save.return_value = sample_company_mock
    data = {
        "name": "New Co",
        "description": "New desc",
        "website": "https://new.com",
        "location": "New City",
    }
    result = company_service.create_company(data)
    mock_company_repository.save.assert_called_once()
    saved_company = mock_company_repository.save.call_args[0][0]
    assert saved_company.name == "New Co"
    assert saved_company.description == "New desc"
    assert saved_company.website == "https://new.com"
    assert saved_company.location == "New City"
    assert result is sample_company_mock


def test_update_company_updates_only_provided_fields(
    company_service, mock_company_repository, sample_company_mock
):
    mock_company_repository.find_by_id.return_value = sample_company_mock
    mock_company_repository.save.return_value = sample_company_mock
    result = company_service.update_company(1, {"name": "Updated Name"})
    assert sample_company_mock.name == "Updated Name"
    mock_company_repository.save.assert_called_once_with(sample_company_mock)
    assert result is sample_company_mock


def test_update_company_raises_company_not_found_exception(
    company_service, mock_company_repository
):
    mock_company_repository.find_by_id.return_value = None
    with pytest.raises(CompanyNotFoundException):
        company_service.update_company(999, {"name": "X"})


def test_delete_company_calls_repository_delete(
    company_service, mock_company_repository, sample_company_mock
):
    mock_company_repository.find_by_id.return_value = sample_company_mock
    company_service.delete_company(1)
    mock_company_repository.find_by_id.assert_called_once_with(1)
    mock_company_repository.delete.assert_called_once_with(sample_company_mock)


def test_delete_company_raises_company_not_found_exception(
    company_service, mock_company_repository
):
    mock_company_repository.find_by_id.return_value = None
    with pytest.raises(CompanyNotFoundException):
        company_service.delete_company(999)
