from typing import Optional, List

from domain.graph.core import Question, QuestionId
from domain.graph.repositories import QuestionRepository


class QuestionService:

    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def get_all_questions(self) -> List[Question]:
        """
        Gets all questions
        :return: a list of all questions
        """
        return self.question_repository.get_all_questions()

    def get_question_by_id(self, question_id: QuestionId) -> Optional[Question]:
        """
        Gets a question by its id
        :param question_id: the question id
        :return: the question or None if it does not exist
        """
        return self.question_repository.get_question_by_id(question_id)

    def add_question(self, question: Question) -> QuestionId:
        """
        Inserts a question
        :param question: the question to insert
        :return: the id of the inserted question
        :raises ValueError: if the question already exists
        """
        return self.question_repository.insert_question(question)

    def update_question(self, question_id: QuestionId, question: Question) -> None:
        """
        Updates an existing question
        :param question_id: the id of the question to update
        :param question: the updated question
        :raises ValueError: if the question does not exist or if the question id does not match the existing question id
        """
        if question_id != question.id:
            raise ValueError("Question id does not match")
        self.question_repository.update_question(question_id, question)

    def delete_question(self, question_id: QuestionId) -> None:
        """
        Deletes a question
        :param question_id: the id of the question to delete
        :raises ValueError: if the question does not exist
        """
        self.question_repository.delete_question(question_id)

    def get_new_candidate_id(self) -> str:
        """
        Gets a new candidate id for a question
        :return: the new candidate id
        """
        return f"q-{len(self.get_all_questions()) + 1}"
