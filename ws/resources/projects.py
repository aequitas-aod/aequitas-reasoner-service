import json
from typing import List, Set

from flask import Blueprint, request
from flask_restful import Api, Resource

from domain.project.core import Project, ProjectId
from presentation.presentation import serialize, deserialize

projects_bp = Blueprint("projects", __name__)
api = Api(projects_bp)

projects: Set = set()


class ProjectResource(Resource):

    def get(self, project_id=None):
        if project_id:
            filtered_projects: List[Project] = list(
                filter(lambda project: project.id.code == project_id, projects)
            )
            if len(filtered_projects) == 0:
                return "", 204
            else:
                return serialize(filtered_projects.pop()), 200
        else:
            all_projects: List[dict] = [
                json.loads(project.model_dump_json()) for project in projects
            ]
            return all_projects, 200

    def post(self):
        new_project: Project = deserialize(request.get_json(), Project)
        projects.add(new_project)
        return serialize(new_project), 201

    def delete(self):
        project_id: ProjectId = deserialize(request.get_json(), ProjectId)
        projects.remove(list(filter(lambda q: q.id == project_id, projects)).pop())
        return "", 200


api.add_resource(ProjectResource, "/projects", "/projects/<string:project_id>")
