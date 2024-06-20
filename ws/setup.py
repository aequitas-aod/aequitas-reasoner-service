from application import QuestionService
from application.project.project_service import ProjectService
from domain.graph.repositories import QuestionRepository
from domain.project.repositories import ProjectRepository
from infrastructure.storage.graph.repositories import Neo4jQuestionRepository
from infrastructure.storage.project.repositories.neo4j_project_repository import (
    Neo4jProjectRepository,
)

question_repository: QuestionRepository = Neo4jQuestionRepository()
question_service: QuestionService = QuestionService(question_repository)

project_repository: ProjectRepository = Neo4jProjectRepository()
project_service: ProjectService = ProjectService(project_repository)
