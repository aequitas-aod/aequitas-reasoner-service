from domain.graph.core import QuestionId, Answer
from domain.project.core import ProjectId, SelectableQuestion
from domain.project.repositories.questionnaire_repository import QuestionnaireRepository


class QuestionnaireService:

    def __init__(self, questionnaire_repository: QuestionnaireRepository):
        self.questionnaire_repository = questionnaire_repository

    def get_nth_question(self, project_id: ProjectId, nth: int) -> SelectableQuestion:
        self.questionnaire_repository

    def insert_answer(
        self, project_id: ProjectId, question_id: QuestionId, answer: Answer
    ) -> None:
        pass

    def reset_questionnaire(self, project_id: ProjectId) -> None:
        pass

    def _get_question_from_graph(self, question_id: QuestionId):
        pass
