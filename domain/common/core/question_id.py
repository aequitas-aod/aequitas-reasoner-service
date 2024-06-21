from pydantic import BaseModel


class QuestionId(BaseModel):

    code: str

    def __str__(self):
        return f"QuestionId(code='{self.code}')"

    def __hash__(self):
        hash(self.code)
