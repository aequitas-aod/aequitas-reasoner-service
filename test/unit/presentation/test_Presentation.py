import unittest

from app.domain.core.enum.Action import Action
from app.domain.factories.QuestionFactory import QuestionFactory


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.question = QuestionFactory().create_boolean_question(
            "Do you practice TDD?",
            Action.METRICS_CHECK
        )

    def test_question_serialize(self):
        self.assertEqual(
            self.question.model_dump_json(),
            {
                "id": str(self.question.id),
                "text": "Do you practice TDD?",
                "type": "boolean",
                "action_needed": "metrics_check",
            },
        )
