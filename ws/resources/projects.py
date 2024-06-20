import json
from typing import List, Set, Optional

from flask import Blueprint, request
from flask_restful import Api, Resource

from domain.project.core import Project, ProjectId
from presentation.presentation import serialize, deserialize
from utils.errors import ConflictError
from utils.status_code import StatusCode
from ws.setup import project_service
from ws.utils.logger import logger

projects_bp = Blueprint("projects", __name__)
api = Api(projects_bp)

projects: Set = set()


class ProjectResource(Resource):

    def get(self, project_id=None):
        if project_id:
            project: Optional[Project] = project_service.get_project_by_id(
                ProjectId(code=project_id)
            )
            if project:
                return serialize(project), StatusCode.OK
            else:
                return "Project not found", StatusCode.NOT_FOUND
        else:
            all_projects: List = project_service.get_all_projects()
            return [serialize(project) for project in all_projects], StatusCode.OK

    def post(self):
        body: dict = request.get_json()
        logger.info(f"Received request {body}")
        try:
            project_id: ProjectId = project_service.add_project(body["name"])
        except ConflictError as e:
            return e.message, e.status_code
        project_created: Project = project_service.get_project_by_id(project_id)
        return serialize(project_created), StatusCode.CREATED

    def delete(self):
        project_id: ProjectId = deserialize(request.get_json(), ProjectId)
        projects.remove(list(filter(lambda q: q.id == project_id, projects)).pop())
        return "", StatusCode.OK


api.add_resource(ProjectResource, "/projects", "/projects/<string:project_id>")
