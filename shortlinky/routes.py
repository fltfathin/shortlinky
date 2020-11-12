from flask import Blueprint, 
from flask import render_template, make_response, redirect
from flask import url_for
from .decorators import login_required

mod = Blueprint("simple_bp", __name__, template_folder="templates")


@mod.route("/")
@login_required
def index():
    return render_template("index.html")


@mod.route("/logout/", methods=["GET", "POST"])
def logout():
    res = make_response(redirect(url_for("login")))
    res.set_cookie("user", "")
    return res
