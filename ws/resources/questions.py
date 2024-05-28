from typing import List, Optional

from flask import Blueprint, request
from flask_restful import Api, Resource

from domain.graph.core import Question, QuestionId
from presentation.presentation import serialize, deserialize
from utils.errors import BadRequestError, ConflictError, NotFoundError
from utils.status_code import StatusCode
from ws.setup import question_service

questions_bp = Blueprint("questions", __name__)
api = Api(questions_bp)


class QuestionResource(Resource):

    def get(self, question_id=None):
        if question_id:
            question: Optional[Question] = question_service.get_question_by_id(
                QuestionId(code=question_id)
            )
            return (
                (serialize(question), StatusCode.OK)
                if question
                else ("Question not found", StatusCode.NOT_FOUND)
            )
        else:
            all_questions: List = question_service.get_all_questions()
            return [serialize(question) for question in all_questions], StatusCode.OK

    def post(self):
        new_question: Question = deserialize(request.get_json(), Question)
        try:
            question_service.add_question(new_question)
        except ConflictError as e:
            return e.message, e.status_code
        return serialize(new_question.id), StatusCode.CREATED

    def put(self, question_id=None):
        if question_id:
            updated_question: Question = deserialize(request.get_json(), Question)
            try:
                question_service.update_question(QuestionId(code=question_id), updated_question)
                return "Question updated successfully", StatusCode.OK
            except BadRequestError as e:
                return e.message, e.status_code
            except ConflictError as e:
                return e.message, e.status_code
        else:
            return "Missing question id", StatusCode.BAD_REQUEST

    def delete(self, question_id=None):
        if question_id:
            try:
                question_service.delete_question(QuestionId(code=question_id))
                return "Question deleted successfully", StatusCode.OK
            except NotFoundError as e:
                return e.message, e.status_code
        else:
            return "Missing question id", StatusCode.BAD_REQUEST


class NewCandidateID(Resource):

    def get(self):
        return question_service.get_new_candidate_id()


api.add_resource(QuestionResource, "/questions", "/questions/<string:question_id>")
api.add_resource(NewCandidateID, "/questions/new-candidate-id")
