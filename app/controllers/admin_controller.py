from flask import redirect, render_template, url_for

from app.services.face_recognition_service import FaceRecognitionService
from app.services.training_service import TrainingService
from app.services.user_service import UserService


class AdminController:
    def __init__(self, user_service=None, face_service=None, training_service=None):
        self.user_service = user_service or UserService()
        self.face_service = face_service or FaceRecognitionService()
        self.training_service = training_service or TrainingService()

    def dashboard(self):
        users = self.user_service.list_users_for_template()
        return render_template("admin_dashboard.html", users=users)

    def show_register(self):
        return render_template("register.html")

    def register_user(self, form):
        user = self.user_service.register_user(
            form["userid"],
            form["username"],
            form["password"],
            form["role"],
        )
        self.face_service.capture_faces(user)
        return redirect("/admin")

    def train_model(self):
        self.training_service.train_model()
        return redirect(url_for("admin.dashboard", trained="yes"))
