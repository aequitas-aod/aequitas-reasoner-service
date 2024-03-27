import json
import logging
import unittest

from app.domain.core.Question import Question
from app.domain.core.QuestionId import QuestionId
from app.domain.core.enum.Action import Action
from app.domain.core.enum.QuestionType import QuestionType
from app.domain.factories.AnswerFactory import AnswerFactory
from app.domain.factories.QuestionFactory import QuestionFactory
from app.main import create_app
from app.presentation.presentation import (
    deserialize_question,
    serialize_question,
    serialize_question_id,
)


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        self.question: Question = QuestionFactory().create_question(
            QuestionId(code="test-question"),
            "Test question",
            QuestionType.SINGLE_CHOICE,
            frozenset(
                {
                    AnswerFactory().create_answer("Yes", "yes"),
                    AnswerFactory().create_answer("A little bit", "little-bit"),
                    AnswerFactory().create_answer("No", "no"),
                }
            ),
        )

    def test_get_question(self):
        self.app.post("/questions", json=serialize_question(self.question))
        response = self.app.get("/questions/test-question")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.question, deserialize_question(json.loads(response.data)))

    def test_get_non_existent_question(self):
        response = self.app.get("/questions/does-not-exist")
        self.assertEqual(response.status_code, 204)

    def test_insert_question(self):
        response = self.app.post("/questions", json=serialize_question(self.question))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.question, deserialize_question(json.loads(response.data)))

    def test_delete_question(self):
        self.app.post("/questions", json=serialize_question(self.question))
        response = self.app.delete(
            "/questions", json=serialize_question_id(self.question.id)
        )
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/questions/test-question")
        self.assertEqual(response.status_code, 204)
