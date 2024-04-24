from typing import FrozenSet, Optional

from domain.graph.core.answer import Answer
from domain.graph.core.answer_id import AnswerId
from domain.graph.core.enum.action import Action
from domain.graph.core.enum.question_type import QuestionType
from domain.graph.core.question import Question
from domain.graph.core.question_id import QuestionId
from domain.graph.factories.answer_factory import AnswerFactory


class QuestionFactory:

    def __init__(self):
        self._answer_factory = AnswerFactory()

    def create_question(
            self,
            question_id: QuestionId,
            text: str,
            question_type: QuestionType,
            available_answers: FrozenSet[Answer],
            previous_question_id: Optional[QuestionId] = None,
            action_needed: Optional[Action] = None,
    ) -> Question:
        return Question(
            id=question_id,
            text=text,
            type=question_type,
            available_answers=available_answers,
            previous_question_id=previous_question_id,
            action_needed=action_needed,
        )

    def create_boolean_question(
            self,
            question_id: QuestionId,
            text: str,
            previous_question_id: Optional[QuestionId] = None,
            action_needed: Optional[Action] = None,
    ) -> Question:
        available_answers: FrozenSet[Answer] = frozenset(
            {
                self._answer_factory.create_boolean_answer(
                    AnswerId(code=f"{question_id.code}-true"), True
                ),
                self._answer_factory.create_boolean_answer(
                    AnswerId(code=f"{question_id.code}-false"), False
                ),
            }
        )
        return self.create_question(
            question_id,
            text,
            QuestionType.BOOLEAN,
            available_answers,
            previous_question_id,
            action_needed,
        )