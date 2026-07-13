from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def register_user(self, user_id, username, password, role):
        user = User(user_id=user_id, username=username, password=password, role=role)
        self.user_repository.add(user)
        return user

    def list_users_for_template(self):
        return [user.to_csv_row() for user in self.user_repository.all()]
