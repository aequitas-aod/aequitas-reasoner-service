import unittest

from app.domain.core.Question import Question
from app.domain.factories.QuestionFactory import QuestionFactory


class TestQuestion(unittest.TestCase):

    def setUp(self):
        self.question = QuestionFactory().create_boolean_question(
            "1", "Is this a test?"
        )
