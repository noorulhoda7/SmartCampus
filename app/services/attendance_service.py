from collections import defaultdict

from app.repositories.attendance_repository import AttendanceRepository
from app.utils.date_utils import current_time, date_today


class AttendanceService:
    def __init__(self, attendance_repository=None):
        self.attendance_repository = attendance_repository or AttendanceRepository()

    def mark_attendance(self, username):
        date = date_today()
        self.attendance_repository.add(username, date, current_time())

    def history_for_user(self, username):
        return self.attendance_repository.records_for_user(username)

    def today_report(self):
        counts = defaultdict(int)
        records = self.attendance_repository.records_for_date(date_today())

        for row in records:
            if row:
                counts[row[0]] += 1

        return {
            "records": records,
            "labels": list(counts.keys()),
            "data": list(counts.values()),
        }
