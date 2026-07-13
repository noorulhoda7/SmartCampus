import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_int(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def env_path(name, default):
    value = os.getenv(name)
    if not value:
        return default
    path = Path(value)
    if path.is_absolute():
        return path
    return BASE_DIR / path


class Config:
    BASE_DIR = BASE_DIR
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    DEBUG = env_bool("FLASK_DEBUG", False)
    HOST = os.getenv("FLASK_HOST", "127.0.0.1")
    PORT = env_int("FLASK_PORT", 5000)

    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'app.db'}")
    ATTENDANCE_DIR = env_path("ATTENDANCE_DIR", BASE_DIR / "Attendance")
    DATABASE_DIR = env_path("DATABASE_DIR", BASE_DIR / "Database")
    USERS_FILE = env_path("USERS_FILE", DATABASE_DIR / "users.txt")
    MODEL_DIR = env_path("MODEL_DIR", BASE_DIR / "model")
    MODEL_PATH = env_path("MODEL_PATH", MODEL_DIR / "cnn_face_model.h5")
    LABEL_PATH = env_path("LABEL_PATH", MODEL_DIR / "labels.pkl")
    HAAR_CASCADE_PATH = env_path("HAAR_CASCADE_PATH", BASE_DIR / "haarcascade_frontalface_default.xml")
    FACE_DATA_DIR = env_path("FACE_DATA_DIR", BASE_DIR / "app" / "static" / "faces")

    FACE_IMAGE_SIZE = env_int("FACE_IMAGE_SIZE", 100)
    FACE_CAPTURE_SAMPLES = env_int("FACE_CAPTURE_SAMPLES", 200)
    RECOGNITION_TIMEOUT_SECONDS = env_int("RECOGNITION_TIMEOUT_SECONDS", 30)
    MODEL_EPOCHS = env_int("MODEL_EPOCHS", 20)

    LOG_DIR = env_path("LOG_DIR", BASE_DIR / "logs")
    LOG_FILE = env_path("LOG_FILE", LOG_DIR / "app.log")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_MAX_BYTES = env_int("LOG_MAX_BYTES", 1048576)
    LOG_BACKUP_COUNT = env_int("LOG_BACKUP_COUNT", 5)
