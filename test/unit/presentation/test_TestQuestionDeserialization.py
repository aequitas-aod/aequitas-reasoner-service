import unittest
from datetime import datetime

from domain.common.core import AnswerId, Answer, QuestionId
from domain.common.core.enum import QuestionType
from domain.graph.core import GraphQuestion
from domain.graph.core.enum import Action
from domain.common.factories import AnswerFactory
from domain.graph.factories import GraphQuestionFactory
from presentation.presentation import deserialize


class TestQuestionDeserialization(unittest.TestCase):

    def setUp(self):
        self.answer = {"id": {"code": "answer"}, "text": "Always."}
        self.boolean_answer = {
            "id": {"code": "boolean-answer"},
            "text": "No",
        }
        self.question_timestamp = datetime.now()
        self.question: dict = {
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
            "previous_question_id": None,
            "enabled_by": [{"code": "answer-code"}],
            "action_needed": Action.METRICS_CHECK.value,
            "created_at": self.question_timestamp.isoformat(),
        }

    def test_deserialize_answer(self):
        expected: Answer = AnswerFactory.create_answer(
            AnswerId(code="answer"), "Always."
        )
        actual: Answer = deserialize(self.answer, Answer)
        self.assertEqual(
            expected,
            actual,
        )

    def test_deserialize_boolean_answer(self):
        expected: Answer = AnswerFactory.create_boolean_answer(
            AnswerId(code="boolean-answer"), False
        )
        actual: Answer = deserialize(self.boolean_answer, Answer)
        self.assertEqual(
            expected,
            actual,
        )

    def test_deserialize_question(self):
        expected: GraphQuestion = GraphQuestionFactory.create_boolean_question(
            QuestionId(code="boolean_question_id"),
            "Do you practice TDD?",
            enabled_by=frozenset({AnswerId(code="answer-code")}),
            action_needed=Action.METRICS_CHECK,
            created_at=self.question_timestamp,
        )
        actual: GraphQuestion = deserialize(self.question, GraphQuestion)
        self.assertEqual(
            expected,
            actual,
        )
