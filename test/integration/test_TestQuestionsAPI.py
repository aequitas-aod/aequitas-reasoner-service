import json
import unittest
from typing import Set

from domain.core.commons import Question
from domain.core.commons import QuestionId
from domain.core.commons import QuestionType
from domain.factories import AnswerFactory
from domain.factories import QuestionFactory
from ws.main import create_app
from presentation.presentation import serialize, deserialize


class TestQuestionsAPI(unittest.TestCase):

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

    def test_get_all_questions(self):
        question2: Question = self.question.model_copy()
        question2.id = QuestionId(code="test-question-2")
        self.app.post("/questions", json=serialize(self.question))
        self.app.post("/questions", json=serialize(question2))
        response = self.app.get("/questions")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(json.loads(response.data)))
        all_questions: Set[Question] = set(
            [deserialize(question, Question) for question in json.loads(response.data)]
        )
        self.assertEqual({self.question, question2}, all_questions)

    def test_get_question(self):
        self.app.post("/questions", json=serialize(self.question))
        response = self.app.get("/questions/test-question")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.question, deserialize(json.loads(response.data), Question)
        )

    def test_get_non_existent_question(self):
        response = self.app.get("/questions/does-not-exist")
        self.assertEqual(response.status_code, 204)

    def test_insert_question(self):
        response = self.app.post("/questions", json=serialize(self.question))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            self.question, deserialize(json.loads(response.data), Question)
        )

    def test_delete_question(self):
        self.app.post("/questions", json=serialize(self.question))
        response = self.app.delete("/questions", json=serialize(self.question.id))
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/questions/test-question")
        self.assertEqual(response.status_code, 204)
