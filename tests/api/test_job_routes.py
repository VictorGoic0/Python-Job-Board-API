"""API tests for Job routes (require test DB)."""
from datetime import datetime, timezone, timedelta

import pytest


def _valid_job_payload(company_id: int):
    return {
        "title": "Software Engineer",
        "description": "Backend development",
        "company_id": company_id,
        "location": "Remote",
        "job_type": "FULL_TIME",
        "experience_level": "MID",
        "remote_option": "REMOTE",
    }


def test_get_jobs_returns_200_and_list_with_company_data(client, sample_job, sample_company):
    response = client.get("/api/jobs/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    job = next((j for j in data if j["id"] == sample_job.id), None)
    assert job is not None
    assert "company" in job
    assert job["company"]["id"] == sample_company.id
    assert job["company"]["name"] == sample_company.name


def test_get_job_by_id_returns_200_and_full_details(client, sample_job, sample_company):
    response = client.get(f"/api/jobs/{sample_job.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == sample_job.id
    assert data["title"] == sample_job.title
    assert "company" in data
    assert data["company"]["id"] == sample_company.id


def test_get_job_by_invalid_id_returns_404(client):
    response = client.get("/api/jobs/99999")
    assert response.status_code == 404


def test_post_jobs_with_valid_data_returns_201(client, sample_company):
    response = client.post(
        "/api/jobs/",
        json=_valid_job_payload(sample_company.id),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Software Engineer"
    assert data["company_id"] == sample_company.id
    assert "id" in data


def test_post_jobs_with_invalid_company_id_returns_404(client):
    response = client.post(
        "/api/jobs/",
        json=_valid_job_payload(99999),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 404


def test_post_jobs_with_missing_required_fields_returns_400(client, sample_company):
    response = client.post(
        "/api/jobs/",
        json={"title": "Job", "company_id": sample_company.id},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400


def test_post_jobs_with_invalid_enum_values_returns_400(client, sample_company):
    payload = _valid_job_payload(sample_company.id)
    payload["job_type"] = "INVALID_TYPE"
    response = client.post(
        "/api/jobs/",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400


def test_post_jobs_with_salary_max_lt_min_returns_400(client, sample_company):
    payload = _valid_job_payload(sample_company.id)
    payload["salary_min"] = 100000
    payload["salary_max"] = 50000
    response = client.post(
        "/api/jobs/",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400


def test_post_jobs_with_past_expiry_date_returns_400(client, sample_company):
    payload = _valid_job_payload(sample_company.id)
    past = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    payload["expiry_date"] = past
    response = client.post(
        "/api/jobs/",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400


def test_patch_job_with_valid_data_returns_200(client, sample_job):
    response = client.patch(
        f"/api/jobs/{sample_job.id}",
        json={"title": "Updated Title"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Updated Title"


def test_patch_job_updates_only_provided_fields(client, sample_job):
    original_description = sample_job.description
    response = client.patch(
        f"/api/jobs/{sample_job.id}",
        json={"title": "Only Title Updated"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Only Title Updated"
    assert data["description"] == original_description


def test_patch_job_invalid_id_returns_404(client):
    response = client.patch(
        "/api/jobs/99999",
        json={"title": "X"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 404


def test_delete_job_returns_204(client, sample_job):
    response = client.delete(f"/api/jobs/{sample_job.id}")
    assert response.status_code == 204


def test_delete_job_invalid_id_returns_404(client):
    response = client.delete("/api/jobs/99999")
    assert response.status_code == 404
