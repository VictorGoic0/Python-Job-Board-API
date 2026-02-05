from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector

from app.extensions import db, ma, api
from config import config


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    CORS(app)

    _configure_injector(app)

    return app


def _configure_injector(app):
    def configure(binder):
        pass

    FlaskInjector(app=app, modules=[configure])
