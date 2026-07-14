import csv

from flask import current_app

from app.extensions import db
from app.models.faculty import Faculty
from app.models.student import Student
from app.models.user import User


class UserRepository:
    def __init__(self, users_file=None):
        self.users_file = users_file

    @property
    def path(self):
        return self.users_file or current_app.config["USERS_FILE"]

    def all(self):
        self.import_legacy_users_if_empty()
        return User.query.order_by(User.id.asc()).all()

    def add(self, user):
        db.session.add(user)
        db.session.flush()
        self._ensure_role_profile(user)
        db.session.commit()
        return user

    def find_by_credentials(self, username, password):
        self.import_legacy_users_if_empty()
        return User.query.filter_by(username=username, password=password).first()

    def import_legacy_users_if_empty(self):
        if User.query.first() is not None or not self.path.exists():
            return

        with self.path.open(newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    user = User.from_csv_row(row)
                except ValueError:
                    continue
                db.session.add(user)
                db.session.flush()
                self._ensure_role_profile(user)
        db.session.commit()

    def _ensure_role_profile(self, user):
        if user.role == "Student" and not user.student:
            db.session.add(Student(user=user))
        elif user.role == "Faculty" and not user.faculty:
            db.session.add(Faculty(user=user))
