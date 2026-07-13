from flask import render_template, session

from app.services.face_recognition_service import FaceRecognitionService


class StudentController:
    def __init__(self, face_service=None):
        self.face_service = face_service or FaceRecognitionService()

    def dashboard(self):
        result, detected_name = self.face_service.recognize_and_mark(session["user"])
        if result:
            return render_template("user_dashboard.html", name=detected_name)
        return "Face not recognized."
