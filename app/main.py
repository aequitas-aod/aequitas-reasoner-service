from flask import Flask

from app.resources.projects import projects_bp
from app.resources.questionnaires import questionnaires_bp
from app.resources.questions import questions_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(questions_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(questionnaires_bp)
    return app
