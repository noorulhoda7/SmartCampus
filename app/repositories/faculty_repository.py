from app.extensions import db
from app.models.faculty import Faculty


class FacultyRepository:
    def find_by_user(self, user):
        return Faculty.query.filter_by(user=user).first()

    def ensure_for_user(self, user, commit=True):
        faculty = self.find_by_user(user)
        if faculty is None:
            faculty = Faculty(user=user)
            db.session.add(faculty)
            if commit:
                db.session.commit()
        return faculty
