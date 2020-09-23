import functools

from flask import Blueprint
from flask import g
from flask import request
from flask import session
from flask import abort
from flask import jsonify
from server.models.users import User

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user' not in g:
            return abort(401, "Login required")

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id:
        g.user = User.query.get(user_id)


@bp.route("/status")
def get_status():
    if 'user' not in g:
        return jsonify({"loggedIn": False})

    return jsonify({
        "loggedIn": True,
        "email": g.user.email
    })


@bp.route("/register", methods=("POST",))
def register():
    autologin = request.args.get("autologin", default="True").lower() == "true"

    email = request.json.get('email')
    password = request.json.get('password')

    user = User.try_register(email, password)
    if not user:
        print(email, password)
        return abort(400, "Invalid email or password")

    if autologin:
        session["user_id"] = user.id

    return jsonify({'email': user.email, 'loggedIn': autologin})


@bp.route("/login", methods=("POST",))
def login():
    email = request.json['email']
    password = request.json['password']

    user = User.by_email_password(email, password)
    if not user:
        return abort(401, "Incorrect email or password")

    session["user_id"] = user.id
    return jsonify({'email': user.email, 'loggedIn': True})


@bp.route("/logout")
def logout():
    user = None
    if 'user' in g:
        user = g.user

    session.clear()
    if not user:
        return jsonify({"loggedIn": False})

    return jsonify({
        "loggedIn": True,
        "email": user.email
    })
