import csv

from flask import current_app


class AttendanceRepository:
    def __init__(self, attendance_dir=None):
        self.attendance_dir = attendance_dir

    @property
    def directory(self):
        return self.attendance_dir or current_app.config["ATTENDANCE_DIR"]

    def file_for_date(self, date):
        return self.directory / f"Attendance-{date}.csv"

    def add(self, username, date, time):
        self.directory.mkdir(parents=True, exist_ok=True)
        file_path = self.file_for_date(date)
        is_new = not file_path.exists()

        with file_path.open("a", newline="") as file:
            writer = csv.writer(file)
            if is_new:
                writer.writerow(["Username", "Date", "Time"])
            writer.writerow([username, date, time])

    def records_for_user(self, username):
        if not self.directory.exists():
            return []

        records = []
        for file_path in self.directory.glob("*.csv"):
            records.extend(row for row in self._read_records(file_path) if row and row[0] == username)
        return sorted(records, key=lambda row: row[1], reverse=True)

    def records_for_date(self, date):
        file_path = self.file_for_date(date)
        if not file_path.exists():
            return []
        return self._read_records(file_path)

    def _read_records(self, file_path):
        with file_path.open(newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            return [row for row in reader]
