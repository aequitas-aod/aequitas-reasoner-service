from abc import ABC, abstractmethod
from typing import List

from domain.graph.core import ProjectId, QuestionId, Question


class QuestionRepository(ABC):

    @abstractmethod
    def get_all_questions(self, project_id: ProjectId) -> List[Question]:
        pass

    @abstractmethod
    def get_question_by_id(
        self, project_id: ProjectId, question_id: QuestionId
    ) -> Question:
        pass

    @abstractmethod
    def insert_question(self, project_id: ProjectId, question) -> None:
        pass

    @abstractmethod
    def update_question(
        self, project_id: ProjectId, question_id: QuestionId, question
    ) -> None:
        pass

    @abstractmethod
    def delete_question(self, project_id: ProjectId, question_id: QuestionId) -> None:
        pass
