from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


def init_extensions(flask_app):
    """Initialize Flask extensions for the application."""
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    return flask_app
