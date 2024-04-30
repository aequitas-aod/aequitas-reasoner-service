import os
from typing import List, Optional

from flask import Blueprint, request
from flask_restful import Api, Resource

from domain.graph.core import Question, QuestionId, AnswerId
from domain.graph.core.enum import Action, QuestionType
from domain.graph.factories import AnswerFactory, QuestionFactory
from presentation.presentation import serialize, deserialize
from ws.setup import question_service
from ws.utils.logger import logger

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
                    AnswerFactory().create_answer(
                        AnswerId(code="answer-yes"), "Yes", "yes"
                    ),
                    AnswerFactory().create_answer(
                        AnswerId(code="answer-little-bit"), "A little bit", "little-bit"
                    ),
                    AnswerFactory().create_answer(
                        AnswerId(code="answer-no"), "No", "no"
                    ),
                }
            ),
            action_needed=Action.METRICS_CHECK,
        ),
    }


class QuestionResource(Resource):

    def get(self, question_id=None):
        if question_id:
            question: Optional[Question] = question_service.get_question_by_id(
                QuestionId(code=question_id)
            )
            logger.info(f"Question: {question}")
            if question is None:
                logger.info(f"E QUINDI")
                return "", 204
            else:
                return serialize(question), 200
            # filtered_questions: List[Question] = list(
            #     filter(lambda q: q.id.code == question_id, questions)
            # )
            # if len(filtered_questions) == 0:
            #     return "", 204
            # else:
            #     return serialize(filtered_questions.pop()), 200
        else:
            logger.info(f"NON QUI")
            all_questions: List = question_service.get_all_questions()
            return [serialize(question) for question in all_questions], 200
            # all_questions: List[dict] = [
            #     json.loads(question.model_dump_json()) for question in questions
            # ]
            # return all_questions, 200

    def post(self):
        new_question: Question = deserialize(request.get_json(), Question)
        question_service.add_question(new_question)
        return serialize(new_question), 201

    def delete(self, question_id=None):
        if question_id:
            question_service.delete_question(QuestionId(code=question_id))
            return "", 200
        else:
            return "", 401


api.add_resource(QuestionResource, "/questions", "/questions/<string:question_id>")
