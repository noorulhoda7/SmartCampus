from flask import Blueprint

from app.controllers.attendance_controller import AttendanceController
from app.middleware.auth_required import user_required

attendance_bp = Blueprint("attendance", __name__)
controller = AttendanceController()


@attendance_bp.route("/user_attendance")
@user_required
def user_history():
    return controller.user_history()


@attendance_bp.route("/view_attendance")
def today_report():
    return controller.today_report()
