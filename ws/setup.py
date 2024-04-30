from application import QuestionService
from domain.graph.repositories import QuestionRepository
from storage.graph.repositories import GraphQuestionRepository

question_repository: QuestionRepository = GraphQuestionRepository()
question_service: QuestionService = QuestionService(question_repository)
