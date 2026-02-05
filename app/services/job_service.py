from typing import List

from injector import inject
from sqlalchemy.orm.exc import StaleDataError

from app.exceptions.custom_exceptions import (
    CompanyNotFoundException,
    JobNotFoundException,
    OptimisticLockException,
)
from app.models.enums import ExperienceLevel, JobType, RemoteOption
from app.models.job import Job
from app.repositories.company_repository import CompanyRepository
from app.repositories.job_repository import JobRepository


class JobService:
    @inject
    def __init__(
        self,
        job_repository: JobRepository,
        company_repository: CompanyRepository,
    ):
        self.job_repository = job_repository
        self.company_repository = company_repository

    def get_all_jobs(self) -> List[Job]:
        return self.job_repository.find_all()

    def get_job_by_id(self, job_id: int) -> Job:
        job = self.job_repository.find_by_id(job_id)
        if not job:
            raise JobNotFoundException(job_id)
        return job

    def create_job(self, data: dict) -> Job:
        company = self.company_repository.find_by_id(data["company_id"])
        if not company:
            raise CompanyNotFoundException(data["company_id"])

        job = Job(
            title=data["title"],
            description=data["description"],
            company_id=data["company_id"],
            location=data["location"],
            salary_min=data.get("salary_min"),
            salary_max=data.get("salary_max"),
            job_type=JobType[data["job_type"]],
            experience_level=ExperienceLevel[data["experience_level"]],
            remote_option=RemoteOption[data["remote_option"]],
            expiry_date=data.get("expiry_date"),
            application_url=data.get("application_url"),
        )
        return self.job_repository.save(job)

    def update_job(self, job_id: int, data: dict) -> Job:
        job = self.get_job_by_id(job_id)

        if "company_id" in data:
            company = self.company_repository.find_by_id(data["company_id"])
            if not company:
                raise CompanyNotFoundException(data["company_id"])

        enum_keys = {
            "job_type": JobType,
            "experience_level": ExperienceLevel,
            "remote_option": RemoteOption,
        }
        for key, value in data.items():
            if key in enum_keys:
                setattr(job, key, enum_keys[key][value])
            elif hasattr(job, key):
                setattr(job, key, value)

        try:
            return self.job_repository.save(job)
        except StaleDataError:
            raise OptimisticLockException()

    def delete_job(self, job_id: int) -> None:
        job = self.get_job_by_id(job_id)
        self.job_repository.delete(job)
