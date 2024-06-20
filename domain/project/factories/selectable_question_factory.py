from datetime import datetime
from typing import FrozenSet, Optional

from domain.graph.core import Answer, AnswerId, QuestionId
from domain.graph.core.enum import Action, QuestionType
from domain.graph.factories import AnswerFactory
from domain.project.core import SelectableQuestion
from domain.project.core.selection import (
    MultipleSelectionStrategy,
    SingleSelectionStrategy,
)


class SelectableQuestionFactory:

    @staticmethod
    def create_selectable_question(
        question_id: QuestionId,
        text: str,
        question_type: QuestionType,
        available_answers: FrozenSet[Answer],
        previous_question_id: Optional[QuestionId] = None,
        enabled_by: FrozenSet[AnswerId] = frozenset(),
        action_needed: Optional[Action] = None,
        created_at: datetime = datetime.now(),
        selected_answers: FrozenSet[Answer] = frozenset(),
    ) -> SelectableQuestion:
        match question_type:
            case QuestionType.BOOLEAN:
                selection_strategy = SingleSelectionStrategy()
            case QuestionType.SINGLE_CHOICE:
                selection_strategy = SingleSelectionStrategy()
            case QuestionType.MULTIPLE_CHOICE:
                selection_strategy = MultipleSelectionStrategy()
            case QuestionType.RATING:
                selection_strategy = SingleSelectionStrategy()
            case _:
                raise ValueError(f"Unsupported question type {question_type}")

        return SelectableQuestion(
            id=question_id,
            text=text,
            type=question_type,
            available_answers=available_answers,
            previous_question_id=previous_question_id,
            enabled_by=enabled_by,
            action_needed=action_needed,
            created_at=created_at,
            selection_strategy=selection_strategy,
            selected_answers=selected_answers,
        )

    @staticmethod
    def create_selectable_boolean_question(
        question_id: QuestionId,
        text: str,
        previous_question_id: Optional[QuestionId] = None,
        enabled_by: FrozenSet[AnswerId] = frozenset(),
        action_needed: Optional[Action] = None,
        created_at: datetime = datetime.now(),
    ) -> SelectableQuestion:
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
        return SelectableQuestionFactory.create_selectable_question(
            question_id,
            text,
            QuestionType.BOOLEAN,
            available_answers,
            previous_question_id,
            enabled_by,
            action_needed,
            created_at,
        )
