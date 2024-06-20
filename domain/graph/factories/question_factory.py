from datetime import datetime
from typing import FrozenSet, Optional

from domain.graph.core import Answer, AnswerId, QuestionId, Question
from domain.graph.core.enum import Action, QuestionType
from domain.graph.factories import AnswerFactory


class QuestionFactory:

    @staticmethod
    def create_question(
        question_id: QuestionId,
        text: str,
        question_type: QuestionType,
        available_answers: FrozenSet[Answer],
        previous_question_id: Optional[QuestionId] = None,
        enabled_by: FrozenSet[AnswerId] = frozenset(),
        action_needed: Optional[Action] = None,
        created_at: datetime = datetime.now(),
    ) -> Question:
        return Question(
            id=question_id,
            text=text,
            type=question_type,
            available_answers=available_answers,
            previous_question_id=previous_question_id,
            enabled_by=enabled_by,
            action_needed=action_needed,
            created_at=created_at,
        )

    @staticmethod
    def create_boolean_question(
        question_id: QuestionId,
        text: str,
        previous_question_id: Optional[QuestionId] = None,
        enabled_by: FrozenSet[AnswerId] = frozenset(),
        action_needed: Optional[Action] = None,
        created_at: datetime = datetime.now(),
    ) -> Question:
        available_answers: FrozenSet[Answer] = frozenset(
            {
                AnswerFactory.create_boolean_answer(
                    AnswerId(code=f"{question_id.code}-true"), True
                ),
                AnswerFactory.create_boolean_answer(
                    AnswerId(code=f"{question_id.code}-false"), False
                ),
            }
        )
        return QuestionFactory.create_question(
            question_id,
            text,
            QuestionType.BOOLEAN,
            available_answers,
            previous_question_id,
            enabled_by,
            action_needed,
            created_at,
        )
