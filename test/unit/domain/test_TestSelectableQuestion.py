import unittest
from datetime import datetime

from domain.graph.core import Answer, AnswerId, QuestionId
from domain.graph.core.enum import QuestionType
from domain.graph.factories.answer_factory import AnswerFactory
from domain.project.core import SelectableQuestion
from domain.project.factories import SelectableQuestionFactory


class TestSelectableQuestion(unittest.TestCase):

    def setUp(self):
        self.question_timestamp = datetime.now()
        self.question: SelectableQuestion = (
            SelectableQuestionFactory.create_selectable_question(
                QuestionId(code="question_id"),
                "Do you practice TDD?",
                QuestionType.SINGLE_CHOICE,
                frozenset(
                    {
                        Answer(
                            id=AnswerId(code="answer-always"),
                            text="Always",
                            value="always",
                        ),
                        Answer(
                            id=AnswerId(code="answer-never"),
                            text="Never",
                            value="never",
                        ),
                    }
                ),
                created_at=self.question_timestamp,
            )
        )

    def test_select_answer(self):
        answer, _ = self.question.available_answers
        question: SelectableQuestion = self.question.select_answer(answer)
        self.assertEqual(question.selected_answers, {answer})

    def test_select_answer_twice(self):
        answer, _ = self.question.available_answers
        question: SelectableQuestion = self.question.select_answer(
            answer
        ).select_answer(answer)
        self.assertEqual(question.selected_answers, {answer})

    def test_select_wrong_answer(self):
        self.assertRaises(
            ValueError,
            lambda: self.question.select_answer(
                Answer(text="this is not in the available answers", value="whatever")
            ),
        )

    def test_deselect_answer(self):
        answer, _ = self.question.available_answers
        question: SelectableQuestion = self.question.select_answer(
            answer
        ).deselect_answer(answer)
        self.assertEqual(question.selected_answers, frozenset())

    def test_deselect_not_selected_answer(self):
        answer, _ = self.question.available_answers
        question: SelectableQuestion = self.question.deselect_answer(answer)
        self.assertEqual(question.selected_answers, frozenset())


class TestBooleanQuestion(unittest.TestCase):
    def setUp(self):
        self.question: SelectableQuestion = (
            SelectableQuestionFactory.create_selectable_boolean_question(
                QuestionId(code="boolean_question_id"), "Do you practice TDD?"
            )
        )

    def test_boolean_answers(self):
        self.assertEqual(
            self.question.available_answers,
            frozenset(
                {
                    AnswerFactory.create_boolean_answer(
                        AnswerId(code="boolean_question_id-true"), True
                    ),
                    AnswerFactory.create_boolean_answer(
                        AnswerId(code="boolean_question_id-false"), False
                    ),
                }
            ),
        )
