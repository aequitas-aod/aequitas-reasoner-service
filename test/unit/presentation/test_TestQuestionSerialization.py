import unittest
from datetime import datetime
from typing import FrozenSet

from domain.graph.core import AnswerId, Answer, QuestionId, Question
from domain.graph.core.enum import Action, QuestionType
from domain.graph.factories import AnswerFactory
from domain.graph.factories import QuestionFactory
from presentation.presentation import serialize


class TestQuestionSerialization(unittest.TestCase):

    def setUp(self):
        self.answer: Answer = AnswerFactory.create_answer(
            AnswerId(code="answer"), "Always.", "always"
        )
        self.boolean_answer: Answer = AnswerFactory.create_boolean_answer(
            AnswerId(code="boolean-answer"), False
        )
        self.enabled_by: FrozenSet[AnswerId] = frozenset(
            {
                AnswerId(code="enabling-answer-1"),
                AnswerId(code="enabling-answer-2"),
            }
        )
        self.question_timestamp = datetime.now()
        self.question: Question = QuestionFactory().create_boolean_question(
            QuestionId(code="boolean_question_id"),
            "Do you practice TDD?",
            QuestionId(code="previous_question_id"),
            self.enabled_by,
            Action.METRICS_CHECK,
            self.question_timestamp,
        )

    def test_serialize_answer(self):
        expected: dict = {
            "id": {"code": "answer"},
            "text": "Always.",
            "value": "always",
        }
        actual: dict = serialize(self.answer)
        self.assertEqual(
            expected,
            actual,
        )

    def test_serialize_boolean_answer(self):
        expected: dict = {
            "id": {"code": "boolean-answer"},
            "text": "No",
            "value": "False",
        }
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
                {
                    "id": {"code": "boolean_question_id-false"},
                    "text": "No",
                    "value": "False",
                },
                {
                    "id": {"code": "boolean_question_id-true"},
                    "text": "Yes",
                    "value": "True",
                },
            ],
            "previous_question_id": {"code": "previous_question_id"},
            "enabled_by": [
                {"code": "enabling-answer-1"},
                {"code": "enabling-answer-2"},
            ],
            "action_needed": Action.METRICS_CHECK.value,
            "created_at": self.question_timestamp.isoformat(),
        }
        actual: dict = serialize(self.question)
        self.assertEqual(
            expected,
            actual,
        )
