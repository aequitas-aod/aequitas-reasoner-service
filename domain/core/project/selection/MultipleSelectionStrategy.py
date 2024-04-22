from typing_extensions import FrozenSet

from domain.core.commons import Answer
from domain.core.project.selection import SelectionStrategy


class MultipleSelectionStrategy(SelectionStrategy):

    def select_answer(self, answer: Answer, selected_answers: FrozenSet[Answer]) -> FrozenSet[Answer]:
        """Return a new question with the selected answer added to the selected answers set.
                        If the answer is already in the selected answers set, the same question is returned.
                        :param answer: the answer to be added to the selected answers set
                        :param selected_answers:
                        :raises ValueError: if the answer is not in the available answers set
                        """
        return selected_answers.union({answer})

    def deselect_answer(self, answer: Answer, selected_answers: FrozenSet[Answer]) -> FrozenSet[Answer]:
        """Return a new question with the selected answer added to the selected answers set.
                        If the answer is already in the selected answers set, the same question is returned.
                        :param answer: the answer to be added to the selected answers set
                        :param selected_answers:
                        :raises ValueError: if the answer is not in the available answers set
                        """
        return selected_answers.difference({answer})

    def __str__(self):
        return "MultipleSelectionStrategy"
