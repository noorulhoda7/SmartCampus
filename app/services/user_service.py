from app.repositories.faculty_repository import FacultyRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository=None, student_repository=None, faculty_repository=None):
        self.user_repository = user_repository or UserRepository()
        self.student_repository = student_repository or StudentRepository()
        self.faculty_repository = faculty_repository or FacultyRepository()

    def register_user(self, user_id, username, password, role):
        user = self.user_repository.create(user_id, username, password, role)
        self._ensure_role_profile(user)
        return user

    def list_users_for_template(self):
        return self.user_repository.template_rows()

    def _ensure_role_profile(self, user):
        if user.role == "Student":
            self.student_repository.ensure_for_user(user)
        elif user.role == "Faculty":
            self.faculty_repository.ensure_for_user(user)
