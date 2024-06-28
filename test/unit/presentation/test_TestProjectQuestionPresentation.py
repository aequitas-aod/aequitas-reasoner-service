import unittest
from datetime import datetime

from domain.common.core import AnswerId, QuestionId
from domain.common.core.enum import QuestionType
from domain.common.factories import AnswerFactory
from domain.project.core import ProjectQuestion
from domain.project.factories import ProjectQuestionFactory
from presentation.presentation import deserialize, serialize


class TestProjectQuestionPresentation(unittest.TestCase):

    def setUp(self):
        self.question_timestamp = datetime.now()
        self.question: ProjectQuestion = ProjectQuestionFactory.create_project_question(
            QuestionId(code="project_question_id"),
            "Do you practice TDD?",
            QuestionType.SINGLE_CHOICE,
            frozenset(
                {
                    AnswerFactory.create_answer(
                        AnswerId(code="project_question_id-false"), "No"
                    ),
                    AnswerFactory.create_answer(
                        AnswerId(code="project_question_id-true"), "Yes"
                    ),
                }
            ),
            created_at=self.question_timestamp,
            selected_answers=frozenset(
                {
                    AnswerFactory.create_answer(
                        AnswerId(code="project_question_id-false"), "No"
                    ),
                }
            ),
        )
        self.question_dict: dict = {
            "id": {"code": "project_question_id"},
            "text": "Do you practice TDD?",
            "type": QuestionType.SINGLE_CHOICE.value,
            "answers": [
                {
                    "id": {"code": "project_question_id-false"},
                    "text": "No",
                },
                {
                    "id": {"code": "project_question_id-true"},
                    "text": "Yes",
                },
            ],
            "created_at": self.question_timestamp.isoformat(),
            "selection_strategy": {"type": "single"},
            "selected_answers": [
                {
                    "id": {"code": "project_question_id-false"},
                    "text": "No",
                },
            ],
            "previous_question_id": None,
        }

    def test_deserialize_project_question(self):
        actual: ProjectQuestion = deserialize(self.question_dict, ProjectQuestion)
        self.assertEqual(
            self.question,
            actual,
        )

    def test_serialize_project_question(self):
        actual: dict = serialize(self.question)
        self.assertEqual(
            self.question_dict,
            actual,
        )
