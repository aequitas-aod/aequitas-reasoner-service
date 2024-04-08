from typing import List

from app.domain.core.Question import Question
from app.domain.repositories.QuestionRepository import QuestionRepository


class GraphQuestionRepository(QuestionRepository):

    def __init__(self):
        pass

    def get_all_questions(self) -> List[Question]:
        pass

    def get_question_by_id(self, id: str) -> Question:
        pass

    def insert_question(self, question) -> bool:
        pass

    def update_question(self, id: str, question) -> bool:
        pass

    def delete_question(self, id: str) -> bool:
        pass
