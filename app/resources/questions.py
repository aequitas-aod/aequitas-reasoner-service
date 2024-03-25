import json

from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse

from app.domain.core.Question import Question
from app.domain.core.QuestionId import QuestionId
from app.domain.core.enum.Action import Action
from app.domain.core.enum.QuestionType import QuestionType
from app.domain.factories.AnswerFactory import AnswerFactory
from app.domain.factories.QuestionFactory import QuestionFactory
from app.presentation.presentation import (
    serialize_question,
    deserialize_question,
    deserialize_question_id,
)
from app.utils.logger import logger

questions_bp = Blueprint("questions", __name__)
api = Api(questions_bp)

questions = {
    QuestionFactory().create_boolean_question(
        QuestionId(code="tdd-question"), "Do you practice TDD?"
    ),
    QuestionFactory().create_question(
        QuestionId(code="ci-question"),
        "Do you use CI?",
        QuestionType.SINGLE_CHOICE,
        frozenset(
            {
                AnswerFactory().create_answer("Yes", "yes"),
                AnswerFactory().create_answer("A little bit", "little-bit"),
                AnswerFactory().create_answer("No", "no"),
            }
        ),
        action_needed=Action.METRICS_CHECK,
    ),
}


class QuestionResource(Resource):

    def get(self, question_id=None):
        if question_id:
            question: Question = list(
                filter(lambda q: q.id.code == question_id, questions)
            ).pop()
            return serialize_question(question), 200
        else:
            return json.loads(json.dumps([q.model_dump_json() for q in questions])), 200

    def post(self):
        new_question: Question = deserialize_question(request.get_json())
        questions.add(new_question)
        return serialize_question(new_question), 201

    def delete(self):
        question_id: QuestionId = deserialize_question_id(request.get_json())
        questions.remove(list(filter(lambda q: q.id == question_id, questions)).pop())
        return "", 200


api.add_resource(QuestionResource, "/questions", "/questions/<string:question_id>")
