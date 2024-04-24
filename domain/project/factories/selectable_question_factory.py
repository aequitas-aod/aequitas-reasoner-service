from typing import FrozenSet, Optional

from domain.graph.core.answer import Answer
from domain.graph.core.answer_id import AnswerId
from domain.graph.core.enum.action import Action
from domain.graph.core.enum.question_type import QuestionType
from domain.graph.core.question_id import QuestionId
from domain.graph.factories.answer_factory import AnswerFactory
from domain.project.core.selectable_question import SelectableQuestion
from domain.project.core.selection.multiple_selection_strategy import MultipleSelectionStrategy
from domain.project.core.selection.single_selection_strategy import SingleSelectionStrategy


class SelectableQuestionFactory:

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
            action_needed=action_needed,
            selection_strategy=selection_strategy,
            selected_answers=selected_answers,
        )

    def create_boolean_question(
            self,
            question_id: QuestionId,
            text: str,
            previous_question_id: Optional[QuestionId] = None,
            action_needed: Optional[Action] = None,
    ) -> SelectableQuestion:
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
