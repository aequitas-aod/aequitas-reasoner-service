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
            )
        )
        self.app.post("/questions", json=json.loads(self.question.model_dump_json()))

    def test_get_question_by_id(self):
        pass
        # response = self.app.get("/questions/test-question")
        # self.assertEqual(response.status_code, 200)
        # logging.Logger("test").info(response.data)
        # self.assertEqual(self.question, response.data.__dict__)

    def test_echo(self):
        pass
        # response = self.app.get("/echo/test")
        # self.assertEqual(response.status_code, 200)
        # self.assertIn(b"test", response.data)
