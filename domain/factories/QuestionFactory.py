from typing import FrozenSet

from domain.core.commons import Action
from domain.core.commons import Answer
from domain.core.commons import Question
from domain.core.commons import QuestionId
from domain.core.commons import QuestionType
from domain.factories.AnswerFactory import AnswerFactory


class QuestionFactory:

    def __init__(self):
        self._answer_factory = AnswerFactory()

    def create_question(
            self,
            question_id: QuestionId,
            text: str,
            question_type: QuestionType,
            available_answers: FrozenSet[Answer],
            action_needed: Action = None,
    ) -> Question:
        return Question(
            id=question_id,
            text=text,
            type=question_type,
            available_answers=available_answers,
            action_needed=action_needed,
        )

    def create_boolean_question(
            self, question_id: QuestionId, text: str, action_needed: Action = None
    ) -> Question:
        available_answers: FrozenSet[Answer] = frozenset(
            {
                self._answer_factory.create_boolean_answer(True),
                self._answer_factory.create_boolean_answer(False),
            }
        )
        return self.create_question(
            question_id,
            text,
            QuestionType.BOOLEAN,
            available_answers,
            action_needed,
        )
