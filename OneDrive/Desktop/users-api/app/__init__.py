from flask import Flask, jsonify

from app.config import Config
from app.errors import ConflictError, NotFoundError, ValidationError
from app.extensions import db, migrate


def create_app(config_object: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.controllers.user_controller import users_bp

    app.register_blueprint(users_bp)

    @app.errorhandler(ValidationError)
    def handle_validation(exc):
        return jsonify({"error": str(exc)}), 400

    @app.errorhandler(NotFoundError)
    def handle_not_found(exc):
        return jsonify({"error": str(exc)}), 404

    @app.errorhandler(ConflictError)
    def handle_conflict(exc):
        return jsonify({"error": str(exc)}), 409

    @app.errorhandler(Exception)
    def handle_unexpected(exc):
        app.logger.exception("Error inesperado")
        return jsonify({"error": "error interno del servidor"}), 500

    return app
