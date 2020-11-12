import os

from flask import Flask, request, render_template, redirect
import re
from flask_sqlalchemy import SQLAlchemy
from secrets import token_urlsafe

url_re = re.compile(
    r"(http[s]?://)?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        # SQLALCHEMY_DATABASE_URI='postgresql://john:doe@localhost:5432/shortlinky',
        SQLALCHEMY_DATABASE_URI="sqlite:///../instance/shortlinky.sqlite3",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .db import make_db

    db, User, Link = make_db(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/", methods=["GET", "POST"])
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
                    thing = Link(link=url, shortlink=shortlink)
                    db.session.add(thing)
                    db.session.commit()
                    return {"ok": True, "shortlink": f"/{shortlink}"}
                else:
                    return {"ok": False, "error": "url invalid"}, 400
            except Exception as e:
                return {"ok": False, "error": str(e)}, 500
        return {"ok": "peko"}

    # a simple page that says hello
    @app.route("/<linkid>")
    def redir(linkid):
        url = Link.query.filter_by(shortlink=linkid).first()
        print(url)
        if url is None:
            return render_template("404.html", error="link unavailable")
        return redirect(url.link)

    return app
