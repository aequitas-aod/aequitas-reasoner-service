from flask import Blueprint
from flask_restful import Api, Resource

answers_bp = Blueprint("answers", __name__)
api = Api(answers_bp)


class AnswerResource(Resource):

    def get(self, answer_id=None):
        if answer_id:
            return "<h1>Answer for user with id {}</h1>".format(answer_id)
        else:
            pass

    def post(self):
        # Implement POST method
        pass


api.add_resource(AnswerResource, "/answers", "/answers/<int:answer_id>")
