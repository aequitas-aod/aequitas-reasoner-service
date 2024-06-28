from typing import FrozenSet, Any, Optional

from pydantic import field_serializer, field_validator
from typing_extensions import Self

from domain.common.core import Answer, QuestionId
from domain.common.core import Question
from domain.project.core.selection import (
    SelectionStrategy,
    SingleSelectionStrategy,
    MultipleSelectionStrategy,
)


class ProjectQuestion(Question):
    selection_strategy: SelectionStrategy
    selected_answers: FrozenSet[Answer]
    previous_question_id: Optional[QuestionId]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def select_answer(self, answer: Answer) -> Self:
        if answer not in self.answers:
            raise ValueError(f"Answer {answer} is not available for this question")
        selected_answers: FrozenSet[Answer] = self.selection_strategy.select_answer(
            answer, self.selected_answers
        )
        return ProjectQuestion(
            id=self.id,
            text=self.text,
            type=self.type,
            answers=self.answers,
            created_at=self.created_at,
            selection_strategy=self.selection_strategy,
            selected_answers=selected_answers,
            previous_question_id=self.previous_question_id,
        )

    def deselect_answer(self, answer: Answer) -> Self:
        selected_answers = self.selection_strategy.deselect_answer(
            answer, self.selected_answers
        )
        return ProjectQuestion(
            id=self.id,
            text=self.text,
            type=self.type,
            answers=self.answers,
            created_at=self.created_at,
            selection_strategy=self.selection_strategy,
            selected_answers=selected_answers,
            previous_question_id=self.previous_question_id,
        )

    @field_serializer("selection_strategy", when_used="json")
    def serialize_selection_strategy(self, selection_strategy: SelectionStrategy):
        if isinstance(selection_strategy, SingleSelectionStrategy):
            return {"type": "single"}
        elif isinstance(selection_strategy, MultipleSelectionStrategy):
            return {"type": "multiple"}
        else:
            raise ValueError(
                f"Unsupported selection strategy {self.selection_strategy}"
            )

    @field_validator("selection_strategy", mode="before")
    def deserialize_selection_strategy(cls, value: Any):
        if isinstance(value, SelectionStrategy):
            return value
        elif isinstance(value, dict) and "type" in value:
            strategy_type = value["type"]
            if strategy_type == "single":
                return SingleSelectionStrategy()
            elif strategy_type == "multiple":
                return MultipleSelectionStrategy()
            else:
                raise ValueError(f"Unsupported selection strategy type {strategy_type}")
        else:
            raise ValueError("Invalid selection strategy value")

    @field_serializer("selected_answers", when_used="json")
    def serialize_selected_answers_in_order(self, answer_ids: FrozenSet[Answer]):
        return sorted(answer_ids, key=lambda answer: answer.id.code)

    def __str__(self) -> str:
        return (
            f"ProjectQuestion(id={self.id},\n text={self.text},\n type={self.type},\n answers={self.answers},\n "
            f"created_at={self.created_at}\n, selection_strategy={self.selection_strategy},\n selected_answers={self.selected_answers},\n "
            f"previous_question_id={self.previous_question_id}\n)"
        )

    def __hash__(self):
        return hash(
            (
                self.text,
                self.type,
                self.answers,
                self.created_at,
                self.selected_answers,
                self.selection_strategy,
                self.previous_question_id,
            )
        )
