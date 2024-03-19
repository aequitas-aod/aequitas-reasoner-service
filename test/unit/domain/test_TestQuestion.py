import unittest

from app.domain.core.QuestionId import QuestionId
from app.domain.factories.QuestionFactory import QuestionFactory


class TestQuestion(unittest.TestCase):

    def setUp(self):
        self.question = QuestionFactory().create_boolean_question(
            QuestionId("question1"), "Is this a test?"
        )

    def test_select_answer(self):
        self.question.select_answer(self.question._availableAnswers[0]).select_answer()
