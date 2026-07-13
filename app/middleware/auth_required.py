from functools import wraps

from flask import redirect, session


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "admin" not in session:
            return redirect("/")
        return view(*args, **kwargs)

    return wrapped


def user_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user" not in session:
            return redirect("/")
        return view(*args, **kwargs)

    return wrapped
