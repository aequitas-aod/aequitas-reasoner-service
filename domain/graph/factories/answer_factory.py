from domain.graph.core.answer import Answer
from domain.graph.core.answer_id import AnswerId


class AnswerFactory:

    def create_answer(self, answer_id: AnswerId, text: str, value: str):
        return Answer(id=answer_id, text=text, value=value)

    def create_boolean_answer(self, answer_id: AnswerId, value: bool):
        return Answer(id=answer_id, text="Yes" if value else "No", value=str(value))
