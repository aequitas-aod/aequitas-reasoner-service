from app.domain.core.Answer import Answer


class AnswerFactory:

    def create_answer(self, text: str, value: str):
        return Answer(text, value)

    def create_boolean_answer(self, value: bool):
        return Answer("Yes" if value else "No", str(value))
