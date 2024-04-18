from pydantic import BaseModel


class Answer(BaseModel):

    text: str
    value: str

    def __str__(self):
        return f"Answer(text='{self.text}', value='{self.value}')"

    def __hash__(self):
        return hash((self.text, self.value))
