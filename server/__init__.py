import os

from flask import Flask, jsonify, redirect
from werkzeug.exceptions import HTTPException

from server.models.events import Event
from server.models.users import User
from server.models import db


def create_app(
        instance_path=None,
        static_folder='../frontend/build'
):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__,
                instance_path=instance_path,
                static_url_path='/',
                static_folder=static_folder,
                instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db_path = os.path.join(app.instance_path, "server.sqlite")
    app.config.from_mapping(

        SECRET_KEY='SECRET_KEY',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + db_path,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)
    # apply the blueprints to the app
    from server import auth, api
    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)

    @app.errorhandler(ValueError)
    def http_error_handler(error):
        return jsonify(code=400, message=str(error)), 400

    @app.errorhandler(HTTPException)
    def http_error_handler(error):
        return jsonify(code=error.code, message=error.description), error.code

    @app.route('/')
    def home():
        return redirect('/index.html', code=302)

    with app.app_context():
        db.create_all()

    return app
