from app.extensions import db
from app.utils.datetime_utils import utc_now


class Company(db.Model):
    __tablename__ = "company"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    website = db.Column(db.String(255))
    location = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
    version = db.Column(db.Integer, default=0, nullable=False)

    jobs = db.relationship(
        "Job",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    def __repr__(self):
        return f"<Company(id={self.id}, name={self.name!r})>"
