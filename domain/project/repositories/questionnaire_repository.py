from abc import ABC, abstractmethod
from typing import List, Optional

from domain.graph.core import QuestionId
from domain.project.core import SelectableQuestion


class QuestionnaireRepository(ABC):

    @abstractmethod
    def get_questionnaire(self) -> List[SelectableQuestion]:
        """Gets all questions of the questionnaire
        :return: a list of all questions"""
        pass

    @abstractmethod
    def get_selectable_question_by_id(
        self, question_id: QuestionId
    ) -> Optional[SelectableQuestion]:
        """Gets a question by its id
        :param question_id: the question id
        :return: the question or None if it does not exist"""

    @abstractmethod
    def insert_selectable_question(self, question: SelectableQuestion) -> QuestionId:
        """Inserts a selectable question
        :param question: the question to insert
        :raises ConflictError: if the project already exists"""
        pass

    @abstractmethod
    def update_selectable_question(
        self, question_id: QuestionId, question: SelectableQuestion
    ) -> None:
        """Updates an existing project
        :param question_id: the id of the question to update
        :param question: the updated question
        :raises NotFoundError: if the question does not exist"""

    @abstractmethod
    def delete_selectable_question(self, question_id: QuestionId) -> None:
        """Deletes a question
        :param question_id: the id of the question to delete
        :raises NotFoundError: if the question does not exist"""
        pass
