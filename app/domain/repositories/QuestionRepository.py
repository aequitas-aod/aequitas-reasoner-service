from abc import ABC, abstractmethod
from typing import List

from app.domain.core.Question import Question


class QuestionRepository(ABC):

    @abstractmethod
    def get_all_questions(self) -> List[Question]:
        pass

    @abstractmethod
    def get_question_by_id(self, question_id: str) -> Question:
        pass

    @abstractmethod
    def insert_question(self, question) -> bool:
        pass

    @abstractmethod
    def update_question(self, question_id: str, question) -> bool:
        pass

    @abstractmethod
    def delete_question(self, question_id: str) -> bool:
        pass