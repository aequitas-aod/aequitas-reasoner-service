from typing import FrozenSet

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
        available_answers: FrozenSet[Answer],
        selected_answers: FrozenSet[Answer] = frozenset(),
        action_needed: Action = None,
    ) -> Question:
        return Question(
            text=text,
            type=question_type,
            available_answers=available_answers,
            selected_answers=selected_answers,
            action_needed=action_needed,
        )

    def create_boolean_question(
        self, text: str, action_needed: Action = None
    ) -> Question:
        available_answers: FrozenSet[Answer] = frozenset(
            {
                self._answer_factory.create_boolean_answer(True),
                self._answer_factory.create_boolean_answer(False),
            }
        )
        return Question(
            text=text,
            type=QuestionType.BOOLEAN,
            available_answers=available_answers,
            action_needed=action_needed,
        )
