import unittest

from domain.graph.core import Answer, Question, QuestionId, AnswerId
from domain.graph.core.enum import Action, QuestionType
from domain.graph.factories import AnswerFactory, QuestionFactory
from presentation.presentation import deserialize


class TestQuestionDeserialization(unittest.TestCase):

    def setUp(self):
        self.answer = {"id": {"code": "answer"}, "text": "Always.", "value": "always"}
        self.boolean_answer = {"id": {"code": "boolean-answer"}, "text": "No", "value": "False"}
        self.question: dict = {
            "id": {"code": "boolean_question_id"},
            "text": "Do you practice TDD?",
            "type": QuestionType.BOOLEAN.value,
            "available_answers": [
                {"id": {"code": "boolean_question_id-false"}, "text": "No", "value": "False"},
                {"id": {"code": "boolean_question_id-true"}, "text": "Yes", "value": "True"},
            ],
            "selected_answers": [],
            "action_needed": Action.METRICS_CHECK.value,
        }

    def test_deserialize_answer(self):
        expected: Answer = AnswerFactory().create_answer(AnswerId(code="answer"), "Always.", "always")
        actual: Answer = deserialize(self.answer, Answer)
        self.assertEqual(
            expected,
            actual,
        )

    def test_deserialize_boolean_answer(self):
        expected: Answer = AnswerFactory().create_boolean_answer(AnswerId(code="boolean-answer"), False)
        actual: Answer = deserialize(self.boolean_answer, Answer)
        self.assertEqual(
            expected,
            actual,
        )

    def test_deserialize_question(self):
        expected: Question = QuestionFactory().create_boolean_question(
            QuestionId(code="boolean_question_id"),
            "Do you practice TDD?",
            Action.METRICS_CHECK,
        )
        actual: Question = deserialize(self.question, Question)
        self.assertEqual(
            expected,
            actual,
        )
