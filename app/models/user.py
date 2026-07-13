from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    user_id: str
    username: str
    password: str
    role: str

    @classmethod
    def from_csv_row(cls, row):
        if len(row) != 4:
            raise ValueError("User row must contain user_id, username, password and role.")
        return cls(user_id=row[0], username=row[1], password=row[2], role=row[3])

    def to_csv_row(self):
        return [self.user_id, self.username, self.password, self.role]
