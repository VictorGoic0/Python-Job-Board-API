from flask.views import MethodView
from flask_smorest import Blueprint
from injector import inject

from app.schemas.company_schema import (
    CompanyCreateSchema,
    CompanySchema,
    CompanyUpdateSchema,
)
from app.services.company_service import CompanyService


companies_blp = Blueprint(
    "companies",
    "companies",
    url_prefix="/api/companies",
    description="Company operations",
)


@companies_blp.route("/")
class CompanyList(MethodView):
    @inject
    def __init__(self, company_service: CompanyService):
        self.company_service = company_service

    @companies_blp.response(200, CompanySchema(many=True))
    def get(self):
        companies = self.company_service.get_all_companies()
        return companies

    @companies_blp.arguments(CompanyCreateSchema)
    @companies_blp.response(201, CompanySchema)
    def post(self, company_data, **_):
        company = self.company_service.create_company(company_data)
        return company, 201


@companies_blp.route("/<int:company_id>")
class CompanyDetail(MethodView):
    @inject
    def __init__(self, company_service: CompanyService):
        self.company_service = company_service

    @companies_blp.response(200, CompanySchema)
    def get(self, company_id):
        company = self.company_service.get_company_by_id(company_id)
        return company

    @companies_blp.arguments(CompanyUpdateSchema)
    @companies_blp.response(200, CompanySchema)
    def patch(self, company_data, company_id, **_):
        company = self.company_service.update_company(company_id, company_data)
        return company

    @companies_blp.response(204)
    def delete(self, company_id):
        self.company_service.delete_company(company_id)
        return "", 204
