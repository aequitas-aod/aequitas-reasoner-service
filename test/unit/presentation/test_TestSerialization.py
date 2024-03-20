import json
import unittest

from app.domain.core.QuestionId import QuestionId
from app.domain.core.enum.Action import Action
from app.domain.core.enum.QuestionType import QuestionType
from app.domain.factories.AnswerFactory import AnswerFactory
from app.domain.factories.QuestionFactory import QuestionFactory


class TestSerialization(unittest.TestCase):

    def setUp(self):
        self.answer = AnswerFactory().create_answer("Always.", "always")
        self.boolean_answer = AnswerFactory().create_boolean_answer(False)
        self.question = QuestionFactory().create_boolean_question(
            QuestionId(code="boolean_question_id"),
            "Do you practice TDD?",
            Action.METRICS_CHECK,
        )

    def test_serialize_answer(self):
        expected: dict = {"text": "Always.", "value": "always"}
        actual: dict = json.loads(self.answer.model_dump_json())
        self.assertEqual(
            expected,
            actual,
        )

    def test_serialize_boolean_answer(self):
        expected: dict = {"text": "No", "value": "False"}
        actual: dict = json.loads(self.boolean_answer.model_dump_json())
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
        actual: dict = json.loads(self.question.model_dump_json())
        self.assertEqual(
            expected,
            actual,
        )
