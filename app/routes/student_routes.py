from flask import Blueprint

from app.controllers.student_controller import StudentController
from app.middleware.auth_required import user_required

student_bp = Blueprint("student", __name__)
controller = StudentController()


@student_bp.route("/user")
@user_required
def dashboard():
    return controller.dashboard()
