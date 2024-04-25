from abc import ABC, abstractmethod
from typing import List, Optional

from domain.graph.core import QuestionId, Question


class QuestionRepository(ABC):

    @abstractmethod
    def get_all_questions(self) -> List[Question]:
        pass

    @abstractmethod
    def get_question_by_id(self, question_id: QuestionId) -> Optional[Question]:
        pass

    @abstractmethod
    def insert_question(self, question) -> None:
        pass

    @abstractmethod
    def update_question(self, question_id: QuestionId, question) -> None:
        pass

    @abstractmethod
    def delete_question(self, question_id: QuestionId) -> None:
        pass
