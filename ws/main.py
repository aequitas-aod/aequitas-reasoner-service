from flask import Flask

from ws.resources.projects import projects_bp
from ws.resources.questionnaires import questionnaires_bp
from ws.resources.questions import questions_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(questions_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(questionnaires_bp)
    return app
