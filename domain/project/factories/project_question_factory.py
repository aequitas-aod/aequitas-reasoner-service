from datetime import datetime
from typing import FrozenSet

from domain.common.core import Answer, AnswerId, QuestionId
from domain.common.core.enum import QuestionType
from domain.common.factories import AnswerFactory
from domain.project.core import ProjectQuestion
from domain.project.core.selection import (
    MultipleSelectionStrategy,
    SingleSelectionStrategy,
)


class ProjectQuestionFactory:

    @staticmethod
    def create_selectable_question(
        question_id: QuestionId,
        text: str,
        question_type: QuestionType,
        available_answers: FrozenSet[Answer],
        created_at: datetime = datetime.now(),
        selected_answers: FrozenSet[Answer] = frozenset(),
    ) -> ProjectQuestion:
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

        if len(selected_answers) > 0 and question_type != QuestionType.MULTIPLE_CHOICE:
            raise ValueError("Selected answers are only allowed for multiple choice questions")
        return ProjectQuestion(
            id=question_id,
            text=text,
            type=question_type,
            available_answers=available_answers,
            created_at=created_at,
            selection_strategy=selection_strategy,
            selected_answers=selected_answers,
        )

    @staticmethod
    def create_selectable_boolean_question(
        question_id: QuestionId,
        text: str,
        created_at: datetime = datetime.now(),
    ) -> ProjectQuestion:
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
        return ProjectQuestionFactory.create_selectable_question(
            question_id,
            text,
            QuestionType.BOOLEAN,
            available_answers,
            created_at,
        )
