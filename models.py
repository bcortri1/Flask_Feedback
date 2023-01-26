from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Contains all user information related to a user"""

    def __repr__(self):
        return f"User: {self.username}"

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.Text(), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedbacks = db.relationship('Feedback')

    @classmethod
    def register(cls, username, pwd):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        currUser = User.query.filter_by(username=username).first()

        if currUser and bcrypt.check_password_hash(currUser.password, pwd):
            return currUser
        else:
            return False


class Feedback(db.Model):
    """Contains all user information related feedback"""

    def __repr__(self):
        return f"Feedback: {self.id} {self.title}"

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(50), nullable=False)

    username = db.Column(db.String(20), db.ForeignKey("users.username"))
