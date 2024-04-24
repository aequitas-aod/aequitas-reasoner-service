from domain.graph.core.project import Project
from domain.graph.core.project_id import ProjectId


class ProjectFactory:

    def create_project(self, project_id: ProjectId, name: str) -> Project:
        return Project(
            id=project_id,
            name=name,
        )
