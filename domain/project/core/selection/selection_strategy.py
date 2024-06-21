from abc import ABC, abstractmethod

from pydantic import BaseModel
from typing_extensions import FrozenSet

from domain.common.core import Answer


class SelectionStrategy(ABC, BaseModel):

    @abstractmethod
    def select_answer(
        self, answer: Answer, selected_answers: FrozenSet[Answer]
    ) -> FrozenSet[Answer]:
        pass

    @abstractmethod
    def deselect_answer(
        self, answer: Answer, selected_answers: FrozenSet[Answer]
    ) -> FrozenSet[Answer]:
        pass
