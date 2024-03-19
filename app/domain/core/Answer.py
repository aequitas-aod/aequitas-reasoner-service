from dataclasses import dataclass


@dataclass
class Answer:

    text: str
    value: str

    def __hash__(self):
        return hash((self.text, self.value))
