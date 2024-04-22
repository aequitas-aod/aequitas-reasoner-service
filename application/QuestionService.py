from domain.core import ProjectId, Question
from domain.graph.repositories import QuestionRepository


class QuestionService:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def get_next_question(self, project_id: ProjectId, question: Question):
        pass

    def go_back_to_question(self, project_id: ProjectId, question: Question):
        pass

    def reset_questionnaire(self, project_id: ProjectId):
        pass
