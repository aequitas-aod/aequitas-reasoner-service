from typing import Set

from app.domain.core.Answer import Answer
from app.domain.core.Question import Question
from app.domain.core.enum.Action import Action
from app.domain.core.enum.QuestionType import QuestionType
from app.domain.factories.AnswerFactory import AnswerFactory


class QuestionFactory:

    def __init__(self):
        self._answer_factory = AnswerFactory()

    def create_question(
        self,
        text: str,
        question_type: QuestionType,
        available_answers: Set[Answer],
        selected_answers: Set[Answer] = None,
        action_needed: Action = None,
    ) -> Question:
        return Question(
            text,
            question_type,
            frozenset(available_answers),
            selected_answers,
            action_needed,
        )

    def create_boolean_question(
        self, text: str, action_needed: Action = None
    ) -> Question:
        available_answers: Set[Answer] = {
            self._answer_factory.create_boolean_answer(True),
            self._answer_factory.create_boolean_answer(False),
        }
        return Question(
            text,
            QuestionType.BOOLEAN,
            frozenset(available_answers),
            action_needed=action_needed,
        )
