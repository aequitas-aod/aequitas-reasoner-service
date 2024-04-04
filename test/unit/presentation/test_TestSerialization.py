import unittest

from app.domain.core import Answer
from app.domain.core import Question
from app.domain.core import QuestionId
from app.domain.core.enum import Action
from app.domain.core.enum import QuestionType
from app.domain.factories import AnswerFactory
from app.domain.factories import QuestionFactory
from app.presentation.presentation import serialize


class TestSerialization(unittest.TestCase):

    def setUp(self):
        self.answer: Answer = AnswerFactory().create_answer("Always.", "always")
        self.boolean_answer: Answer = AnswerFactory().create_boolean_answer(False)
        self.question: Question = QuestionFactory().create_boolean_question(
            QuestionId(code="boolean_question_id"),
            "Do you practice TDD?",
            Action.METRICS_CHECK,
        )

    def test_serialize_answer(self):
        expected: dict = {"text": "Always.", "value": "always"}
        actual: dict = serialize(self.answer)
        self.assertEqual(
            expected,
            actual,
        )

    def test_serialize_boolean_answer(self):
        expected: dict = {"text": "No", "value": "False"}
        actual: dict = serialize(self.boolean_answer)
        self.assertEqual(
            expected,
            actual,
        )

    def test_serialize_question(self):
        expected: dict = {
            "id": {"code": "boolean_question_id"},
            "text": "Do you practice TDD?",
            "type": QuestionType.BOOLEAN.value,
            "available_answers": [
                {"text": "No", "value": "False"},
                {"text": "Yes", "value": "True"},
            ],
            "selected_answers": [],
            "action_needed": Action.METRICS_CHECK.value,
        }
        actual: dict = serialize(self.question)
        self.assertEqual(
            expected,
            actual,
        )
