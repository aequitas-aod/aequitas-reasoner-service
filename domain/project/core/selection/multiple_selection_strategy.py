from typing_extensions import FrozenSet

from domain.common.core import Answer
from domain.project.core.selection import SelectionStrategy


class MultipleSelectionStrategy(SelectionStrategy):

    def select_answer(
        self, answer: Answer, selected_answers: FrozenSet[Answer]
    ) -> FrozenSet[Answer]:
        """Return a new question with the selected answer added to the selected answers set.
        If the answer is already in the selected answers set, the same question is returned.
        :param answer: the answer to be added to the selected answers set
        :param selected_answers:
        """
        return selected_answers.union({answer})

    def deselect_answer(
        self, answer: Answer, selected_answers: FrozenSet[Answer]
    ) -> FrozenSet[Answer]:
        """Return a new question with the selected answer added to the selected answers set.
        If the answer is already in the selected answers set, the same question is returned.
        :param answer: the answer to be added to the selected answers set
        :param selected_answers:
        """
        return selected_answers.difference({answer})

    def __str__(self):
        return "MultipleSelectionStrategy"
