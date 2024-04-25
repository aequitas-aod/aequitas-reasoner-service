from domain.graph.core import QuestionId, Answer
from domain.graph.repositories import QuestionRepository
from domain.project.core import ProjectId, SelectableQuestion


class QuestionnaireService:

    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def get_first_question(self, project_id: ProjectId):
        pass

    def insert_answer(
        self, project_id: ProjectId, question_id: QuestionId, answer: Answer
    ):
        pass

    def get_next_question(self, project_id: ProjectId, question: SelectableQuestion):
        pass

    def go_back_to_question(self, project_id: ProjectId, question: QuestionId):
        pass

    def reset_questionnaire(self, project_id: ProjectId):
        pass
