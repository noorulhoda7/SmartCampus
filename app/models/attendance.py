from app.extensions import db


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, index=True)
    date = db.Column(db.String(20), nullable=False, index=True)
    time = db.Column(db.String(20), nullable=False)

    def to_template_row(self):
        return [self.username, self.date, self.time]
