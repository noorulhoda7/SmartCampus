from app.extensions import db
from app.models.user import User


class UserRepository:
    def create(self, user_id, username, password, role):
        user = User(user_id=user_id, username=username, password=password, role=role)
        return self.add(user)

    def all(self):
        return User.query.order_by(User.id.asc()).all()

    def template_rows(self):
        return [user.to_template_row() for user in self.all()]

    def add(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def find_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def find_by_credentials(self, username, password):
        return User.query.filter_by(username=username, password=password).first()
