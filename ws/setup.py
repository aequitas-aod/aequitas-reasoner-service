from application import QuestionService
from domain.graph.repositories import QuestionRepository
from infrastructure.storage.graph.repositories import Neo4jQuestionRepository

question_repository: QuestionRepository = Neo4jQuestionRepository()
question_service: QuestionService = QuestionService(question_repository)
