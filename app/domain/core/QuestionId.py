from pydantic import BaseModel


class QuestionId(BaseModel):

    code: str

    def __str__(self):
        return f"QuestionId(code={self.code})"


if __name__ == '__main__':
    question_id = QuestionId(code="123")
    print(question_id.model_dump_json())