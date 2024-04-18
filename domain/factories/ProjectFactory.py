from domain.core import Project
from domain.core import ProjectId


class ProjectFactory:

    def create_project(self, project_id: ProjectId, name: str) -> Project:
        return Project(
            id=project_id,
            name=name,
        )
