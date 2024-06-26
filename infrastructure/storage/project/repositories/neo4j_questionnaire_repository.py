from typing import List, Optional

from domain.common.core import QuestionId, Answer, AnswerId
from domain.common.core.enum import QuestionType
from domain.common.factories import AnswerFactory
from domain.project.core import ProjectQuestion, Project, ProjectId
from domain.project.factories import ProjectQuestionFactory
from domain.project.repositories import ProjectRepository
from domain.project.repositories.questionnaire_repository import QuestionnaireRepository
from infrastructure.storage.project.repositories.neo4j_project_repository import (
    Neo4jProjectRepository,
)
from presentation.presentation import serialize, deserialize
from utils.env import DB_HOST, DB_USER, DB_PASSWORD
from utils.neo4j_driver import Neo4jDriver, Credentials, Neo4jQuery


class Neo4jQuestionnaireRepository(QuestionnaireRepository):

    def __init__(self):
        self.driver: Neo4jDriver = Neo4jDriver(
            DB_HOST, Credentials(DB_USER, DB_PASSWORD)
        )
        self.project_repository: ProjectRepository = Neo4jProjectRepository()

    def get_project_question_by_id(
        self, question_id: QuestionId
    ) -> Optional[ProjectQuestion]:
        query_string: str = (
            "MATCH (q:ProjectQuestion {id: $question_id})-[:HAS_SELECTED]->(a:Answer) "
            "OPTIONAL MATCH (prev_q: ProjectQuestion)-[:NEXT]->(q)"
            "RETURN q, COLLECT(a) AS selected_answers, prev_q as previous_question_code"
        )
        query: Neo4jQuery = Neo4jQuery(query_string, {"question_id": question_id.code})
        res: List[dict] = self.driver.query(query)
        if len(res) == 0:
            return None
        question: ProjectQuestion = self._convert_node_in_project_question(
            res[0]["q"], res[0]["selected_answers"], res[0]["previous_question_code"]
        )
        return question

    def insert_project_question(self, question: ProjectQuestion) -> QuestionId:
        project_code: str = question.id.code.split("-")[0]
        project: Optional[Project] = self.project_repository.get_project_by_id(
            ProjectId(code=project_code)
        )
        if project is None:
            raise ValueError(f"Project with id {project_code} does not exist")
        queries: List[Neo4jQuery] = []
        q: dict = self._convert_project_question_in_node(question)
        query_string: str = (
            "MATCH (p:Project {id: $project_code}) "
            "CREATE (q:ProjectQuestion $question) "
        )
        query: Neo4jQuery = Neo4jQuery(
            query_string, {"project_code": project_code, "question": q}
        )
        queries.append(query)
        for answer in question.selected_answers:
            a: dict = self._convert_answer_in_node(answer)
            queries.append(Neo4jQuery("CREATE (:Answer $answer)", {"answer": a}))
            queries.append(
                Neo4jQuery(
                    "MATCH (q:ProjectQuestion {id: $question_id}) "
                    "MATCH (a:Answer {id: $answer_id}) "
                    "CREATE (q)-[:HAS_SELECTED]->(a)",
                    {"question_id": question.id.code, "answer_id": answer.id.code},
                )
            )
        if question.previous_question_id is None:
            query_string: str = (
                "MATCH (p:Project {id: $project_code}) "
                "MATCH (q:ProjectQuestion {id: $question_id}) "
                "CREATE (p)-[:QUESTIONNAIRE]->(q)"
            )
            query: Neo4jQuery = Neo4jQuery(
                query_string,
                {"project_code": project_code, "question_id": question.id.code},
            )
            queries.append(query)
        else:
            previous_question: Optional[ProjectQuestion] = (
                self.get_project_question_by_id(question.previous_question_id)
            )
            if previous_question is None:
                raise ValueError(
                    f"Previous question with id {question.previous_question_id} does not exist"
                )
            query_string: str = (
                "MATCH (q:ProjectQuestion {id: $question_id}) "
                "MATCH (prev_q: ProjectQuestion {id: $prev_question_id}) "
                "CREATE (prev_q)-[:NEXT]->(q)"
            )
            query: Neo4jQuery = Neo4jQuery(
                query_string,
                {
                    "question_id": question.id.code,
                    "prev_question_id": question.previous_question_id.code,
                },
            )
            queries.append(query)

        self.driver.transaction(queries)
        return question.id

    def update_project_question(
        self, question_id: QuestionId, question: ProjectQuestion
    ) -> None:
        # if not self._check_project_question_exists(question_id):
        #     raise NotFoundError(f"Question with id {question_id} does not exist")
        self.delete_project_question(question_id)
        self.insert_project_question(question)

    def delete_project_question(self, question_id: QuestionId) -> None:
        # if not self._check_project_question_exists(question_id):
        #     raise NotFoundError(f"Question with id {question_id} does not exist")
        self.driver.query(
            Neo4jQuery(
                "MATCH (q:ProjectQuestion {id: $question_id})"
                "OPTIONAL MATCH (q)-[:HAS_SELECTED]->(a:Answer)"
                "OPTIONAL MATCH (prev_q: ProjectQuestion)-[:NEXT]->(q)"
                "OPTIONAL MATCH (p: Project)-[:QUESTIONNAIRE]->(q)"
                "DETACH DELETE q, a",
                {"question_id": question_id.code},
            )
        )

    def get_questionnaire(self) -> List[ProjectQuestion]:
        pass

    def _check_project_question_exists(self, question_id: QuestionId) -> bool:
        q: ProjectQuestion = self.get_project_question_by_id(question_id)
        return q is not None

    def _convert_project_question_in_node(self, question: ProjectQuestion) -> dict:
        q: dict = serialize(question)
        q["id"] = question.id.code
        q["created_at"] = question.created_at.isoformat()
        q["available_answers"] = list(
            map(lambda a: a.id.code, question.available_answers)
        )
        q["selection_strategy"] = question.selection_strategy.__class__.__name__
        del q["selected_answers"]
        del q["previous_question_id"]
        return q

    def _convert_answer_in_node(self, answer: Answer) -> dict:
        a: dict = serialize(answer)
        a["id"] = answer.id.code
        return a

    def _convert_node_in_project_question(
        self, q: dict, selected_answers: List, previous_question_code: Optional[str]
    ) -> ProjectQuestion:
        question: dict = q
        question["id"] = {"code": q["id"]}
        question["available_answers"] = [
            {"id": {"code": answer_id}} for answer_id in question["available_answers"]
        ]
        question["selection_strategy"] = {"type": q["selection_strategy"]}
        question["selected_answers"] = [
            {"id": {"code": a["id"]}, "text": a["text"]} for a in selected_answers
        ]
        question["previous_question_id"] = {"code": previous_question_code} if previous_question_code else None
        return deserialize(question, ProjectQuestion)


