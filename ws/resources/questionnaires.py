from flask import Blueprint
from flask_restful import Api, Resource

from utils.status_code import StatusCode

questionnaires_bp = Blueprint("questionnaires", __name__)
api = Api(questionnaires_bp)


class QuestionnaireResource(Resource):
    def get(self, project_id):
        # Replace this with business logic
        return "", StatusCode.OK

    def delete(self, project_id):
        # Replace this with business logic
        return "", 404


api.add_resource(QuestionnaireResource, "/projects/<string:project_id>/questionnaire")
