from flask import Blueprint
from flask import render_template, make_response, redirect
from flask import url_for, request
from .decorators import login_required
from .db import Link, User, session
import re
from secrets import token_urlsafe

mod = Blueprint("simple_bp", __name__, template_folder="templates")

url_re = re.compile(
    r"(http[s]?://)?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)


@mod.route("/")
@login_required
def index():
    return render_template("index.html")


@mod.route("/logout/", methods=["GET", "POST"])
def logout():
    res = make_response(redirect(url_for("simple_bp.login")))
    res.set_cookie("user", "")
    return res


@mod.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "fathin" and password == "secret":
            res = make_response(
                redirect(request.args.get("next", url_for("simple_bp.index")))
            )
            res.set_cookie("user", username)
            return res
        else:
            return render_template("login.html", error="wrong username/password")
    return render_template("login.html")


@mod.route("/api/", methods=["GET", "POST"])
@login_required
def hello():
    if request.method == "POST":
        try:
            data = request.get_json()
            url = data.get("url")
            res = url_re.fullmatch(url)
            if res is not None:
                shortlink = data.get("shortlink")
                if shortlink == "" or shortlink is None:
                    shortlink = token_urlsafe(64)[0:8]
                new_link = Link(link=url, shortlink=shortlink)
                session.add(new_link)
                session.commit()
                return {"ok": True, "shortlink": f"/{shortlink}"}
            else:
                return {"ok": False, "error": "url invalid"}, 400
        except Exception as e:
            return {"ok": False, "error": str(e)}, 500
    return {"ok": "peko"}

# TODO: manage links


# a simple page that says hello
@mod.route("/<linkid>")
def redir(linkid):
    url = session.query(Link).filter_by(shortlink=linkid).first()
    if url is None:
        return render_template("404.html", error="link unavailable")
    return redirect(url.link)
