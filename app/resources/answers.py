from flask import Blueprint
from flask_restful import Api, Resource

from app.domain.factories.AnswerFactory import AnswerFactory

answers_bp = Blueprint("answers", __name__)
api = Api(answers_bp)

answer_factory = AnswerFactory()
answers = {
    answer_factory.create_answer("Always", "always"),
    answer_factory.create_answer("Usually", "usually"),
    answer_factory.create_answer("Sometimes", "sometimes"),
    answer_factory.create_answer("Never", "never"),
    answer_factory.create_boolean_answer(True),
    answer_factory.create_boolean_answer(False),
}


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
