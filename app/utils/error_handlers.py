import traceback

from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.orm.exc import StaleDataError

from app.exceptions.custom_exceptions import (
    CompanyNotFoundException,
    JobNotFoundException,
    OptimisticLockException,
)


def register_error_handlers(app):
    @app.errorhandler(JobNotFoundException)
    def handle_job_not_found(error):
        return jsonify({"message": str(error), "status": 404}), 404

    @app.errorhandler(CompanyNotFoundException)
    def handle_company_not_found(error):
        return jsonify({"message": str(error), "status": 404}), 404

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return (
            jsonify(
                {
                    "message": "Validation failed",
                    "status": 400,
                    "errors": error.messages,
                }
            ),
            400,
        )

    @app.errorhandler(OptimisticLockException)
    @app.errorhandler(StaleDataError)
    def handle_optimistic_lock(error):
        return (
            jsonify({"message": "Resource modified by another user", "status": 409}),
            409,
        )

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        # Always log full traceback to console so we can see the real error
        app.logger.exception("Unhandled exception: %s", error)

        payload = {"message": "An unexpected error occurred", "status": 500}
        if app.debug:
            payload["error"] = str(error)
            payload["traceback"] = traceback.format_exc().splitlines()
        return jsonify(payload), 500
