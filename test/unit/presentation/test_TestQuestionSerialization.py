import unittest
from datetime import datetime
from typing import FrozenSet

from domain.common.core import AnswerId, Answer, QuestionId
from domain.common.core.enum import QuestionType
from domain.graph.core import GraphQuestion
from domain.graph.core.enum import Action
from domain.common.factories import AnswerFactory
from domain.graph.factories import GraphQuestionFactory
from presentation.presentation import serialize


class TestQuestionSerialization(unittest.TestCase):

    def setUp(self):
        self.answer: Answer = AnswerFactory.create_answer(
            AnswerId(code="answer"), "Always."
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
        self.question: GraphQuestion = GraphQuestionFactory.create_boolean_question(
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
                },
                {
                    "id": {"code": "boolean_question_id-true"},
                    "text": "Yes",
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
