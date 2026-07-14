from app.extensions import db
from app.models.student import Student


class StudentRepository:
    def find_by_user(self, user):
        return Student.query.filter_by(user=user).first()

    def ensure_for_user(self, user, commit=True):
        student = self.find_by_user(user)
        if student is None:
            student = Student(user=user)
            db.session.add(student)
            if commit:
                db.session.commit()
        return student
