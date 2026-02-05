from typing import List, Optional

from sqlalchemy import select

from app.extensions import db
from app.models.company import Company


class CompanyRepository:
    def find_all(self) -> List[Company]:
        result = db.session.execute(select(Company))
        return list(result.scalars().all())

    def find_by_id(self, company_id: int) -> Optional[Company]:
        return db.session.get(Company, company_id)

    def find_by_name(self, name: str) -> Optional[Company]:
        result = db.session.execute(select(Company).where(Company.name == name))
        return result.scalar_one_or_none()

    def save(self, company: Company) -> Company:
        db.session.add(company)
        db.session.commit()
        db.session.refresh(company)
        return company

    def delete(self, company: Company) -> None:
        db.session.delete(company)
        db.session.commit()
