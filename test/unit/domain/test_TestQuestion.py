import unittest

from app.domain.core.Answer import Answer
from app.domain.core.QuestionId import QuestionId
from app.domain.core.enum.QuestionType import QuestionType
from app.domain.factories.QuestionFactory import QuestionFactory


class TestQuestion(unittest.TestCase):

    def setUp(self):
        self.question = QuestionFactory().create_question(
            "Do you practice TDD?",
            QuestionType.SINGLE_CHOICE,
            {Answer("Always", "always"), Answer("Never", "never")},
        )

    def test_question_id(self):
        self.assertEqual(
            self.question.id,
            QuestionId(
                str(
                    hash(
                        (
                            self.question.text,
                            self.question.type,
                            self.question.available_answers,
                            self.question.selected_answers,
                            self.question.action_needed,
                        )
                    )
                )
            ),
        )

    def test_select_answer(self):
        answer, _ = self.question.available_answers
        question = self.question.select_answer(answer)
        self.assertEqual(question.selected_answers, {answer})

    def test_select_answer_twice(self):
        answer, _ = self.question.available_answers
        question = self.question.select_answer(answer).select_answer(answer)
        self.assertEqual(question.selected_answers, {answer})

    def test_select_wrong_answer(self):
        self.assertRaises(
            ValueError,
            lambda: self.question.select_answer(
                Answer("this is not in the available answers", "whatever")
            ),
        )
