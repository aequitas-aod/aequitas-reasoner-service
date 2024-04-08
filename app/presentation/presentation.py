import json

from pydantic import BaseModel
import app.domain.core as _core_domain


# def serialize_answer(answer: Answer) -> dict:
#     return json.loads(answer.model_dump_json())


# def deserialize_answer(answer: dict) -> Answer:
#     return Answer(**answer)


# def serialize_question(question: Question) -> dict:
#     return json.loads(question.model_dump_json())


# def deserialize_question(question: dict) -> Question:
#     return Question(**question)


# def serialize_question_id(question_id: QuestionId) -> dict:
#     return json.loads(question_id.model_dump_json())


# def deserialize_question_id(question_id: dict) -> QuestionId:
#     return QuestionId(**question_id)


def _is_admissible_type(obj: type) -> bool:
    for name in dir(_core_domain):
        symbol = getattr(_core_domain, name)
        if isinstance(symbol, type) and issubclass(obj, symbol):
            return True
    return False


def serialize(obj: BaseModel) -> dict:
    if not _is_admissible_type(type(obj)):
        raise ValueError(f"Type {type(obj)} is not admissible")
    return json.loads(obj.model_dump_json())


def deserialize(obj: dict, type: type) -> BaseModel:
    if not _is_admissible_type(type):
        raise ValueError(f"Type {type} is not admissible")
    return type(**obj)
