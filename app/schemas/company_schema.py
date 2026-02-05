from marshmallow import Schema, fields, validate


class CompanySummarySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    location = fields.String()


class CompanySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String(allow_none=True)
    website = fields.String(allow_none=True)
    location = fields.String()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    version = fields.Integer(dump_only=True)


class CompanyCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = fields.String(allow_none=True)
    website = fields.Url(allow_none=True)
    location = fields.String(required=True, validate=validate.Length(min=1, max=255))


class CompanyUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(min=1, max=255))
    description = fields.String(allow_none=True)
    website = fields.Url(allow_none=True)
    location = fields.String(validate=validate.Length(min=1, max=255))
