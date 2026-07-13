import csv

from flask import current_app

from app.models.user import User


class UserRepository:
    def __init__(self, users_file=None):
        self.users_file = users_file

    @property
    def path(self):
        return self.users_file or current_app.config["USERS_FILE"]

    def all(self):
        users = []
        if not self.path.exists():
            return users

        with self.path.open(newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    users.append(User.from_csv_row(row))
                except ValueError:
                    continue
        return users

    def add(self, user):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(user.to_csv_row())

    def find_by_credentials(self, username, password):
        for user in self.all():
            if user.username == username and user.password == password:
                return user
        return None
