from typing import List, Optional

from flask import Blueprint, request
from flask_restful import Api, Resource

from domain.graph.core import Question, QuestionId
from presentation.presentation import serialize, deserialize
from ws.setup import question_service

questions_bp = Blueprint("questions", __name__)
api = Api(questions_bp)


class QuestionResource(Resource):

    def get(self, question_id=None):
        if question_id:
            question: Optional[Question] = question_service.get_question_by_id(
                QuestionId(code=question_id)
            )
            return (serialize(question), 200) if question else ("Question not found", 404)
        else:
            all_questions: List = question_service.get_all_questions()
            return [serialize(question) for question in all_questions], 200

    def post(self):
        new_question: Question = deserialize(request.get_json(), Question)
        try:
            question_service.add_question(new_question)
        except ValueError:
            return "Question already exists", 409
        return serialize(new_question.id), 201

    def delete(self, question_id=None):
        if question_id:
            try:
                question_service.delete_question(QuestionId(code=question_id))
                return "Question deleted successfully", 200
            except ValueError:
                return "Question not found", 404
        else:
            return "Missing question id", 400


class NewCandidateID(Resource):

    def get(self):
        return question_service.get_new_candidate_id()


api.add_resource(QuestionResource, "/questions", "/questions/<string:question_id>")
api.add_resource(NewCandidateID, "/questions/new-candidate-id")
