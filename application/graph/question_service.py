from typing import Optional, List

from domain.graph.core import Question, QuestionId
from domain.graph.repositories import QuestionRepository


class QuestionService:

    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def get_all_questions(self) -> List[Question]:
        return self.question_repository.get_all_questions()

    def get_question_by_id(self, question_id: QuestionId) -> Optional[Question]:
        return self.question_repository.get_question_by_id(question_id)

    def add_question(self, question: Question) -> None:
        self.question_repository.insert_question(question)

    def update_question(self, question_id: QuestionId, question: Question) -> None:
        self.question_repository.update_question(question_id, question)

    def delete_question(self, question_id: QuestionId) -> None:
        self.question_repository.delete_question(question_id)
