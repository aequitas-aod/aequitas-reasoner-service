from typing import FrozenSet

from pydantic import field_serializer
from typing_extensions import Self

from domain.common.core import Question
from domain.common.core import Answer
from domain.project.core.selection import SelectionStrategy


class ProjectQuestion(Question):
    selection_strategy: SelectionStrategy
    selected_answers: FrozenSet[Answer] = frozenset()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def select_answer(self, answer: Answer) -> Self:
        if answer not in self.available_answers:
            raise ValueError(f"Answer {answer} is not available for this question")
        selected_answers = self.selection_strategy.select_answer(
            answer, self.selected_answers
        )
        return ProjectQuestion(
            id=self.id,
            text=self.text,
            type=self.type,
            available_answers=self.available_answers,
            created_at=self.created_at,
            selection_strategy=self.selection_strategy,
            selected_answers=selected_answers,
        )

    def deselect_answer(self, answer: Answer) -> Self:
        selected_answers = self.selection_strategy.deselect_answer(
            answer, self.selected_answers
        )
        return ProjectQuestion(
            id=self.id,
            text=self.text,
            type=self.type,
            available_answers=self.available_answers,
            created_at=self.created_at,
            selection_strategy=self.selection_strategy,
            selected_answers=selected_answers,
        )

    @field_serializer("selected_answers", when_used="json")
    def serialize_available_answers_in_order(self, answer_ids: FrozenSet[Answer]):
        return sorted(answer_ids, key=lambda answer: answer.text)

    def __str__(self) -> str:
        return (
            f"SelectableQuestion(id={self.id}, text={self.text}, type={self.type}, \n"
            f"selection_strategy={self.selection_strategy}, selected_answers={self.selected_answers})"
        )

    def __hash__(self):
        return hash(
            (
                self.text,
                self.type,
                self.available_answers,
                self.created_at,
                self.selected_answers,
            )
        )