if __name__ == "__main__":
    questionnaire_repository: QuestionnaireRepository = Neo4jQuestionnaireRepository()
    project_question: ProjectQuestion = ProjectQuestionFactory.create_project_question(
        QuestionId(code="p1-Q-1"),
        text="What is your favorite color?",
        question_type=QuestionType.SINGLE_CHOICE,
        available_answers=frozenset(
            {
                AnswerFactory.create_answer(AnswerId(code="p1-Q-1-A-1"), "Red"),
                AnswerFactory.create_answer(AnswerId(code="p1-Q-1-A-2"), "Green"),
                AnswerFactory.create_answer(AnswerId(code="p1-Q-1-A-3"), "Blue"),
            }
        ),
    )
    updated_question: ProjectQuestion = project_question.select_answer(
        AnswerFactory.create_answer(AnswerId(code="p1-Q-1-A-1"), "Red")
    )
    project_question2: ProjectQuestion = ProjectQuestionFactory.create_project_question(
        QuestionId(code="p1-Q-2"),
        text="What is your favorite animal?",
        question_type=QuestionType.SINGLE_CHOICE,
        available_answers=frozenset(
            {
                AnswerFactory.create_answer(AnswerId(code="p1-Q-2-A-1"), "Dog"),
                AnswerFactory.create_answer(AnswerId(code="p1-Q-2-A-2"), "Cat"),
                AnswerFactory.create_answer(AnswerId(code="p1-Q-2-A-3"), "Bird"),
            }
        ),
        previous_question_id=QuestionId(code="p1-Q-1"),
    )
    updated_question2: ProjectQuestion = project_question2.select_answer(
        AnswerFactory.create_answer(AnswerId(code="p1-Q-2-A-1"), "Dog")
    )

    questionnaire_repository.insert_project_question(project_question)
    questionnaire_repository.update_project_question(
        project_question.id, updated_question
    )
    questionnaire_repository.insert_project_question(project_question2)
    questionnaire_repository.update_project_question(
        project_question2.id, updated_question2
    )
    # print(updated_question.selection_strategy.__class__.__name__)
    # questionnaire_repository.delete_project_question(project_question.id)
