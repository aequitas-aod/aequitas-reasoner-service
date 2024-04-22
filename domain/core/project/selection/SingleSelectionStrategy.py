from typing_extensions import FrozenSet

from domain.core.commons import Answer
from domain.core.project.selection import SelectionStrategy


class SingleSelectionStrategy(SelectionStrategy):

    def select_answer(self, answer: Answer, selected_answers: FrozenSet[Answer]) -> FrozenSet[Answer]:
        return frozenset({answer})

    def deselect_answer(self, answer: Answer, selected_answers: FrozenSet[Answer]) -> FrozenSet[Answer]:
        return frozenset()

    def __str__(self):
        return "SingleSelectionStrategy"
