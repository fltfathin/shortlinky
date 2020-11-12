from flask import request, redirect, url_for
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_fun(*args, **kwargs):
        if (user := request.cookies.get("user")) is None or user == "":
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)

    return decorated_fun
