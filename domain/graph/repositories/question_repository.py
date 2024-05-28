from abc import ABC, abstractmethod
from typing import List, Optional

from domain.graph.core import QuestionId, Question


class QuestionRepository(ABC):

    @abstractmethod
    def get_all_questions(self) -> List[Question]:
        """Gets all questions
        :return: a list of all questions"""
        pass

    @abstractmethod
    def get_question_by_id(self, question_id: QuestionId) -> Optional[Question]:
        """Gets a question by its id
        :param question_id: the question id
        :return: the question or None if it does not exist"""
        pass

    @abstractmethod
    def insert_question(self, question) -> QuestionId:
        """Inserts a question
        :param question: the question to insert
        :return: the id of the inserted question
        :raises ValueError: if the question already exists"""
        pass

    @abstractmethod
    def update_question(self, question_id: QuestionId, question) -> None:
        """Updates an existing question
        :param question_id: the id of the question to update
        :param question: the updated question
        :raises ValueError: if the question does not exist"""
        pass

    @abstractmethod
    def delete_question(self, question_id: QuestionId) -> None:
        """Deletes a question
        :param question_id: the id of the question to delete
        :raises ValueError: if the question does not exist"""
        pass
