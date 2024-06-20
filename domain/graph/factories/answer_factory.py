from domain.graph.core.answer import Answer, AnswerId


class AnswerFactory:

    @staticmethod
    def create_answer(answer_id: AnswerId, text: str, value: str):
        return Answer(id=answer_id, text=text, value=value)

    @staticmethod
    def create_boolean_answer(answer_id: AnswerId, value: bool):
        return Answer(id=answer_id, text="Yes" if value else "No", value=str(value))
