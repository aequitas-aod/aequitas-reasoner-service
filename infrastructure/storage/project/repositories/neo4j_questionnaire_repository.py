from typing import List, Optional

from domain.graph.core import QuestionId, Answer, AnswerId
from domain.graph.core.enum import QuestionType
from domain.graph.factories import AnswerFactory
from domain.project.core import ProjectId, Project, SelectableQuestion
from domain.project.factories import ProjectFactory, SelectableQuestionFactory
from domain.project.repositories.project_repository import ProjectRepository
from domain.project.repositories.questionnaire_repository import QuestionnaireRepository
from presentation.presentation import deserialize, serialize
from utils.env import DB_HOST, DB_USER, DB_PASSWORD
from utils.errors import NotFoundError, ConflictError
from utils.neo4j_driver import Neo4jDriver, Credentials, Neo4jQuery


class Neo4jQuestionnaireRepository(QuestionnaireRepository):

    def __init__(self):
        self.driver: Neo4jDriver = Neo4jDriver(
            DB_HOST, Credentials(DB_USER, DB_PASSWORD)
        )

    def get_selectable_question_by_id(
        self, question_id: QuestionId
    ) -> Optional[SelectableQuestion]:
        query_string: str = (
            "MATCH (q:SelectableQuestion {id: $question_id})-[:HAS_SELECTED]->(a:Answer)"
            "RETURN q, COLLECT(a) AS selected_answers"
        )
        query: Neo4jQuery = Neo4jQuery(query_string, {"question_id": question_id.code})
        res: List[dict] = self.driver.query(query)
        if len(res) == 0:
            return None
        question: SelectableQuestion = self._convert_node_in_selectable_question(
            res[0]["q"], res[0]["selected_answers"]
        )
        return question

    def insert_selectable_question(self, question: SelectableQuestion) -> QuestionId:
        project_code: str = question.id.code.split("-")[0]
        queries: List[Neo4jQuery] = []
        if len(question.enabled_by) == 0:
            q: dict = self._convert_selectable_question_in_node(question)
            query_string: str = (
                "MATCH (p:Project {id: $project_code}) "
                "CREATE (q:SelectableQuestion $question) "
                "CREATE (p)-[:QUESTIONNAIRE]->(q)"
            )
            query: Neo4jQuery = Neo4jQuery(
                query_string, {"project_code": project_code, "question": q}
            )
            queries.append(query)
        else:
            raise NotImplementedError("Not implemented yet")

        for answer in question.selected_answers:
            a: dict = self._convert_answer_in_node(answer)
            queries.append(Neo4jQuery("CREATE (:Answer $answer)", {"answer": a}))
            queries.append(
                Neo4jQuery(
                    "MATCH (q:SelectableQuestion {id: $question_id}) "
                    "MATCH (a:Answer {id: $answer_id}) "
                    "CREATE (q)-[:HAS_SELECTED]->(a)",
                    {"question_id": question.id.code, "answer_id": answer.id.code},
                )
            )

        self.driver.transaction(queries)
        return question.id

    def update_selectable_question(
        self, question_id: QuestionId, question: SelectableQuestion
    ) -> None:
        # if not self._check_selectable_question_exists(question_id):
        #     raise NotFoundError(f"Question with id {question_id} does not exist")
        self.delete_selectable_question(question_id)
        self.insert_selectable_question(question)

    def delete_selectable_question(self, question_id: QuestionId) -> None:
        # if not self._check_selectable_question_exists(question_id):
        #     raise NotFoundError(f"Question with id {question_id} does not exist")
        self.driver.query(
            Neo4jQuery(
                "MATCH (q:SelectableQuestion {id: $question_id})"
                "OPTIONAL MATCH (q)-[:HAS_SELECTED]->(a:Answer)"
                "OPTIONAL MATCH (prev_q: SelectableQuestion)-[:NEXT]->(q)"
                "OPTIONAL MATCH (p: Project)-[:QUESTIONNAIRE]->(q)"
                "DETACH DELETE q, a",
                {"question_id": question_id.code},
            )
        )

    def get_questionnaire(self) -> List[SelectableQuestion]:
        pass

    def _check_selectable_question_exists(self, question_id: QuestionId) -> bool:
        q: SelectableQuestion = self.get_selectable_question_by_id(question_id)
        return q is not None

    def _convert_selectable_question_in_node(
        self, question: SelectableQuestion
    ) -> dict:
        q: dict = serialize(question)
        q["id"] = question.id.code
        q["created_at"] = question.created_at.isoformat()
        q["available_answers"] = map(lambda a: a.id.code, question.available_answers)
        q["previous_question_id"] = question.previous_question_id.code
        q["selection_strategy"] = question.selection_strategy.__class__.__name__
        del q["selected_answers"]
        return q

    def _convert_answer_in_node(self, answer: Answer) -> dict:
        a: dict = serialize(answer)
        a["id"] = answer.id.code
        return a

    def _convert_node_in_selectable_question(
        self, q: dict, selected_answers: List
    ) -> SelectableQuestion:
        # TODO: Implement this method
        raise NotImplementedError("Not implemented yet")


if __name__ == "__main__":
    questionnaire_repository: QuestionnaireRepository = Neo4jQuestionnaireRepository()
    selectable_question: SelectableQuestion = (
        SelectableQuestionFactory.create_selectable_question(
            QuestionId(code="p1-Q-1"),
            text="What is your favorite color?",
            question_type=QuestionType.SINGLE_CHOICE,
            available_answers=frozenset(
                {
                    AnswerFactory.create_answer(
                        AnswerId(code="p1-Q-1-A-1"), "Red", "red"
                    ),
                    AnswerFactory.create_answer(
                        AnswerId(code="p1-Q-1-A-2"), "Green", "green"
                    ),
                    AnswerFactory.create_answer(
                        AnswerId(code="p1-Q-1-A-3"), "Blue", "blue"
                    ),
                }
            ),
        )
    )
    updated_question: SelectableQuestion = selectable_question.select_answer(
        AnswerFactory.create_answer(AnswerId(code="p1-Q-1-A-1"), "Red", "red")
    )
    # questionnaire_repository.insert_selectable_question(selectable_question)
    # questionnaire_repository.update_selectable_question(
    #     selectable_question.id, updated_question
    # )
    print(updated_question.selection_strategy.__class__.__name__)
    # questionnaire_repository.delete_selectable_question(selectable_question.id)
