from app.repositories.user_repository import UserRepository


class AuthService:
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin"
    ADMIN_ROLE = "admin"

    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def authenticate(self, username, password, role):
        if role == self.ADMIN_ROLE and username == self.ADMIN_USERNAME and password == self.ADMIN_PASSWORD:
            return {"type": "admin", "username": username, "role": role}

        user = self.user_repository.find_by_credentials(username, password)
        if user and user.role == role:
            return {"type": "user", "username": user.username, "role": user.role}

        return None
