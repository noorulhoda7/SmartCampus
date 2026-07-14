from app.extensions import db
from app.models.attendance import Attendance


class AttendanceRepository:
    def add(self, username, date, time):
        record = Attendance(username=username, date=date, time=time)
        db.session.add(record)
        db.session.commit()
        return record

    def records_for_user(self, username):
        records = (
            Attendance.query
            .filter_by(username=username)
            .order_by(Attendance.date.desc(), Attendance.time.desc(), Attendance.id.desc())
            .all()
        )
        return [record.to_template_row() for record in records]

    def records_for_date(self, date):
        records = (
            Attendance.query
            .filter_by(date=date)
            .order_by(Attendance.id.asc())
            .all()
        )
        return [record.to_template_row() for record in records]
