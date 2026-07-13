from flask import render_template, session

from app.services.attendance_service import AttendanceService


class AttendanceController:
    def __init__(self, attendance_service=None):
        self.attendance_service = attendance_service or AttendanceService()

    def user_history(self):
        records = self.attendance_service.history_for_user(session["user"])
        return render_template("attendance_history.html", records=records)

    def today_report(self):
        report = self.attendance_service.today_report()
        return render_template(
            "attendance.html",
            records=report["records"],
            labels=report["labels"],
            data=report["data"],
        )
