from abc import ABC, abstractmethod
from typing import List, Optional

from domain.project.core import ProjectId, Project


class ProjectRepository(ABC):

    @abstractmethod
    def get_all_projects(self) -> List[Project]:
        """Gets all projects
        :return: a list of all projects"""
        pass

    @abstractmethod
    def get_project_by_id(self, project_id: ProjectId) -> Optional[Project]:
        """Gets a project by its id
        :param project_id: the project id
        :return: the project or None if it does not exist"""
        pass

    @abstractmethod
    def insert_project(self, project) -> ProjectId:
        """Inserts a project
        :param project: the project to insert
        :return: the id of the inserted project
        :raises ValueError: if the project already exists"""
        pass

    @abstractmethod
    def update_project(self, project_id: ProjectId, project) -> None:
        """Updates an existing project
        :param project_id: the id of the project to update
        :param project: the updated project
        :raises ValueError: if the project does not exist"""
        pass

    @abstractmethod
    def delete_project(self, project_id: ProjectId) -> None:
        """Deletes a project
        :param project_id: the id of the project to delete
        :raises ValueError: if the project does not exist"""
        pass
