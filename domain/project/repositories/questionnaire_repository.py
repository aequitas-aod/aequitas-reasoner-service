from abc import ABC, abstractmethod

from domain.project.core import SelectableQuestion


class QuestionnaireRepository(ABC):

    @abstractmethod
    def insert_selectable_question(self, question: SelectableQuestion) -> None:
        pass
