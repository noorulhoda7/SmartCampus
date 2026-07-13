from flask import Blueprint

from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)
controller = AuthController()


@auth_bp.route("/")
def home():
    return controller.show_login()


@auth_bp.route("/login", methods=["POST"])
def login():
    return controller.login()


@auth_bp.route("/logout")
def logout():
    return controller.logout()
