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
        self.project: Project = ProjectFactory().create_project(
            ProjectId(code="test-core"),
            "Test core",
        )

    def test_get_all_projects(self):
        project2: Project = self.project.model_copy()
        project2.id = ProjectId(code="test-core-2")
        self.app.post("/projects", json=serialize(self.project))
        self.app.post("/projects", json=serialize(project2))
        response = self.app.get("/projects")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(json.loads(response.data)))
        all_projects: Set[Project] = set(
            [deserialize(project, Project) for project in json.loads(response.data)]
        )
        self.assertEqual({self.project, project2}, all_projects)

    def test_get_project(self):
        self.app.post("/projects", json=serialize(self.project))
        response = self.app.get("/projects/test-core")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.project, deserialize(json.loads(response.data), Project))

    def test_get_non_existent_project(self):
        response = self.app.get("/projects/does-not-exist")
        self.assertEqual(response.status_code, 404)

    def test_insert_project(self):
        response = self.app.post("/projects", json=serialize(self.project))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.project, deserialize(json.loads(response.data), Project))

    def test_delete_project(self):
        self.app.post("/projects", json=serialize(self.project))
        response = self.app.delete("/projects", json=serialize(self.project.id))
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/projects/test-core")
        self.assertEqual(response.status_code, 404)
