from app.domain.core.Project import Project
from app.domain.core.ProjectId import ProjectId


class ProjectFactory:

    def create_project(self, project_id: ProjectId, name: str) -> Project:
        return Project(
            id=project_id,
            name=name,
        )
