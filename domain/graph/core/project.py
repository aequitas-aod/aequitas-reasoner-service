from pydantic import BaseModel

from domain.graph.core.project_id import ProjectId


class Project(BaseModel):

    id: ProjectId
    name: str

    def __str__(self) -> str:
        return f"Project(id={self.id}, name={self.name})"

    def __hash__(self):
        return hash(self.name)
