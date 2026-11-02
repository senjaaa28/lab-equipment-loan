import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from .validators import NotFoundError, ValidationError


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "lab_equipment.db"),
    )
    app.json.sort_keys = False

    if test_config is not None:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    from . import database
    from .routes import item_routes, loan_routes

    database.init_app(app)
    app.register_blueprint(item_routes.bp)
    app.register_blueprint(loan_routes.bp)

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        return jsonify({"error": str(error)}), 404

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({"error": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception(error)
        return jsonify({"error": "Terjadi kesalahan pada server."}), 500

    return app
