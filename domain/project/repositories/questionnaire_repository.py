from abc import ABC, abstractmethod
from typing import List, Optional

from domain.common.core import QuestionId
from domain.project.core import ProjectQuestion


class QuestionnaireRepository(ABC):

    @abstractmethod
    def get_questionnaire(self) -> List[ProjectQuestion]:
        """Gets all questions of the questionnaire
        :return: a list of all questions"""
        pass

    @abstractmethod
    def get_project_question_by_id(
        self, question_id: QuestionId
    ) -> Optional[ProjectQuestion]:
        """Gets a question by its id
        :param question_id: the question id
        :return: the question or None if it does not exist"""

    @abstractmethod
    def insert_project_question(self, question: ProjectQuestion) -> QuestionId:
        """Inserts a project question
        :param question: the question to insert
        :raises ConflictError: if the project already exists
        :raises ValueError: if the project does not exist"""
        pass

    @abstractmethod
    def update_project_question(
        self, question_id: QuestionId, question: ProjectQuestion
    ) -> None:
        """Updates an existing project
        :param question_id: the id of the question to update
        :param question: the updated question
        :raises NotFoundError: if the question does not exist"""

    @abstractmethod
    def delete_project_question(self, question_id: QuestionId) -> None:
        """Deletes a question
        :param question_id: the id of the question to delete
        :raises NotFoundError: if the question does not exist"""
        pass
