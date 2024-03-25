import json

from app.domain.core.Answer import Answer
from app.domain.core.Question import Question
from app.domain.core.QuestionId import QuestionId


def serialize_answer(answer: Answer) -> dict:
    return json.loads(answer.model_dump_json())


def deserialize_answer(answer: dict) -> Answer:
    return Answer(**answer)


def serialize_question(question: Question) -> dict:
    return json.loads(question.model_dump_json())


def deserialize_question(question: dict) -> Question:
    return Question(**question)


def serialize_question_id(question_id: QuestionId) -> dict:
    return json.loads(question_id.model_dump_json())


def deserialize_question_id(question_id: dict) -> QuestionId:
    return QuestionId(**question_id)
