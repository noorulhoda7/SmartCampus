from app.extensions import db
from app.models.faculty import Faculty
from app.models.role import Role
from app.models.student import Student
from app.models.user import User


DEFAULT_ROLES = ("admin", "Student", "Faculty")


def seed_database():
    for role_name in DEFAULT_ROLES:
        if Role.query.filter_by(name=role_name).first() is None:
            db.session.add(Role(name=role_name))

    admin = _get_or_create_user("admin", "admin", "admin", "admin")
    sample_student = _get_or_create_user("sample-student", "sample_student", "student123", "Student")
    sample_faculty = _get_or_create_user("sample-faculty", "sample_faculty", "faculty123", "Faculty")

    _ensure_student(sample_student)
    _ensure_faculty(sample_faculty)

    db.session.commit()
    return {
        "roles": len(DEFAULT_ROLES),
        "admin": admin.username,
        "student": sample_student.username,
        "faculty": sample_faculty.username,
    }


def _get_or_create_user(user_id, username, password, role):
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(user_id=user_id, username=username, password=password, role=role)
        db.session.add(user)
        db.session.flush()
    return user


def _ensure_student(user):
    if user.student is None:
        db.session.add(Student(user=user))


def _ensure_faculty(user):
    if user.faculty is None:
        db.session.add(Faculty(user=user))
