from flask import Flask, Blueprint
from flask_restx import Api


def create_app():
    app = Flask(__name__)
    # mount our api application under a url-prefix /api/
    api_bp = Blueprint("api", __name__, url_prefix="/api")
    api = Api(
        api_bp,
        title="Todo's Application",
        description="An example api application using flask-restx",
        version="1.0",
        doc="/swagger/",
        validate=True,
    )
    app.register_blueprint(api_bp)
    return app, api


app, api = create_app()
