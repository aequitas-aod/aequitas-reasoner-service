from domain.common.core import QuestionId, Answer
from domain.graph.repositories import GraphQuestionRepository
from domain.project.core import ProjectId, ProjectQuestion


class QuestionnaireService:

    def __init__(self, question_repository: GraphQuestionRepository):
        self.question_repository = question_repository

    def get_nth_question(self, project_id: ProjectId, nth: int) -> ProjectQuestion:
        # self.question_repository
        pass

    def insert_answer(
        self, project_id: ProjectId, question_id: QuestionId, answer: Answer
    ) -> None:
        pass

    def reset_questionnaire(self, project_id: ProjectId) -> None:
        pass

    def _get_question_from_graph(self, question_id: QuestionId):
        pass
