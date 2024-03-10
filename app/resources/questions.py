from flask import Blueprint
from flask_restful import Api, Resource

questions_bp = Blueprint('questions', __name__)
api = Api(questions_bp)


class Question(Resource):

    def get(self, question_id=None):
        if question_id:
            return "<h1>Question for user with id {}</h1>".format(question_id)
        else:
            pass

    def post(self):
        # Implement POST method
        pass


api.add_resource(Question, '/questions', '/questions/<int:question_id>')
