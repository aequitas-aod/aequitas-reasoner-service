from pydantic import BaseModel


class ProjectId(BaseModel):

    code: str

    def __str__(self):
        return f"ProjectId(code={self.code})"
