import os
from typing import List
from typing_extensions import LiteralString

from dotenv import load_dotenv
from neo4j import GraphDatabase

from app.domain.core import ProjectId, QuestionId
from app.domain.core.Question import Question
from app.domain.core.enum import QuestionType, Action
from app.domain.factories import QuestionFactory, AnswerFactory
from app.domain.repositories.QuestionRepository import QuestionRepository
from app.presentation.presentation import serialize

load_dotenv()


class GraphQuestionRepository(QuestionRepository):

    def __init__(self):
        self._driver = GraphDatabase.driver(
            f"neo4j://{os.environ.get('DB_HOST')}",
            auth=(os.environ.get("DB_USER"), os.environ.get("DB_PASSWORD")),
        )
        self._driver.verify_connectivity()

    def get_all_questions(self, project_id: ProjectId):
        query: LiteralString = "MATCH (question:Question) RETURN question"
        with self._driver.session() as session:
            return session.run(query).data()

    def get_question_by_id(
        self, project_id: ProjectId, question_id: QuestionId
    ) -> Question:
        query: LiteralString = "MATCH (q:Question {{id: $question_id}}) RETURN q"
        with self._driver.session() as session:
            return session.run(query, question_id=question_id.code).data()

    def insert_question(self, project_id: ProjectId, question: Question) -> None:
        with self._driver.session() as session:
            q: dict = self.__convert_question_in_node(question)
            session.run("CREATE (:Question $question)", question=q).data()

            for answer in question.available_answers:
                session.run(
                    "CREATE (:Answer $answer)",
                    answer=serialize(answer),
                ).data()
                session.run(
                    "MATCH (q:Question {id: $question_id}) MATCH (a:Answer {text: $text, value: $value}) CREATE (q)-[:HAS_ANSWER]->(a)",
                    question_id=question.id.code,
                    text=answer.text,
                    value=answer.value,
                ).data()

    def update_question(
        self, project_id: ProjectId, question_id: str, question
    ) -> None:
        pass

    def delete_question(self, project_id: ProjectId, question_id: str) -> None:
        pass

    def __convert_question_in_node(self, question: Question) -> dict:
        q: dict = serialize(question)
        q["id"] = question.id.code
        del q["available_answers"]
        del q["selected_answers"]
        return q


if __name__ == "__main__":
    print(GraphQuestionRepository().get_all_questions(ProjectId(code="project1")))
    # GraphQuestionRepository().insert_question(
    #     ProjectId(code="project1"),
    #     QuestionFactory().create_question(
    #         QuestionId(code="ci-question"),
    #         "Do you use CI?",
    #         QuestionType.SINGLE_CHOICE,
    #         frozenset(
    #             {
    #                 AnswerFactory().cre   ate_answer("Yes", "yes"),
    #                 AnswerFactory().create_answer("A little bit", "little-bit"),
    #                 AnswerFactory().create_answer("No", "no"),
    #             }
    #         ),
    #         action_needed=Action.METRICS_CHECK,
    #     ),
    # )
