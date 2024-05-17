import json
import unittest
from typing import Set

from python_on_whales import DockerClient

from domain.graph.core import Question, QuestionId, AnswerId
from domain.graph.core.enum import QuestionType
from domain.graph.factories import AnswerFactory, QuestionFactory
from presentation.presentation import serialize, deserialize
from ws.main import create_app
from ws.utils.logger import logger


class TestQuestionsAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.docker = DockerClient(compose_env_file=".env")
        cls.docker.compose.down(volumes=True)
        cls.docker.compose.up(detach=True, wait=True)
        cls.app = create_app().test_client()
        cls.question: Question = QuestionFactory().create_question(
            QuestionId(code="test-question"),
            "Test question",
            QuestionType.SINGLE_CHOICE,
            frozenset(
                {
                    AnswerFactory().create_answer(
                        AnswerId(code="answer-yes"), "Yes", "yes"
                    ),
                    AnswerFactory().create_answer(
                        AnswerId(code="answer-little-bit"), "A little bit", "little-bit"
                    ),
                    AnswerFactory().create_answer(
                        AnswerId(code="answer-no"), "No", "no"
                    ),
                }
            ),
        )
        cls.question2: Question = QuestionFactory().create_boolean_question(
            QuestionId(code="test-question-2"), "Test question 2"
        )

    @classmethod
    def tearDownClass(cls):
        cls.docker.compose.down(volumes=True)

    def test_get_all_questions(self):
        self.app.post("/questions", json=serialize(self.question))
        self.app.post("/questions", json=serialize(self.question2))
        response = self.app.get("/questions")
        questions_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(questions_dict))
        all_questions: Set[Question] = set(
            [deserialize(question, Question) for question in questions_dict]
        )
        self.assertEqual({self.question, self.question2}, all_questions)
        self.app.delete(f"/questions/{self.question.id.code}")
        self.app.delete(f"/questions/{self.question2.id}")

    def test_get_question(self):
        self.app.post("/questions", json=serialize(self.question))
        response = self.app.get(f"/questions/{self.question.id.code}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.question, deserialize(json.loads(response.data), Question)
        )
        self.app.delete(f"/questions/{self.question.id.code}")

    def test_get_non_existent_question(self):
        response = self.app.get("/questions/does-not-exist")
        self.assertEqual(response.status_code, 204)

    def test_insert_question(self):
        response = self.app.post("/questions", json=serialize(self.question))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            self.question, deserialize(json.loads(response.data), Question)
        )
        self.app.delete(f"/questions/{self.question.id.code}")

    def test_delete_question(self):
        self.app.post("/questions", json=serialize(self.question))
        response = self.app.delete(f"/questions/{self.question.id.code}")
        self.assertEqual(response.status_code, 200)
        response = self.app.get(f"/questions/{self.question.id.code}")
        self.assertEqual(response.status_code, 204)
        self.app.delete(f"/questions/{self.question.id.code}")
