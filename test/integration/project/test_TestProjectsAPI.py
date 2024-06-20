import json
import unittest
from typing import Set

from domain.project.core import Project, ProjectId
from domain.project.factories import ProjectFactory
from ws.main import create_app
from presentation.presentation import serialize, deserialize


class TestProjectsAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        self.project_name_1: str = "Project name 1"
        self.project_name_2: str = "Project name 2"

    def test_get_all_projects(self):
        self.app.post("/projects", json={"name": self.project_name_1})
        self.app.post("/projects", json={"name": self.project_name_2})
        response = self.app.get("/projects")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(json.loads(response.data)))
        all_projects: Set[Project] = set(
            [deserialize(project, Project) for project in json.loads(response.data)]
        )
        self.assertEqual(map(lambda p: p.name, all_projects), {self.project_name_1, self.project_name_2})

    def test_get_project(self):
        self.app.post("/projects", json={"name": self.project_name_1})
        response = self.app.get("/projects/test-1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.project_name_1, deserialize(json.loads(response.data), Project))

    def test_get_non_existent_project(self):
        response = self.app.get("/projects/does-not-exist")
        self.assertEqual(response.status_code, 404)

    def test_insert_project(self):
        response = self.app.post("/projects", json={"name": self.project_name_1})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.project_name_1, deserialize(json.loads(response.data), Project))

    def test_delete_project(self):
        response = self.app.post("/projects", json={"name": self.project_name_1})
        created_project_id: ProjectId = deserialize(json.loads(response.data), ProjectId)
        response = self.app.delete("/projects", json=serialize(created_project_id))
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/projects/test-1")
        self.assertEqual(response.status_code, 404)
