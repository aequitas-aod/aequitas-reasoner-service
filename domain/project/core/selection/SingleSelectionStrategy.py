from typing_extensions import FrozenSet

from domain.graph.core import Answer
from domain.project.core.selection import SelectionStrategy


class SingleSelectionStrategy(SelectionStrategy):

    def select_answer(self, answer: Answer, selected_answers: FrozenSet[Answer]) -> FrozenSet[Answer]:
        return frozenset({answer})

    def deselect_answer(self, answer: Answer, selected_answers: FrozenSet[Answer]) -> FrozenSet[Answer]:
        return frozenset()

    def __str__(self):
        return "SingleSelectionStrategy"
