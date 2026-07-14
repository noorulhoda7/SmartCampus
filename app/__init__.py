from flask import Flask

from app.cli import register_cli_commands
from app.config.settings import Config
from app.errors import register_error_handlers
from app.extensions import init_extensions
from app.routes.admin_routes import admin_bp
from app.routes.attendance_routes import attendance_bp
from app.routes.auth_routes import auth_bp
from app.routes.faculty_routes import faculty_bp
from app.routes.student_routes import student_bp
from app.utils.logger import configure_logging


def create_app(config_class=Config):
    flask_app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    flask_app.config.from_object(config_class)

    configure_logging(flask_app)
    init_extensions(flask_app)

    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(admin_bp)
    flask_app.register_blueprint(student_bp)
    flask_app.register_blueprint(faculty_bp)
    flask_app.register_blueprint(attendance_bp)
    register_error_handlers(flask_app)
    register_cli_commands(flask_app)

    # Database schema is managed exclusively by Alembic migrations.
    from app import models

    return flask_app
