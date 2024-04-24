from pydantic import BaseModel

from domain.graph.core.answer_id import AnswerId


class Answer(BaseModel):

    id: AnswerId
    text: str
    value: str

    def __str__(self):
        return f"Answer(id='{self.id}' text='{self.text}', value='{self.value}')"

    def __hash__(self):
        return hash((self.id.code, self.text, self.value))
