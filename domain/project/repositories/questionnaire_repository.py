from abc import ABC, abstractmethod

from domain.project.core import ProjectQuestion


class QuestionnaireRepository(ABC):

    @abstractmethod
    def insert_selectable_question(self, question: ProjectQuestion) -> None:
        pass
