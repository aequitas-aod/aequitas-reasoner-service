from flask import Blueprint
from flask_restful import Api, Resource

from application.project import questionnaire_service
from utils.status_code import StatusCode

questionnaires_bp = Blueprint("questionnaires", __name__)
api = Api(questionnaires_bp)


class QuestionnaireResource(Resource):
    def get(self, project_id=None, index=None):
        if project_id and index:
            questionnaire_service
            # Replace this with business logic
            return "", StatusCode.OK
        else:
            return "Missing project id or question index", StatusCode.BAD_REQUEST

    def delete(self, project_id=None, index=None):
        # Replace this with business logic
        return "", 404


"/projects/{self.project_id.code}/questionnaire/1"
api.add_resource(
    QuestionnaireResource, "/projects/<string:project_id>/questionnaire/<int:index>"
)
