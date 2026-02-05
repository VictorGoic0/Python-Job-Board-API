from typing import List

from injector import inject
from sqlalchemy.orm.exc import StaleDataError

from app.exceptions.custom_exceptions import (
    CompanyNotFoundException,
    OptimisticLockException,
)
from app.models.company import Company
from app.repositories.company_repository import CompanyRepository


class CompanyService:
    @inject
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    def get_all_companies(self) -> List[Company]:
        return self.company_repository.find_all()

    def get_company_by_id(self, company_id: int) -> Company:
        company = self.company_repository.find_by_id(company_id)
        if not company:
            raise CompanyNotFoundException(company_id)
        return company

    def create_company(self, data: dict) -> Company:
        company = Company(
            name=data["name"],
            description=data.get("description"),
            website=data.get("website"),
            location=data["location"],
        )
        return self.company_repository.save(company)

    def update_company(self, company_id: int, data: dict) -> Company:
        company = self.get_company_by_id(company_id)
        for key, value in data.items():
            if hasattr(company, key):
                setattr(company, key, value)
        try:
            return self.company_repository.save(company)
        except StaleDataError:
            raise OptimisticLockException()

    def delete_company(self, company_id: int) -> None:
        company = self.get_company_by_id(company_id)
        self.company_repository.delete(company)
