from flask import redirect, render_template, request, session

from app.services.auth_service import AuthService


class AuthController:
    def __init__(self, auth_service=None):
        self.auth_service = auth_service or AuthService()

    def show_login(self):
        return render_template("login.html")

    def login(self):
        result = self.auth_service.authenticate(
            request.form["username"],
            request.form["password"],
            request.form["role"],
        )

        if not result:
            return "Invalid credentials"

        if result["type"] == "admin":
            session["admin"] = result["username"]
            return redirect("/admin")

        session["user"] = result["username"]
        session["role"] = result["role"]
        if result["role"] == "Faculty":
            return redirect("/faculty")
        return redirect("/user")

    def logout(self):
        session.clear()
        return redirect("/")
