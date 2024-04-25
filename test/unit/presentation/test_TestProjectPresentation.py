import unittest

from domain.project.core import Project, ProjectId
from domain.project.factories import ProjectFactory
from presentation.presentation import serialize, deserialize


class TestProjectSerialization(unittest.TestCase):

    def setUp(self):
        self.project: Project = ProjectFactory().create_project(
            ProjectId(code="project1"),
            "project_name",
        )
        self.project_dict: dict = {
            "id": {"code": "project1"},
            "name": "project_name",
        }

    def test_serialize_question(self):
        expected: dict = {
            "id": {"code": "project1"},
            "name": "project_name",
        }
        actual: dict = serialize(self.project)
        self.assertEqual(
            expected,
            actual,
        )

    def test_deserialize_project(self):
        expected: Project = ProjectFactory().create_project(
            ProjectId(code="project1"),
            "project_name",
        )
        actual: Project = deserialize(self.project_dict, Project)
        self.assertEqual(
            expected,
            actual,
        )
