from pydantic import BaseModel


class Answer(BaseModel):
    text: str
    value: str

    def __hash__(self):
        return hash((self.text, self.value))
