from app.extensions import db
from app.models.role import Role
from app.repositories.faculty_repository import FacultyRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.user_repository import UserRepository


DEFAULT_ROLES = ("admin", "Student", "Faculty")


def seed_database():
    user_repository = UserRepository()
    student_repository = StudentRepository()
    faculty_repository = FacultyRepository()

    for role_name in DEFAULT_ROLES:
        if Role.query.filter_by(name=role_name).first() is None:
            db.session.add(Role(name=role_name))
    db.session.commit()

    admin = _get_or_create_user(user_repository, "admin", "admin", "admin", "admin")
    sample_student = _get_or_create_user(user_repository, "sample-student", "sample_student", "student123", "Student")
    sample_faculty = _get_or_create_user(user_repository, "sample-faculty", "sample_faculty", "faculty123", "Faculty")

    student_repository.ensure_for_user(sample_student)
    faculty_repository.ensure_for_user(sample_faculty)

    return {
        "roles": len(DEFAULT_ROLES),
        "admin": admin.username,
        "student": sample_student.username,
        "faculty": sample_faculty.username,
    }


def _get_or_create_user(user_repository, user_id, username, password, role):
    user = user_repository.find_by_username(username)
    if user is None:
        user = user_repository.create(user_id, username, password, role)
    return user
