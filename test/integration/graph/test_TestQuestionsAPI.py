import json
import unittest
from datetime import datetime
from typing import Set

from python_on_whales import DockerClient

from domain.graph.core import Question, QuestionId, AnswerId
from domain.graph.core.enum import QuestionType
from domain.graph.factories import AnswerFactory, QuestionFactory
from presentation.presentation import serialize, deserialize
from ws.main import create_app


class TestQuestionsAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.docker = DockerClient()
        cls.docker.compose.down(volumes=True)
        cls.docker.compose.up(detach=True, wait=True)
        cls.app = create_app().test_client()
        cls.question_timestamp = datetime.now()
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
            created_at=cls.question_timestamp,
        )
        cls.question2: Question = QuestionFactory().create_boolean_question(
            QuestionId(code="test-question-2"), "Test question 2",
            created_at=cls.question_timestamp,
        )

    @classmethod
    def tearDownClass(cls):
        cls.docker.compose.down(volumes=True)

    def tearDown(self):
        self.__delete_all_questions()

    def __delete_all_questions(self):
        response = self.app.get("/questions")
        questions_dict = json.loads(response.data)
        for question in questions_dict:
            self.app.delete(f"/questions/{question['id']['code']}")

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

    def test_get_question(self):
        self.app.post("/questions", json=serialize(self.question))
        response = self.app.get(f"/questions/{self.question.id.code}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.question, deserialize(json.loads(response.data), Question)
        )

    def test_get_non_existent_question(self):
        response = self.app.get("/questions/does-not-exist")
        self.assertEqual(response.status_code, 404)

    def test_insert_question(self):
        response = self.app.post("/questions", json=serialize(self.question))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            self.question.id, deserialize(json.loads(response.data), QuestionId)
        )

    def test_insert_duplicate_question(self):
        self.app.post("/questions", json=serialize(self.question))
        response = self.app.post("/questions", json=serialize(self.question))
        self.assertEqual(response.status_code, 409)

    def test_update_question(self):
        self.app.post("/questions", json=serialize(self.question))
        updated_question: Question = self.question.model_copy()
        updated_question.text = "Updated text"
        updated_question.type = QuestionType.MULTIPLE_CHOICE
        response = self.app.put(
            f"/questions/{self.question.id.code}", json=serialize(updated_question)
        )
        self.assertEqual(response.status_code, 200)
        response = self.app.get(f"/questions/{self.question.id.code}")
        self.assertEqual(
            updated_question, deserialize(json.loads(response.data), Question)
        )
        response = self.app.put(
            f"/questions/{self.question2.id.code}", json=serialize(self.question)
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.data), "Updated question id does not match"
        )

    def test_delete_question(self):
        self.app.post("/questions", json=serialize(self.question))
        response = self.app.delete(f"/questions/{self.question.id.code}")
        self.assertEqual(response.status_code, 200)
        response = self.app.get(f"/questions/{self.question.id.code}")
        self.assertEqual(response.status_code, 404)

    def test_delete_non_existent_question(self):
        response = self.app.delete("/questions/does-not-exist")
        self.assertEqual(response.status_code, 404)

    def test_get_new_candidate_id(self):
        response = self.app.get("/questions/new-candidate-id")
        self.assertEqual(response.status_code, 200)
        expected_question_id = serialize(QuestionId(code="q-1"))
        self.assertEqual(expected_question_id, json.loads(response.data))
        self.app.post("/questions", json=serialize(self.question))
        response = self.app.get("/questions/new-candidate-id")
        self.assertEqual(response.status_code, 200)
        expected_question_id = serialize(QuestionId(code="q-2"))
        self.assertEqual(expected_question_id, json.loads(response.data))

    def test_get_new_candidate_id_after_deletion(self):
        self.app.post("/questions", json=serialize(self.question))
        self.app.delete(f"/questions/{self.question.id.code}")
        response = self.app.get("/questions/new-candidate-id")
        self.assertEqual(response.status_code, 200)
        expected_question_id = serialize(QuestionId(code="q-1"))
        self.assertEqual(expected_question_id, json.loads(response.data))

    def test_last_inserted_question(self):
        self.app.post("/questions", json=serialize(self.question))
        response = self.app.get("/questions/last-inserted")
        self.assertEqual(response.status_code, 200)
        expected_question = serialize(self.question)
        self.assertEqual(expected_question, json.loads(response.data))
        self.app.post("/questions", json=serialize(self.question2))
        response = self.app.get("/questions/last-inserted")
        self.assertEqual(response.status_code, 200)
        expected_question = serialize(self.question2)
        self.assertEqual(expected_question, json.loads(response.data))
