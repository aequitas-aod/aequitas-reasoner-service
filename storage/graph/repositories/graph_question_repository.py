import time
from typing import List, Optional

from domain.graph.core import QuestionId, Question, AnswerId, Answer
from domain.graph.core.enum import QuestionType, Action
from domain.graph.factories import AnswerFactory, QuestionFactory
from domain.graph.repositories import QuestionRepository
from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable
from presentation.presentation import serialize, deserialize
from utils.env import DB_HOST, DB_USER, DB_PASSWORD


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
                question: dict = r["q"]
                question["id"] = {"code": question["id"]}
                question["available_answers"] = [
                    {"id": {"code": a["id"]}, "text": a["text"], "value": a["value"]}
                    for a in r["answers"]
                ]
                question["previous_question_id"] = (
                    {"code": r["previous_question_id"]}
                    if r["previous_question_id"]
                    else None
                )
                query = (
                    "MATCH (q:Question {id: $question_id})"
                    "OPTIONAL MATCH (q)-[:ENABLED_BY]->(a:Answer)"
                    "RETURN COLLECT(a.id) AS enabled_by"
                )
                res: list[dict] = session.run(
                    query, question_id=question["id"]["code"]
                ).data()
                question["enabled_by"] = [{"code": a} for a in res[0]["enabled_by"]]
                questions.append(deserialize(question, Question))

            return questions

    def get_question_by_id(self, question_id: QuestionId) -> Optional[Question]:
        query = (
            "MATCH (q:Question {id: $question_id})-[:HAS_ANSWER]->(a:Answer)"
            "OPTIONAL MATCH (q)-[:PREVIOUS]->(prev:Question)"
            "RETURN q, COLLECT(a) AS answers, prev.id AS previous_question_id"
        )
        driver = self.__open_connection()
        with driver.session() as session:
            res: list[dict] = session.run(query, question_id=question_id.code).data()
            if len(res) == 0:
                return None
            question: dict = res[0]["q"]
            question["id"] = {"code": question["id"]}
            question["available_answers"] = [
                {"id": {"code": a["id"]}, "text": a["text"], "value": a["value"]}
                for a in res[0]["answers"]
            ]
            question["previous_question_id"] = (
                {"code": res[0]["previous_question_id"]}
                if res[0]["previous_question_id"]
                else None
            )
            query = (
                "MATCH (q:Question {id: $question_id}) "
                "OPTIONAL MATCH (q)-[:ENABLED_BY]->(a:Answer) "
                "RETURN COLLECT(a.id) AS enabled_by"
            )
            res: list[dict] = session.run(query, question_id=question_id.code).data()
            question["enabled_by"] = [{"code": a} for a in res[0]["enabled_by"]]
            driver.close()
            return deserialize(question, Question)

    def insert_question(self, question: Question) -> None:
        res: Optional[Question] = self.get_question_by_id(question.id)
        if res:
            raise ValueError(f"Question with id {question.id} already exists")
        driver = self.__open_connection()
        with driver.session() as session:
            q: dict = self.__convert_question_in_node(question)
            prev_question_id: str = (
                question.previous_question_id.code
                if question.previous_question_id
                else None
            )
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
        q: Question = self.get_question_by_id(question_id)
        if not q:
            raise ValueError(f"Question with id {question_id} does not exist")
        self.delete_question(question_id)
        self.insert_question(question)

    def delete_question(self, question_id: QuestionId) -> None:
        query = (
            "MATCH (q:Question {id: $question_id})-[:HAS_ANSWER]->(a:Answer)"
            "DETACH DELETE q, a"
        )
        driver = self.__open_connection()
        with driver.session() as session:
            session.run(query, question_id=question_id.code).data()
            driver.close()

    def __convert_question_in_node(self, question: Question) -> dict:
        q: dict = serialize(question)
        q["id"] = question.id.code
        del q["available_answers"]
        del q["previous_question_id"]
        del q["enabled_by"]
        return q

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
    q1: Question = QuestionFactory().create_question(
        QuestionId(code="ci-question"),
        "Do you use CI?",
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
        None,
        action_needed=Action.METRICS_CHECK,
    )
    GraphQuestionRepository().delete_all_questions()
    GraphQuestionRepository().insert_question(q1)
    q2: Question = QuestionFactory().create_question(
        QuestionId(code="cd-question"),
        "Do you use CD?",
        QuestionType.SINGLE_CHOICE,
        frozenset(
            {
                AnswerFactory().create_answer(AnswerId(code="yes"), "Yes", "yes"),
                AnswerFactory().create_answer(
                    AnswerId(code="little-bit"), "A little bit", "little-bit"
                ),
                AnswerFactory().create_answer(AnswerId(code="no"), "No", "no"),
            }
        ),
        previous_question_id=QuestionId(code="ci-question"),
        enabled_by=frozenset(
            {AnswerId(code="answer-yes"), AnswerId(code="answer-little-bit")}
        ),
        action_needed=Action.METRICS_CHECK,
    )
    GraphQuestionRepository().insert_question(q2)
    # GraphQuestionRepository().delete_question("ci-question")
    print(GraphQuestionRepository().get_question_by_id(QuestionId(code="cd-question")))
    # print(GraphQuestionRepository().delete_all_questions())
