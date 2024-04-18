from domain.core import Answer


class AnswerFactory:

    def create_answer(self, text: str, value: str):
        return Answer(text=text, value=value)

    def create_boolean_answer(self, value: bool):
        return Answer(text="Yes" if value else "No", value=str(value))
