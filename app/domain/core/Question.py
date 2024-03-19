from typing import Optional, FrozenSet

from pydantic import BaseModel
from typing_extensions import Self

from app.domain.core.Answer import Answer
from app.domain.core.QuestionId import QuestionId
from app.domain.core.enum.Action import Action
from app.domain.core.enum.QuestionType import QuestionType


class Question(BaseModel):
    text: str
    type: QuestionType
    available_answers: FrozenSet[Answer]
    selected_answers: FrozenSet[Answer] = frozenset()
    action_needed: Optional[Action] = None
    id: QuestionId = QuestionId(code=str(hash("ss")))

    def select_answer(self, answer: Answer) -> Self:
        """Return a new question with the selected answer added to the selected answers set.
        If the answer is already in the selected answers set, the same question is returned.
        :param answer: the answer to be added to the selected answers set
        :raises ValueError: if the answer is not in the available answers set
        """
        if answer not in self.available_answers:
            raise ValueError(f"Answer {answer} is not available for this question")
        return Question(
            text=self.text,
            type=self.type,
            available_answers=self.available_answers,
            selected_answers=self.selected_answers.union({answer}),
            action_needed=self.action_needed
        )

    def deselect_answer(self, answer: Answer) -> Self:
        return Question(
            text=self.text,
            type=self.type,
            available_answers=self.available_answers,
            selected_answers=self.selected_answers.difference({answer}),
            action_needed=self.action_needed
        )

    def __str__(self) -> str:
        return (
            f"Question(id={self.id}, text={self.text}, type={self.type}, available_answers={self.available_answers},"
            f"selected_answer={self.selected_answers}, action_needed={self.action_needed})"
        )

    def __eq__(self, other: Self) -> bool:
        return self.id == other.id

    def __hash__(self):
        return hash(
            (
                self.text,
                self.type,
                self.available_answers,
                self.selected_answers,
                self.action_needed,
            )
        )


if __name__ == '__main__':
    question = Question(
        text="Do you practice TDD?",
        type=QuestionType.BOOLEAN,
        available_answers=frozenset([Answer(text="Yes", value="yes"), Answer(text="No", value="no")]),
        action_needed=Action.METRICS_CHECK,
    )
    print(question.model_dump_json())
