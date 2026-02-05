"""API tests for Company routes (require test DB)."""
import pytest


def test_get_companies_returns_200_and_list(client):
    response = client.get("/api/companies/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_company_by_id_returns_200_and_company_data(client, sample_company):
    response = client.get(f"/api/companies/{sample_company.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == sample_company.id
    assert data["name"] == sample_company.name
    assert data["location"] == sample_company.location


def test_get_company_by_invalid_id_returns_404(client):
    response = client.get("/api/companies/99999")
    assert response.status_code == 404


def test_post_companies_with_valid_data_returns_201(client):
    response = client.post(
        "/api/companies/",
        json={
            "name": "New Company",
            "description": "Desc",
            "website": "https://example.com",
            "location": "City",
        },
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "New Company"
    assert data["location"] == "City"
    assert "id" in data


def test_post_companies_with_invalid_data_returns_400(client):
    response = client.post(
        "/api/companies/",
        json={
            "name": "X",
            "description": "Desc",
            "website": "not-a-url",
            "location": "City",
        },
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "errors" in data or "message" in data


def test_post_companies_with_missing_fields_returns_400(client):
    response = client.post(
        "/api/companies/",
        json={"name": "X"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400


def test_patch_company_with_valid_data_returns_200(client, sample_company):
    response = client.patch(
        f"/api/companies/{sample_company.id}",
        json={"name": "Updated Name"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Updated Name"


def test_patch_company_updates_only_provided_fields(client, sample_company):
    original_location = sample_company.location
    response = client.patch(
        f"/api/companies/{sample_company.id}",
        json={"name": "Only Name Updated"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Only Name Updated"
    assert data["location"] == original_location


def test_patch_company_invalid_id_returns_404(client):
    response = client.patch(
        "/api/companies/99999",
        json={"name": "X"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 404


def test_delete_company_returns_204(client, sample_company):
    response = client.delete(f"/api/companies/{sample_company.id}")
    assert response.status_code == 204


def test_delete_company_invalid_id_returns_404(client):
    response = client.delete("/api/companies/99999")
    assert response.status_code == 404
