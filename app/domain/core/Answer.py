class Answer:

    def __init__(self, text: str, value: str):
        self._text = text
        self._value = value

    @property
    def text(self):
        return self._text

    @property
    def value(self):
        return self._value

    def __str__(self):
        return f"Answer(text={self.text}, value={self.value})"

    def __eq__(self, other):
        return self.text == other.text and self.value == other.value
