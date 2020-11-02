from flask_sqlalchemy import SQLAlchemy


def make_db(app):
    db: SQLAlchemy = SQLAlchemy(app=app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        pass_hash = db.Column(db.String(100), nullable=False)

    class Link(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        link = db.Column(db.String(200), nullable=False)
        shortlink = db.Column(db.String(100), nullable=False)

    db.create_all()
    return db, User, Link
