from typing import List, Optional

from domain.graph.core import QuestionId, Question, AnswerId, Answer
from domain.graph.core.enum import QuestionType
from domain.graph.factories import AnswerFactory, QuestionFactory
from domain.graph.repositories import QuestionRepository
from presentation.presentation import serialize, deserialize
from utils.env import DB_HOST, DB_USER, DB_PASSWORD
from utils.errors import NotFoundError, ConflictError
from utils.neo4j_driver import Neo4jDriver, Credentials, Neo4jQuery


class GraphQuestionRepository(QuestionRepository):

    def __init__(self):
        self.driver: Neo4jDriver = Neo4jDriver(
            DB_HOST, Credentials(DB_USER, DB_PASSWORD)
        )

    def get_all_questions(self) -> List[Question]:
        query_string = (
            "MATCH (q:Question)-[:HAS_ANSWER]->(a:Answer)"
            "OPTIONAL MATCH (q)-[:PREVIOUS]->(prev:Question)"
            "RETURN q, COLLECT(a) AS answers, prev.id AS previous_question_id"
        )
        query: Neo4jQuery = Neo4jQuery(query_string, {})
        res: List[dict] = self.driver.query(query)
        questions: List[Question] = []
        for r in res:
            question: Question = self._convert_node_in_question(
                r["q"], r["answers"], r["previous_question_id"]
            )
            questions.append(question)
        return questions

    def get_question_by_id(self, question_id: QuestionId) -> Optional[Question]:
        query_string = (
            "MATCH (q:Question {id: $question_id})-[:HAS_ANSWER]->(a:Answer)"
            "OPTIONAL MATCH (q)-[:PREVIOUS]->(prev:Question)"
            "RETURN q, COLLECT(a) AS answers, prev.id AS previous_question_id"
        )
        query: Neo4jQuery = Neo4jQuery(query_string, {"question_id": question_id.code})
        r: List[dict] = self.driver.query(query)
        if len(r) == 0:
            return None
        question: Question = self._convert_node_in_question(
            r[0]["q"], r[0]["answers"], r[0]["previous_question_id"]
        )
        return question

    def insert_question(self, question: Question) -> None:
        if self._check_question_exists(question.id):
            raise ConflictError(f"Question with id {question.id} already exists")

        q: dict = self._convert_question_in_node(question)
        prev_question_id: Optional[str] = None
        if question.previous_question_id:
            prev_question_id = question.previous_question_id.code

        queries: List[Neo4jQuery] = [
            Neo4jQuery(
                "CREATE (:Question $question)",
                {"question": q},
            )
        ]
        for answer in question.available_answers:
            a: dict = self._convert_answer_in_node(answer)
            queries.append(Neo4jQuery("CREATE (:Answer $answer)", {"answer": a}))
            queries.append(
                Neo4jQuery(
                    "MATCH (q:Question {id: $question_id}) MATCH (a:Answer {id: $answer_id}) CREATE (q)-[:HAS_ANSWER]->(a)",
                    {"question_id": question.id.code, "answer_id": answer.id.code},
                )
            )
        if prev_question_id:
            queries.append(
                Neo4jQuery(
                    "MATCH (q1:Question {id: $question_id}) MATCH (q2:Question {id: $prev_question_id}) CREATE (q1)-[:PREVIOUS]->(q2)",
                    {
                        "question_id": question.id.code,
                        "prev_question_id": prev_question_id,
                    },
                )
            )
        for answer_id in question.enabled_by:
            queries.append(
                Neo4jQuery(
                    "MATCH (q1:Question {id: $question_id}) MATCH (a:Answer {id: $answer_id}) CREATE (q1)-[:ENABLED_BY]->(a)",
                    {"question_id": question.id.code, "answer_id": answer_id.code},
                )
            )

        self.driver.transaction(queries)

    def update_question(self, question_id: QuestionId, question: Question) -> None:
        if not self._check_question_exists(question_id):
            raise NotFoundError(f"Question with id {question_id} does not exist")
        self.delete_question(question_id)
        self.insert_question(question)

    def delete_question(self, question_id: QuestionId) -> None:
        if not self._check_question_exists(question_id):
            raise NotFoundError(f"Question with id {question_id} does not exist")
        query = (
            "MATCH (q:Question {id: $question_id})-[:HAS_ANSWER]->(a:Answer)"
            "DETACH DELETE q, a"
        )
        self.driver.query(Neo4jQuery(query, {"question_id": question_id.code}))

    def get_last_inserted_question(self) -> Optional[Question]:
        query_string = (
            "MATCH (q:Question)-[:HAS_ANSWER]->(a:Answer)"
            "OPTIONAL MATCH (q)-[:PREVIOUS]->(prev:Question)"
            "RETURN q, COLLECT(a) AS answers, prev.id AS previous_question_id"
            " ORDER BY q.created_at DESC LIMIT 1"
        )
        query: Neo4jQuery = Neo4jQuery(query_string, {})
        r: List[dict] = self.driver.query(query)
        if len(r) == 0:
            return None
        question: Question = self._convert_node_in_question(
            r[0]["q"], r[0]["answers"], r[0]["previous_question_id"]
        )
        return question

    def _check_question_exists(self, question_id: QuestionId) -> bool:
        q: Question = self.get_question_by_id(question_id)
        return q is not None

    def _get_enabled_by(self, question_id: QuestionId) -> List[dict]:
        query_string = (
            "MATCH (q:Question {id: $question_id}) "
            "OPTIONAL MATCH (q)-[:ENABLED_BY]->(a:Answer) "
            "RETURN COLLECT(a.id) AS enabled_by"
        )
        query: Neo4jQuery = Neo4jQuery(query_string, {"question_id": question_id.code})
        r: List[dict] = self.driver.query(query)
        return [{"code": code} for code in r[0]["enabled_by"]]

    def _convert_question_in_node(self, question: Question) -> dict:
        q: dict = serialize(question)
        q["id"] = question.id.code
        q["created_at"] = question.created_at.isoformat()
        del q["available_answers"]
        del q["previous_question_id"]
        del q["enabled_by"]
        return q

    def _convert_node_in_question(
        self, q: dict, answers: List, previous_question_id: QuestionId
    ) -> Question:
        question: dict = q
        question["id"] = {"code": question["id"]}
        question["created_at"] = question["created_at"]
        question["available_answers"] = [
            {"id": {"code": a["id"]}, "text": a["text"], "value": a["value"]}
            for a in answers
        ]
        question["previous_question_id"] = (
            {"code": previous_question_id} if previous_question_id else None
        )
        enabled_by: List[dict] = self._get_enabled_by(
            QuestionId(code=question["id"]["code"])
        )
        question["enabled_by"] = enabled_by
        if "action_needed" in question:
            question["action_needed"] = question["action_needed"]
        else:
            question["action_needed"] = None
        return deserialize(question, Question)

    def _convert_answer_in_node(self, answer: Answer) -> dict:
        a: dict = serialize(answer)
        a["id"] = answer.id.code
        return a

    def delete_all_questions(self) -> None:
        self.driver.transaction(
            [
                Neo4jQuery("MATCH (n:Question) DETACH DELETE n", {}),
                Neo4jQuery("MATCH (n:Answer) DETACH DELETE n", {}),
            ]
        )


