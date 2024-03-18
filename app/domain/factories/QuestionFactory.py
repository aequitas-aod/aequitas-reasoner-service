from typing import List

from app.domain.core.Answer import Answer
from app.domain.core.Question import Question
from app.domain.core.QuestionId import QuestionId
from app.domain.core.enum.Action import Action
from app.domain.core.enum.QuestionType import QuestionType
from app.domain.factories.AnswerFactory import AnswerFactory


class QuestionFactory:

    def __init__(self):
        self._answer_factory = AnswerFactory()

    def create_question(
        self,
        question_id: QuestionId,
        text: str,
        question_type: QuestionType,
        available_answers: List[Answer],
        selected_answer: List[Answer],
        action_needed: Action,
    ) -> Question:
        return Question(
            question_id,
            text,
            question_type,
            available_answers,
            selected_answer,
            action_needed,
        )

    def create_boolean_question(
        self, question_id: QuestionId, text: str, action_needed: Action = None
    ) -> Question:
        available_answers: List[Answer] = [
            self._answer_factory.create_boolean_answer(True),
            self._answer_factory.create_boolean_answer(False),
        ]
        return Question(
            question_id,
            text,
            QuestionType.BOOLEAN,
            available_answers,
            [],
            action_needed,
        )
