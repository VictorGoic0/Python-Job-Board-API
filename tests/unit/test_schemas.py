"""PR #2 verification: schema validation and custom validators."""
from datetime import datetime, timedelta, timezone

import pytest
from marshmallow import ValidationError

from app.models.company import Company
from app.models.job import Job
from app.schemas.company_schema import CompanyCreateSchema, CompanyUpdateSchema
from app.schemas.job_schema import JobCreateSchema, JobUpdateSchema


def test_models_import():
    """Verify models can be imported (syntax and dependencies)."""
    assert Company is not None
    assert Job is not None


def test_company_create_schema_valid():
    data = {"name": "Acme", "location": "NYC"}
    schema = CompanyCreateSchema()
    result = schema.load(data)
    assert result["name"] == "Acme"
    assert result["location"] == "NYC"


def test_company_create_schema_invalid_empty_name():
    schema = CompanyCreateSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({"name": "", "location": "NYC"})
    assert "name" in exc_info.value.messages


def test_job_create_schema_valid():
    data = {
        "title": "Engineer",
        "description": "Build things",
        "company_id": 1,
        "location": "NYC",
        "job_type": "FULL_TIME",
        "experience_level": "MID",
        "remote_option": "HYBRID",
    }
    schema = JobCreateSchema()
    result = schema.load(data)
    assert result["title"] == "Engineer"
    assert result["job_type"] == "FULL_TIME"


def test_job_create_schema_salary_max_lt_min_raises():
    data = {
        "title": "Engineer",
        "description": "Build things",
        "company_id": 1,
        "location": "NYC",
        "job_type": "FULL_TIME",
        "experience_level": "MID",
        "remote_option": "HYBRID",
        "salary_min": 100,
        "salary_max": 50,
    }
    schema = JobCreateSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load(data)
    assert "salary_max" in exc_info.value.messages


def test_job_create_schema_expiry_past_raises():
    past = datetime.now(timezone.utc) - timedelta(days=1)
    data = {
        "title": "Engineer",
        "description": "Build things",
        "company_id": 1,
        "location": "NYC",
        "job_type": "FULL_TIME",
        "experience_level": "MID",
        "remote_option": "HYBRID",
        "expiry_date": past,
    }
    schema = JobCreateSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load(data)
    assert "expiry_date" in exc_info.value.messages


def test_job_update_schema_salary_validators():
    schema = JobUpdateSchema()
    with pytest.raises(ValidationError):
        schema.load({"salary_min": 100, "salary_max": 50})
