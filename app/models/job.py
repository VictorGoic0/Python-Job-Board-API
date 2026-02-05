from app.extensions import db
from app.models.enums import ExperienceLevel, JobType, RemoteOption
from app.utils.datetime_utils import utc_now


class Job(db.Model):
    __tablename__ = "job"

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company_id = db.Column(
        db.BigInteger,
        db.ForeignKey("company.id", ondelete="CASCADE"),
        nullable=False,
    )
    location = db.Column(db.String(255), nullable=False)
    salary_min = db.Column(db.Numeric(10, 2))
    salary_max = db.Column(db.Numeric(10, 2))
    job_type = db.Column(db.Enum(JobType), nullable=False)
    experience_level = db.Column(db.Enum(ExperienceLevel), nullable=False)
    remote_option = db.Column(db.Enum(RemoteOption), nullable=False)
    posted_date = db.Column(db.DateTime, default=utc_now, nullable=False)
    expiry_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    application_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
    version = db.Column(db.Integer, default=0, nullable=False)

    company = db.relationship("Company", back_populates="jobs")

    def __repr__(self):
        return f"<Job(id={self.id}, title={self.title!r})>"
