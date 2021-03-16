"""Models for notes app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User Model"""
    __tablename__ = "users"

    username = db.Column(db.String(20), 
                         primary_key=True)
    password = db.Column(db.Text,
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)

    notes = db.relationship("Note")

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """ Register user w/hashed pw and return user """

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')

        return cls(username=username, password=hashed, email=email, 
                   first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False

class Note(db.Model):
    """ Model for a Note class """
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    title = db.Column(
        db.String(100),
        nullable=False,
    )
    content = db.Column(
        db.Text,
        nullable=False
    )
    owner = db.Column(
        db.String(20),
        db.ForeignKey("users.username")  
    )

    user_name = db.relationship("User")