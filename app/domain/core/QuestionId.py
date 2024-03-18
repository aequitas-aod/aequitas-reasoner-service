class QuestionId:

    def __init__(self, code: str):
        self._code = code

    @property
    def code(self):
        return self._code

    def __eq__(self, other):
        return self.code == other.code

    def __str__(self):
        return f"QuestionId(code={self.code})"
