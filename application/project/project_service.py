from typing import Optional, List

from domain.project.core import Project, ProjectId
from domain.project.repository import ProjectRepository
from utils.errors import BadRequestError


class ProjectService:

    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def get_all_projects(self) -> List[Project]:
        """
        Gets all projects
        :return: a list of all projects
        """
        return self.project_repository.get_all_projects()

    def get_project_by_id(self, project_id: ProjectId) -> Optional[Project]:
        """
        Gets a project by its id
        :param project_id: the project id
        :return: the project or None if it does not exist
        """
        return self.project_repository.get_project_by_id(project_id)

    def add_project(self, project: Project) -> ProjectId:
        """
        Inserts a project
        :param project: the project to insert
        :return: the id of the inserted project
        :raises ConflictError: if the project already exists
        """
        return self.project_repository.insert_project(project)

    def update_project(self, project_id: ProjectId, project: Project) -> None:
        """
        Updates an existing project
        :param project_id: the id of the project to update
        :param project: the updated project
        :raises BadRequestError: if the project id does not match the existing project id
        :raises NotFoundError: if the project does not exist
        """
        if project_id != project.id:
            raise BadRequestError("Updated project id does not match")
        self.project_repository.update_project(project_id, project)

    def delete_project(self, project_id: ProjectId) -> None:
        """
        Deletes a project
        :param project_id: the id of the project to delete
        :raises NotFoundError: if the project does not exist
        """
        self.project_repository.delete_project(project_id)

    def get_new_candidate_id(self) -> ProjectId:
        """
        Gets a new candidate id for a project
        :return: the new candidate id
        """
        increment = 1
        projects_number = len(self.get_all_projects())
        candidate_id: ProjectId = ProjectId(code=f"q-{projects_number + increment}")
        check = self.project_repository.get_project_by_id(candidate_id)
        while check is not None:
            increment += 1
            candidate_id = ProjectId(code=f"q-{projects_number + increment}")
            check = self.project_repository.get_project_by_id(candidate_id)
        return candidate_id
