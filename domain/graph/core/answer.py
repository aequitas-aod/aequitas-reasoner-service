from pydantic import BaseModel

from domain.graph.core import AnswerId


class Answer(BaseModel):

    id: AnswerId
    text: str
    value: str

    def __str__(self):
        return f"Answer(\n id={self.id},\n text='{self.text}',\n value='{self.value}')"

    def __hash__(self):
        return hash((self.id.code, self.text, self.value))
