import os
from typing import List, Optional

from dotenv import load_dotenv
from neo4j import GraphDatabase
from typing_extensions import LiteralString

from domain.graph.core import QuestionId, Question, AnswerId, Answer
from domain.graph.core.enum import QuestionType, Action
from domain.graph.factories import AnswerFactory, QuestionFactory
from domain.graph.repositories import QuestionRepository
from presentation.presentation import serialize, deserialize

load_dotenv()


class GraphQuestionRepository(QuestionRepository):

    def __init__(self):
        self._driver = GraphDatabase.driver(
            f"neo4j://{os.environ.get('DB_HOST')}",
            auth=(os.environ.get("DB_USER"), os.environ.get("DB_PASSWORD")),
        )
        self._driver.verify_connectivity()

    def get_all_questions(self) -> List[Question]:
        query: LiteralString = (
            "MATCH (q:Question)-[:HAS_ANSWER]->(a:Answer)"
            "OPTIONAL MATCH (q)-[:PREVIOUS]->(prev:Question)"
            "RETURN q, COLLECT(a) AS answers, prev.id AS previous_question_id"
        )
        with self._driver.session() as session:
            res: list[dict] = session.run(query).data()
            print("RES", res)
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
                query: LiteralString = (
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
        with self._driver.session() as session:
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
            print(res)
            question["enabled_by"] = [{"code": a} for a in res[0]["enabled_by"]]
            print(question)
            return deserialize(question, Question)

    def insert_question(self, question: Question) -> None:
        res: Optional[Question] = self.get_question_by_id(question.id)
        if res:
            raise ValueError(f"Question with id {question.id} already exists")
        with self._driver.session() as session:
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

    def update_question(self, question_id: str, question) -> None:
        pass

    def delete_question(self, question_id: str) -> None:
        query = (
            "MATCH (q:Question {id: $question_id})-[:HAS_ANSWER]->(a:Answer)"
            "DETACH DELETE q, a"
        )
        with self._driver.session() as session:
            session.run(query, question_id=question_id).data()

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
        with self._driver.session() as session:
            session.run("MATCH (n:Question) DETACH DELETE n").data()
            session.run("MATCH (n:Answer) DETACH DELETE n").data()


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
    GraphQuestionRepository().delete_question("ci-question")
    print(GraphQuestionRepository().get_question_by_id(QuestionId(code="cd-question")))
    # print(GraphQuestionRepository().get_all_questions())
