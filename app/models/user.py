from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(120), nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, index=True)

    student = db.relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    faculty = db.relationship("Faculty", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def to_template_row(self):
        return [self.user_id, self.username, self.password, self.role]
