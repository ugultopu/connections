from http import HTTPStatus

from flask import Flask, jsonify
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from connections.config import Config
from connections.extensions import cors, db, ma, migrate
from connections.views import blueprint


def create_app(config_object=Config):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blueprint)


def register_errorhandlers(app):
    """Register error handlers."""
    @app.errorhandler(403)
    def handle_forbidden(error):
        return jsonify({'description': error.description}), error.code

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({'description': error.description}), error.code

    @app.errorhandler(422)
    def handle_unprocessable_entity(error):
        response = {
            'description': 'Input failed validation.',
            'errors': error.exc.messages,
        }
        return jsonify(response), HTTPStatus.BAD_REQUEST

    # Catch webargs validation errors and return them in JSON format
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        response = {
            'description': 'Input failed validation.',
            'errors': error.messages,
        }
        return jsonify(response), HTTPStatus.BAD_REQUEST

    @app.errorhandler(IntegrityError)
    def handle_integrity_errors(error):
        return (jsonify({'description': f'Database integrity error: {error.orig.args[1]}'}),
                HTTPStatus.BAD_REQUEST)
