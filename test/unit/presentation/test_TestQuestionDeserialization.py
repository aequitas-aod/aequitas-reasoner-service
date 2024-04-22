import unittest

from domain.core.commons import Answer
from domain.core.commons import Question
from domain.core.commons import QuestionId
from domain.core.commons import Action
from domain.core.commons import QuestionType
from domain.factories import AnswerFactory
from domain.factories import QuestionFactory
from presentation.presentation import deserialize


class TestQuestionDeserialization(unittest.TestCase):

    def setUp(self):
        self.answer = {"text": "Always.", "value": "always"}
        self.boolean_answer = {"text": "No", "value": "False"}
        self.question: dict = {
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

    def test_deserialize_answer(self):
        expected: Answer = AnswerFactory().create_answer("Always.", "always")
        actual: Answer = deserialize(self.answer, Answer)
        self.assertEqual(
            expected,
            actual,
        )

    def test_deserialize_boolean_answer(self):
        expected: Answer = AnswerFactory().create_boolean_answer(False)
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
