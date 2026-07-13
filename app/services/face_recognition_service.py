import datetime

import cv2
import joblib
import numpy as np
from flask import current_app

from app.services.attendance_service import AttendanceService


class FaceRecognitionService:
    def __init__(self, attendance_service=None):
        self.attendance_service = attendance_service or AttendanceService()

    def capture_faces(self, user):
        folder = current_app.config["FACE_DATA_DIR"] / f"{user.user_id}_{user.username}_{user.role}"
        folder.mkdir(parents=True, exist_ok=True)

        face_cascade = self._face_cascade()
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Camera could not be opened. Please check webcam permissions and connection.")

        count = 0
        samples = current_app.config["FACE_CAPTURE_SAMPLES"]
        image_size = current_app.config["FACE_IMAGE_SIZE"]

        while count < samples:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                face = gray[y:y + h, x:x + w]
                face = cv2.resize(face, (image_size, image_size))
                cv2.imwrite(str(folder / f"{count}.jpg"), face)
                count += 1
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"Captured: {count}/{samples}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            cv2.imshow("Capturing", frame)
            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def recognize_and_mark(self, username):
        model, labels = self._load_model()
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return False, None

        face_cascade = self._face_cascade()
        image_size = current_app.config["FACE_IMAGE_SIZE"]
        timeout = current_app.config["RECOGNITION_TIMEOUT_SECONDS"]
        start_time = datetime.datetime.now()
        detected_user = None

        while (datetime.datetime.now() - start_time).seconds < timeout:
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                face = gray[y:y + h, x:x + w]
                face = cv2.resize(face, (image_size, image_size))
                face = face.reshape(1, image_size, image_size, 1) / 255.0
                pred = model.predict(face)
                pred_class = np.argmax(pred)

                for user_key, label in labels.items():
                    if label == pred_class and username in user_key:
                        self.attendance_service.mark_attendance(username)
                        detected_user = user_key
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame, user_key, (x, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                        break

                if detected_user:
                    break

            cv2.imshow("Face Recognition - User", frame)
            if cv2.waitKey(1) == 27 or detected_user:
                break

        cap.release()
        cv2.destroyAllWindows()
        return bool(detected_user), detected_user

    def _face_cascade(self):
        cascade = cv2.CascadeClassifier(str(current_app.config["HAAR_CASCADE_PATH"]))
        if cascade.empty():
            raise RuntimeError("Face detection model could not be loaded.")
        return cascade

    def _load_model(self):
        model_path = current_app.config["MODEL_PATH"]
        label_path = current_app.config["LABEL_PATH"]
        if not model_path.exists() or not label_path.exists():
            raise FileNotFoundError("Face model is not trained yet. Please train the model from the admin dashboard.")

        from tensorflow.keras.models import load_model

        return load_model(str(model_path)), joblib.load(label_path)
