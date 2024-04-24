from pydantic import BaseModel


class AnswerId(BaseModel):

    code: str

    def __str__(self):
        return f"AnswerId(code={self.code})"
