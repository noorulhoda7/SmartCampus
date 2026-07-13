from flask import Flask

from app.config.settings import Config
from app.extensions import init_extensions
from app.routes.admin_routes import admin_bp
from app.routes.attendance_routes import attendance_bp
from app.routes.auth_routes import auth_bp
from app.routes.faculty_routes import faculty_bp
from app.routes.student_routes import student_bp


def create_app(config_class=Config):
    flask_app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    flask_app.config.from_object(config_class)

    init_extensions(flask_app)

    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(admin_bp)
    flask_app.register_blueprint(student_bp)
    flask_app.register_blueprint(faculty_bp)
    flask_app.register_blueprint(attendance_bp)

    return flask_app
