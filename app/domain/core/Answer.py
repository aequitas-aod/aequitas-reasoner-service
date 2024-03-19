from pydantic import BaseModel


class Answer(BaseModel):

    def __init__(self, text: str, value: str):
        super().__init__()
        self._text = text
        self._value = value

    @property
    def text(self) -> str:
        return self._text

    @property
    def value(self) -> str:
        return self._value

    def __str__(self):
        return f"Answer(text='{self.text}', value='{self.value}')"

    def __hash__(self):
        return hash((self.text, self.value))