if __name__ == "__main__":
    GraphQuestionRepository().delete_all_questions()
    q1: Question = QuestionFactory().create_question(
        QuestionId(code="test-question"),
        "Test question",
        QuestionType.SINGLE_CHOICE,
        frozenset(
            {
                AnswerFactory().create_answer(
                    AnswerId(code="answer-yes"), "Yes", "yes"
                ),
                AnswerFactory().create_answer(
                    AnswerId(code="answer-little-bit"), "A little bit", "little-bit"
                ),
                AnswerFactory().create_answer(AnswerId(code="answer-no"), "No", "no"),
            }
        ),
    )
    GraphQuestionRepository().insert_question(q1)
    # q2: Question = QuestionFactory().create_question(
    #     QuestionId(code="cd-question"),
    #     "Do you use CD?",
    #     QuestionType.SINGLE_CHOICE,
    #     frozenset(
    #         {
    #             AnswerFactory().create_answer(AnswerId(code="yes"), "Yes", "yes"),
    #             AnswerFactory().create_answer(
    #                 AnswerId(code="little-bit"), "A little bit", "little-bit"
    #             ),
    #             AnswerFactory().create_answer(AnswerId(code="no"), "No", "no"),
    #         }
    #     ),
    #     previous_question_id=QuestionId(code="ci-question"),
    #     enabled_by=frozenset(
    #         {AnswerId(code="answer-yes"), AnswerId(code="answer-little-bit")}
    #     ),
    #     action_needed=Action.METRICS_CHECK,
    # )
    # GraphQuestionRepository().insert_question(q2)
    # print(GraphQuestionRepository().get_all_questions())
    # GraphQuestionRepository().delete_question(QuestionId(code="test-question"))
    # print(GraphQuestionRepository().get_question_by_id(QuestionId(code="cd-question")))
    # print(GraphQuestionRepository().delete_all_questions())
