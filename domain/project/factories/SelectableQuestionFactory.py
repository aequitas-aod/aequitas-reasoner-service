from typing import FrozenSet

from domain.graph.core import Answer, QuestionId, AnswerId
from domain.graph.core.enum import Action, QuestionType
from domain.graph.factories.AnswerFactory import AnswerFactory
from domain.project.core import SelectableQuestion
from domain.project.core.selection import SingleSelectionStrategy, MultipleSelectionStrategy


class SelectableQuestionFactory:

    def __init__(self):
        self._answer_factory = AnswerFactory()

    def create_question(
            self,
            question_id: QuestionId,
            text: str,
            question_type: QuestionType,
            available_answers: FrozenSet[Answer],
            action_needed: Action = None,
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
            action_needed=action_needed,
            selection_strategy=selection_strategy,
            selected_answers=selected_answers,
        )

    def create_boolean_question(
            self,
            question_id: QuestionId,
            text: str,
            action_needed: Action = None,
    ) -> SelectableQuestion:
        available_answers: FrozenSet[Answer] = frozenset(
            {
                self._answer_factory.create_boolean_answer(AnswerId(code=f"{question_id.code}-true"), True),
                self._answer_factory.create_boolean_answer(AnswerId(code=f"{question_id.code}-false"), False),
            }
        )
        return self.create_question(
            question_id,
            text,
            QuestionType.BOOLEAN,
            available_answers,
            action_needed
        )
