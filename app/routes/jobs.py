from flask.views import MethodView
from flask_smorest import Blueprint
from injector import inject

from app.schemas.job_schema import (
    JobCreateSchema,
    JobDetailSchema,
    JobSchema,
    JobUpdateSchema,
)
from app.services.job_service import JobService


jobs_blp = Blueprint(
    "jobs",
    "jobs",
    url_prefix="/api/jobs",
    description="Job operations",
)


@jobs_blp.route("/")
class JobList(MethodView):
    @inject
    def __init__(self, job_service: JobService):
        self.job_service = job_service

    @jobs_blp.response(200, JobSchema(many=True))
    def get(self):
        jobs = self.job_service.get_all_jobs()
        return jobs

    @jobs_blp.arguments(JobCreateSchema)
    @jobs_blp.response(201, JobSchema)
    def post(self, job_data, **_):
        job = self.job_service.create_job(job_data)
        return job, 201


@jobs_blp.route("/<int:job_id>")
class JobDetail(MethodView):
    @inject
    def __init__(self, job_service: JobService):
        self.job_service = job_service

    @jobs_blp.response(200, JobDetailSchema)
    def get(self, job_id):
        job = self.job_service.get_job_by_id(job_id)
        return job

    @jobs_blp.arguments(JobUpdateSchema)
    @jobs_blp.response(200, JobSchema)
    def patch(self, job_data, job_id, **_):
        job = self.job_service.update_job(job_id, job_data)
        return job

    @jobs_blp.response(204)
    def delete(self, job_id):
        self.job_service.delete_job(job_id)
        return "", 204
