import logging
from logging.handlers import RotatingFileHandler


def configure_logging(flask_app):
    log_dir = flask_app.config["LOG_DIR"]
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = flask_app.config["LOG_FILE"]
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=flask_app.config["LOG_MAX_BYTES"],
        backupCount=flask_app.config["LOG_BACKUP_COUNT"],
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(flask_app.config["LOG_LEVEL"])
    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    flask_app.logger.handlers.clear()
    flask_app.logger.propagate = True
    flask_app.logger.setLevel(flask_app.config["LOG_LEVEL"])


def get_logger(name):
    return logging.getLogger(name)
