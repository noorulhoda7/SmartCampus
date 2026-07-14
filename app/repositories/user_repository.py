from app.extensions import db
from app.models.faculty import Faculty
from app.models.student import Student
from app.models.user import User


class UserRepository:
    def all(self):
        return User.query.order_by(User.id.asc()).all()

    def add(self, user):
        db.session.add(user)
        db.session.flush()
        self._ensure_role_profile(user)
        db.session.commit()
        return user

    def find_by_credentials(self, username, password):
        return User.query.filter_by(username=username, password=password).first()

    def _ensure_role_profile(self, user):
        if user.role == "Student" and not user.student:
            db.session.add(Student(user=user))
        elif user.role == "Faculty" and not user.faculty:
            db.session.add(Faculty(user=user))
