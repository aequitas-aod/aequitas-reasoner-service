import json

from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse

from app.domain.core.Question import Question
from app.domain.core.QuestionId import QuestionId
from app.domain.core.enum.Action import Action
from app.domain.core.enum.QuestionType import QuestionType
from app.domain.factories.AnswerFactory import AnswerFactory
from app.domain.factories.QuestionFactory import QuestionFactory

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
            question: Question = list(filter(lambda q: q.id.code == question_id, questions)).pop()
            return json.loads(question.model_dump_json()), 200
        else:
            return json.loads(json.dumps([q.model_dump_json() for q in questions])), 200

    def post(self):
        new_question: Question = Question(**request.get_json())
        questions.add(new_question)
        return json.loads(new_question.model_dump_json()), 201


api.add_resource(QuestionResource, "/questions", "/questions/<string:question_id>")
