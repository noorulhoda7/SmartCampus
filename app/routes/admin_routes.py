from flask import Blueprint, request

from app.controllers.admin_controller import AdminController
from app.middleware.auth_required import admin_required

admin_bp = Blueprint("admin", __name__)
controller = AdminController()


@admin_bp.route("/admin")
@admin_required
def dashboard():
    return controller.dashboard()


@admin_bp.route("/register", methods=["GET", "POST"])
@admin_required
def register():
    if request.method == "POST":
        return controller.register_user(request.form)
    return controller.show_register()


@admin_bp.route("/train_model")
@admin_required
def train_model():
    return controller.train_model()
