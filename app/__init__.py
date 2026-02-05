from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import singleton

from app.extensions import db, ma, api
from config import config


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    if config_name == "development":
        app.config["DEBUG"] = True

    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    CORS(app)

    from app.routes.companies import companies_blp
    from app.routes.jobs import jobs_blp

    api.register_blueprint(jobs_blp)
    api.register_blueprint(companies_blp)

    from app.utils.error_handlers import register_error_handlers

    register_error_handlers(app)

    _configure_injector(app)

    return app


def _configure_injector(app):
    from app.repositories.company_repository import CompanyRepository
    from app.repositories.job_repository import JobRepository
    from app.services.company_service import CompanyService
    from app.services.job_service import JobService

    def configure(binder):
        binder.bind(CompanyRepository, to=CompanyRepository, scope=singleton)
        binder.bind(JobRepository, to=JobRepository, scope=singleton)
        binder.bind(CompanyService, to=CompanyService, scope=singleton)
        binder.bind(JobService, to=JobService, scope=singleton)

    FlaskInjector(app=app, modules=[configure])
