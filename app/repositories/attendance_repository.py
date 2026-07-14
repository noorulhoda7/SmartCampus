import csv

from flask import current_app

from app.extensions import db
from app.models.attendance import Attendance


class AttendanceRepository:
    def __init__(self, attendance_dir=None):
        self.attendance_dir = attendance_dir

    @property
    def directory(self):
        return self.attendance_dir or current_app.config["ATTENDANCE_DIR"]

    def file_for_date(self, date):
        return self.directory / f"Attendance-{date}.csv"

    def add(self, username, date, time):
        self.import_legacy_attendance_if_empty()
        record = Attendance(username=username, date=date, time=time)
        db.session.add(record)
        db.session.commit()
        return record

    def records_for_user(self, username):
        self.import_legacy_attendance_if_empty()
        records = (
            Attendance.query
            .filter_by(username=username)
            .order_by(Attendance.date.desc(), Attendance.time.desc(), Attendance.id.desc())
            .all()
        )
        return [record.to_csv_row() for record in records]

    def records_for_date(self, date):
        self.import_legacy_attendance_if_empty()
        records = (
            Attendance.query
            .filter_by(date=date)
            .order_by(Attendance.id.asc())
            .all()
        )
        return [record.to_csv_row() for record in records]

    def import_legacy_attendance_if_empty(self):
        if Attendance.query.first() is not None or not self.directory.exists():
            return

        for file_path in self.directory.glob("*.csv"):
            for row in self._read_records(file_path):
                if len(row) < 3:
                    continue
                db.session.add(Attendance(username=row[0], date=row[1], time=row[2]))
        db.session.commit()

    def _read_records(self, file_path):
        with file_path.open(newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            return [row for row in reader]
