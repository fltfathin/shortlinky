from sqlalchemy import Column, Integer, String
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///instance/shortlinky.sqlite3")

Base = declarative_base()

db = sessionmaker()
db.configure(bind=engine)
session = db()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    pass_hash = Column(String(100), nullable=False)

# TODO: handle hash


class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True)
    link = Column(String(200), nullable=False)
    shortlink = Column(String(100), nullable=False)


def create_db():
    Base.metadata.create_all(bind=engine)
