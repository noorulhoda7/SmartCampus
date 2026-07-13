from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).resolve().parents[2]
    SECRET_KEY = "your_secret_key"

    ATTENDANCE_DIR = BASE_DIR / "Attendance"
    DATABASE_DIR = BASE_DIR / "Database"
    USERS_FILE = DATABASE_DIR / "users.txt"
    MODEL_DIR = BASE_DIR / "model"
    MODEL_PATH = MODEL_DIR / "cnn_face_model.h5"
    LABEL_PATH = MODEL_DIR / "labels.pkl"
    HAAR_CASCADE_PATH = BASE_DIR / "haarcascade_frontalface_default.xml"
    FACE_DATA_DIR = BASE_DIR / "app" / "static" / "faces"

    FACE_IMAGE_SIZE = 100
    FACE_CAPTURE_SAMPLES = 200
    RECOGNITION_TIMEOUT_SECONDS = 30
    MODEL_EPOCHS = 20
