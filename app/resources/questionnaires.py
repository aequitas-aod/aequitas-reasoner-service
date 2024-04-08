from flask import Blueprint
from flask_restful import Api, Resource

questionnaires_bp = Blueprint("questionnaires", __name__)
api = Api(questionnaires_bp)


class QuestionnaireResource(Resource):
    def get(self, project_id):
        # Replace this with business logic
        return '', 200

    def delete(self, project_id):
        # Assume you have logic to delete questions for the given project ID
        # Replace this with business logic
        return '', 204


api.add_resource(QuestionnaireResource, '/projects/<string:project_id>/questionnaire')
