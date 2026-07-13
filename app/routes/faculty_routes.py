from flask import Blueprint

from app.controllers.faculty_controller import FacultyController
from app.middleware.auth_required import user_required

faculty_bp = Blueprint("faculty", __name__)
controller = FacultyController()


@faculty_bp.route("/faculty")
@user_required
def dashboard():
    return controller.dashboard()
