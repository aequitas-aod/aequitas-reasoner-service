import time
from typing import List, Optional

from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable

from domain.graph.core import QuestionId, Question, AnswerId, Answer
from domain.graph.core.enum import QuestionType
from domain.graph.factories import AnswerFactory, QuestionFactory
from domain.graph.repositories import QuestionRepository
from presentation.presentation import serialize, deserialize
from utils.env import DB_HOST, DB_USER, DB_PASSWORD
from utils.errors import NotFoundError, ConflictError


class GraphQuestionRepository(QuestionRepository):

    def __open_connection(self, max_retries=20, retry_interval=0.5) -> Driver:
        print(f"Connecting to Neo4j at {DB_HOST}")
        driver = GraphDatabase.driver(
            f"neo4j://{DB_HOST}",
            auth=(DB_USER, DB_PASSWORD),
        )
        retries = 0
        while retries < max_retries:
            try:
                # Try to execute a simple query to ensure the server is ready
                with driver.session() as session:
                    session.run("RETURN 1")
                    driver.close()
                break
            except ServiceUnavailable as e:
                retries += 1
                time.sleep(retry_interval)

        if driver:
            return driver
        else:
            raise TimeoutError(
                "Neo4j server did not become available within the specified time."
            )

    def get_all_questions(self) -> List[Question]:
        query = (
            "MATCH (q:Question)-[:HAS_ANSWER]->(a:Answer)"
            "OPTIONAL MATCH (q)-[:PREVIOUS]->(prev:Question)"
            "RETURN q, COLLECT(a) AS answers, prev.id AS previous_question_id"
        )
        driver = self.__open_connection()
        with driver.session() as session:
            res: list[dict] = session.run(query).data()
            questions: list[Question] = []
            for r in res:
                question: Question = self.__convert_node_in_question(
                    r["q"], r["answers"], r["previous_question_id"]
                )
                questions.append(question)
            driver.close()
            return questions

    def get_question_by_id(self, question_id: QuestionId) -> Optional[Question]:
        query = (
            "MATCH (q:Question {id: $question_id})-[:HAS_ANSWER]->(a:Answer)"
            "OPTIONAL MATCH (q)-[:PREVIOUS]->(prev:Question)"
            "RETURN q, COLLECT(a) AS answers, prev.id AS previous_question_id"
        )
        driver = self.__open_connection()
        with driver.session() as session:
            r: list[dict] = session.run(query, question_id=question_id.code).data()
            if len(r) == 0:
                return None
            driver.close()
            question: Question = self.__convert_node_in_question(
                r[0]["q"], r[0]["answers"], r[0]["previous_question_id"]
            )
            return question

    def insert_question(self, question: Question) -> None:
        if self.__check_question_exists(question.id):
            raise ConflictError(f"Question with id {question.id} already exists")
        driver = self.__open_connection()
        with driver.session() as session:
            q: dict = self.__convert_question_in_node(question)
            prev_question_id: Optional[str] = None
            if question.previous_question_id:
                prev_question_id = question.previous_question_id.code
            session.run("CREATE (:Question $question)", question=q).data()

            for answer in question.available_answers:
                a: dict = self.__convert_answer_in_node(answer)
                session.run(
                    "CREATE (:Answer $answer)",
                    answer=a,
                ).data()
                session.run(
                    "MATCH (q:Question {id: $question_id}) MATCH (a:Answer {id: $answer_id}) CREATE (q)-[:HAS_ANSWER]->(a)",
                    question_id=question.id.code,
                    answer_id=answer.id.code,
                ).data()

            if prev_question_id:
                session.run(
                    "MATCH (q1:Question {id: $question_id}) MATCH (q2:Question {id: $prev_question_id}) CREATE (q1)-[:PREVIOUS]->(q2)",
                    question_id=question.id.code,
                    prev_question_id=prev_question_id,
                ).data()

            for answer_id in question.enabled_by:
                session.run(
                    "MATCH (q1:Question {id: $question_id}) MATCH (a:Answer {id: $answer_id}) CREATE (q1)-[:ENABLED_BY]->(a)",
                    question_id=question.id.code,
                    answer_id=answer_id.code,
                ).data()
            driver.close()

    def update_question(self, question_id: QuestionId, question: Question) -> None:
        if not self.__check_question_exists(question_id):
            raise NotFoundError(f"Question with id {question_id} does not exist")
        self.delete_question(question_id)
        self.insert_question(question)

    def delete_question(self, question_id: QuestionId) -> None:
        if not self.__check_question_exists(question_id):
            raise NotFoundError(f"Question with id {question_id} does not exist")
        query = (
            "MATCH (q:Question {id: $question_id})-[:HAS_ANSWER]->(a:Answer)"
            "DETACH DELETE q, a"
        )
        driver = self.__open_connection()
        with driver.session() as session:
            session.run(query, question_id=question_id.code).data()
            driver.close()

    def get_last_inserted_question(self) -> Optional[Question]:
        query = (
            "MATCH (q:Question)-[:HAS_ANSWER]->(a:Answer)"
            "OPTIONAL MATCH (q)-[:PREVIOUS]->(prev:Question)"
            "RETURN q, COLLECT(a) AS answers, prev.id AS previous_question_id"
            " ORDER BY q.created_at DESC LIMIT 1"
        )
        driver = self.__open_connection()
        with driver.session() as session:
            r: list[dict] = session.run(query).data()
            if len(r) == 0:
                return None
            driver.close()
            question: Question = self.__convert_node_in_question(
                r[0]["q"], r[0]["answers"], r[0]["previous_question_id"]
            )
            return question

    def __check_question_exists(self, question_id: QuestionId) -> bool:
        q: Question = self.get_question_by_id(question_id)
        return q is not None

    def __get_enabled_by(self, question_id: QuestionId) -> List[dict]:
        driver = self.__open_connection()
        with driver.session() as session:
            query = (
                "MATCH (q:Question {id: $question_id}) "
                "OPTIONAL MATCH (q)-[:ENABLED_BY]->(a:Answer) "
                "RETURN COLLECT(a.id) AS enabled_by"
            )
            r: list[dict] = session.run(query, question_id=question_id["code"]).data()
            driver.close()
            return [{"code": code} for code in r[0]["enabled_by"]]

    def __convert_question_in_node(self, question: Question) -> dict:
        q: dict = serialize(question)
        q["id"] = question.id.code
        q["created_at"] = question.created_at.isoformat()
        del q["available_answers"]
        del q["previous_question_id"]
        del q["enabled_by"]
        return q

    def __convert_node_in_question(
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
        enabled_by: List[dict] = self.__get_enabled_by(question["id"])
        question["enabled_by"] = enabled_by
        if "action_needed" in question:
            question["action_needed"] = question["action_needed"]
        else:
            question["action_needed"] = None
        return deserialize(question, Question)

    def __convert_answer_in_node(self, answer: Answer) -> dict:
        a: dict = serialize(answer)
        a["id"] = answer.id.code
        return a

    def delete_all_questions(self) -> None:
        driver = self.__open_connection()
        with driver.session() as session:
            session.run("MATCH (n:Question) DETACH DELETE n").data()
            session.run("MATCH (n:Answer) DETACH DELETE n").data()
            driver.close()


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
        enabled_by=frozenset(
            {AnswerId(code="answer-yes"), AnswerId(code="answer-little-bit")}
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
    print(GraphQuestionRepository().get_all_questions())
    GraphQuestionRepository().delete_question(QuestionId(code="test-question"))
    # print(GraphQuestionRepository().get_question_by_id(QuestionId(code="cd-question")))
    # print(GraphQuestionRepository().delete_all_questions())
