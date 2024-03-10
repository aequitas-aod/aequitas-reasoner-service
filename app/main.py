from flask import Flask

from app.resources.answers import answers_bp
from app.resources.questions import questions_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(answers_bp)
    app.register_blueprint(questions_bp)
    return app
