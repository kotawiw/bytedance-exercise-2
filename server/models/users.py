from . import db

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from email.utils import parseaddr

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password_hashed = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.email

    @staticmethod
    def try_register(email, password):

        email = _check_email(email)
        if not email:
            return None

        current_user = User.query.filter_by(email=email).first()
        if current_user:
            print(current_user)
            return None

        password_hashed = _check_and_hash_password(password)
        if not password_hashed:
            print(password)
            return None

        user = User(email=email, password_hashed=password_hashed)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def by_email_password(email, password=None):
        user = User.query.filter_by(email=email).first()

        if user and password:
            if not check_password_hash(user.password_hashed, password):
                return None

        return user


def _check_and_hash_password(password):
    return generate_password_hash(password)


def _check_email(email):
    if not email:
        raise ValueError("Invalid email")

    _, parsed_email = parseaddr(email)
    if parsed_email != email:
        raise ValueError("Invalid email")

    return email