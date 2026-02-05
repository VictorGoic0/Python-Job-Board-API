from marshmallow import Schema, fields, validate, validates_schema, ValidationError

from app.models.enums import ExperienceLevel, JobType, RemoteOption
from app.schemas.company_schema import CompanySummarySchema
from app.utils.datetime_utils import utc_now

ENUM_JOB_TYPE = [e.value for e in JobType]
ENUM_EXPERIENCE_LEVEL = [e.value for e in ExperienceLevel]
ENUM_REMOTE_OPTION = [e.value for e in RemoteOption]


class JobSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    description = fields.String()
    company_id = fields.Integer()
    location = fields.String()
    salary_min = fields.Decimal(as_string=True, allow_none=True)
    salary_max = fields.Decimal(as_string=True, allow_none=True)
    job_type = fields.Enum(JobType, by_value=True)
    experience_level = fields.Enum(ExperienceLevel, by_value=True)
    remote_option = fields.Enum(RemoteOption, by_value=True)
    posted_date = fields.DateTime(dump_only=True)
    expiry_date = fields.DateTime(allow_none=True)
    is_active = fields.Boolean()
    application_url = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    version = fields.Integer(dump_only=True)
    company = fields.Nested(CompanySummarySchema, dump_only=True)


class JobDetailSchema(JobSchema):
    pass


class JobCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = fields.String(required=True)
    company_id = fields.Integer(required=True)
    location = fields.String(required=True)
    salary_min = fields.Decimal(as_string=True, allow_none=True, validate=validate.Range(min=0))
    salary_max = fields.Decimal(as_string=True, allow_none=True, validate=validate.Range(min=0))
    job_type = fields.String(required=True, validate=validate.OneOf(ENUM_JOB_TYPE))
    experience_level = fields.String(required=True, validate=validate.OneOf(ENUM_EXPERIENCE_LEVEL))
    remote_option = fields.String(required=True, validate=validate.OneOf(ENUM_REMOTE_OPTION))
    expiry_date = fields.DateTime(allow_none=True)
    application_url = fields.Url(allow_none=True)

    @validates_schema
    def validate_salary_range(self, data, **kwargs):
        if data.get("salary_min") is not None and data.get("salary_max") is not None:
            if data["salary_max"] < data["salary_min"]:
                raise ValidationError({"salary_max": "salary_max must be >= salary_min"})

    @validates_schema
    def validate_expiry_future(self, data, **kwargs):
        if data.get("expiry_date") is not None and data["expiry_date"] <= utc_now():
            raise ValidationError({"expiry_date": "expiry_date must be in the future"})


class JobUpdateSchema(Schema):
    title = fields.String(validate=validate.Length(min=1, max=255))
    description = fields.String()
    company_id = fields.Integer()
    location = fields.String()
    salary_min = fields.Decimal(as_string=True, allow_none=True, validate=validate.Range(min=0))
    salary_max = fields.Decimal(as_string=True, allow_none=True, validate=validate.Range(min=0))
    job_type = fields.String(validate=validate.OneOf(ENUM_JOB_TYPE))
    experience_level = fields.String(validate=validate.OneOf(ENUM_EXPERIENCE_LEVEL))
    remote_option = fields.String(validate=validate.OneOf(ENUM_REMOTE_OPTION))
    expiry_date = fields.DateTime(allow_none=True)
    is_active = fields.Boolean()
    application_url = fields.Url(allow_none=True)

    @validates_schema
    def validate_salary_range(self, data, **kwargs):
        if data.get("salary_min") is not None and data.get("salary_max") is not None:
            if data["salary_max"] < data["salary_min"]:
                raise ValidationError({"salary_max": "salary_max must be >= salary_min"})

    @validates_schema
    def validate_expiry_future(self, data, **kwargs):
        if data.get("expiry_date") is not None and data["expiry_date"] <= utc_now():
            raise ValidationError({"expiry_date": "expiry_date must be in the future"})
