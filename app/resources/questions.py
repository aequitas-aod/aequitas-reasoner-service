import json
import os
from typing import List

from flask import Blueprint, request
from flask_restful import Api, Resource

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

questions_bp = Blueprint("questions", __name__)
api = Api(questions_bp)

if os.environ.get("TEST") == "true":
    questions: set = set()
else:
    questions: set = {
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
            filtered_questions: List[Question] = list(
                filter(lambda q: q.id.code == question_id, questions)
            )
            if len(filtered_questions) == 0:
                return "", 204
            else:
                return serialize_question(filtered_questions.pop()), 200
        else:
            all_questions: List[dict] = [
                json.loads(question.model_dump_json()) for question in questions
            ]
            return all_questions, 200

    def post(self):
        new_question: Question = deserialize_question(request.get_json())
        questions.add(new_question)
        return serialize_question(new_question), 201

    def delete(self):
        question_id: QuestionId = deserialize_question_id(request.get_json())
        questions.remove(list(filter(lambda q: q.id == question_id, questions)).pop())
        return "", 200


api.add_resource(QuestionResource, "/questions", "/questions/<string:question_id>")
