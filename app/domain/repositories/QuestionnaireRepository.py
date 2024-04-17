from abc import ABC, abstractmethod
from typing import List

from app.domain.core import ProjectId, Question, QuestionId


class QuestionnaireRepository(ABC):

    def __init__(self, project_id: ProjectId):
        self.project_id = project_id

    @abstractmethod
    def get_questionnaire(self) -> List[Question]:
        pass

    @abstractmethod
    def insert_question(self, question: Question) -> bool:
        pass

    @abstractmethod
    def update_question(self, question_id: QuestionId, question: Question) -> bool:
        pass

    @abstractmethod
    def delete_question(self, question_id: QuestionId) -> Question:
        pass

