from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.job import Job


class JobRepository:
    def find_all(self) -> List[Job]:
        result = db.session.execute(
            select(Job).options(joinedload(Job.company))
        )
        return list(result.unique().scalars().all())

    def find_by_id(self, job_id: int) -> Optional[Job]:
        result = db.session.execute(
            select(Job)
            .where(Job.id == job_id)
            .options(joinedload(Job.company))
        )
        return result.unique().scalar_one_or_none()

    def find_by_company_id(self, company_id: int) -> List[Job]:
        result = db.session.execute(
            select(Job)
            .where(Job.company_id == company_id)
            .options(joinedload(Job.company))
        )
        return list(result.unique().scalars().all())

    def save(self, job: Job) -> Job:
        db.session.add(job)
        db.session.commit()
        db.session.refresh(job)
        return job

    def delete(self, job: Job) -> None:
        db.session.delete(job)
        db.session.commit()
