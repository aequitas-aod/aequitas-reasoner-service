import os
from typing import List

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
            "MATCH (q:Question)-[:HAS_ANSWER]->(a:Answer) RETURN q, COLLECT(a) AS answers"
        )
        with self._driver.session() as session:
            res: list[dict] = session.run(query).data()
            questions: List[Question] = []
            for question in res:
                q: dict = question["q"]
                q["id"] = {"code": q["id"]}
                q["available_answers"] = [a for a in question["answers"]]
                questions.append(deserialize(q, Question))
            return questions

    def get_question_by_id(self, question_id: QuestionId) -> Question:
        query: LiteralString = (
            "MATCH (q:Question {id: $question_id})-[:HAS_ANSWER]->(a:Answer) RETURN q, COLLECT(a) AS answers"
        )
        with self._driver.session() as session:
            res: list[dict] = session.run(query, question_id=question_id.code).data()
            question: dict = res[0]["q"]
            question["id"] = {"code": question["id"]}
            question["available_answers"] = [a for a in res[0]["answers"]]
            return deserialize(question, Question)

    def insert_question(self, question: Question) -> None:
        with self._driver.session() as session:
            q: dict = self.__convert_question_in_node(question)
            prev_question_id: str = (
                question.previous_question_id.code
                if question.previous_question_id
                else None
            )
            print(q)
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

    def update_question(self, question_id: str, question) -> None:
        pass

    def delete_question(self, question_id: str) -> None:
        pass

    def __convert_question_in_node(self, question: Question) -> dict:
        q: dict = serialize(question)
        q["id"] = question.id.code
        del q["previous_question_id"]
        del q["available_answers"]
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
    GraphQuestionRepository().delete_all_questions()

    # print(
    #     GraphQuestionRepository().get_question_by_id(QuestionId(code="ci-question"))
    # )
    GraphQuestionRepository().insert_question(
        QuestionFactory().create_question(
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
                    AnswerFactory().create_answer(
                        AnswerId(code="answer-no"), "No", "no"
                    ),
                }
            ),
            None,
            action_needed=Action.METRICS_CHECK,
        ),
    )

    GraphQuestionRepository().insert_question(
        QuestionFactory().create_question(
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
            QuestionId(code="ci-question"),
            action_needed=Action.METRICS_CHECK,
        ),
    )
