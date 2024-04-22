import os
from typing import List
from typing_extensions import LiteralString

from dotenv import load_dotenv
from neo4j import GraphDatabase

from domain.core import ProjectId, QuestionId
from domain.core import Question
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

    def get_all_questions(self, project_id: ProjectId) -> List[Question]:
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
                q["selected_answers"] = []
                questions.append(deserialize(q, Question))
            return questions

    def get_question_by_id(
        self, project_id: ProjectId, question_id: QuestionId
    ) -> Question:
        query: LiteralString = (
            "MATCH (q:Question {id: $question_id})-[:HAS_ANSWER]->(a:Answer) RETURN q, COLLECT(a) AS answers"
        )
        with self._driver.session() as session:
            res: list[dict] = session.run(query, question_id=question_id.code).data()
            question: dict = res[0]["q"]
            question["id"] = {"code": question["id"]}
            question["available_answers"] = [a for a in res[0]["answers"]]
            question["selected_answers"] = []
            return deserialize(question, Question)

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
    print(
        GraphQuestionRepository().get_question_by_id(
            ProjectId(code="project1"), QuestionId(code="ci-question")
        )
    )
    # GraphQuestionRepository().insert_question(
    #     ProjectId(code="project1"),
    #     QuestionFactory().create_question(
    #         QuestionId(code="ci-question"),
    #         "Do you use CI?",
    #         QuestionType.SINGLE_CHOICE,
    #         frozenset(
    #             {
    #                 AnswerFactory().create_answer("Yes", "yes"),
    #                 AnswerFactory().create_answer("A little bit", "little-bit"),
    #                 AnswerFactory().create_answer("No", "no"),
    #             }
    #         ),
    #         action_needed=Action.METRICS_CHECK,
    #     ),
    # )
