from typing import Optional, FrozenSet

from pydantic import BaseModel, field_serializer
from typing_extensions import Self

from domain.core import Answer
from domain.core.QuestionId import QuestionId
from domain.core.enum import Action
from domain.core.enum import QuestionType


class Question(BaseModel):

    id: QuestionId
    text: str
    type: QuestionType
    available_answers: FrozenSet[Answer]
    selected_answers: FrozenSet[Answer] = frozenset()
    action_needed: Optional[Action] = None

    def select_answer(self, answer: Answer) -> Self:
        """Return a new question with the selected answer added to the selected answers set.
        If the answer is already in the selected answers set, the same question is returned.
        :param answer: the answer to be added to the selected answers set
        :raises ValueError: if the answer is not in the available answers set
        """
        if answer not in self.available_answers:
            raise ValueError(f"Answer {answer} is not available for this question")
        return Question(
            id=self.id,
            text=self.text,
            type=self.type,
            available_answers=self.available_answers,
            selected_answers=self.selected_answers.union({answer}),
            action_needed=self.action_needed,
        )

    def deselect_answer(self, answer: Answer) -> Self:
        return Question(
            id=self.id,
            text=self.text,
            type=self.type,
            available_answers=self.available_answers,
            selected_answers=self.selected_answers.difference({answer}),
            action_needed=self.action_needed,
        )

    @field_serializer("available_answers", "selected_answers", when_used="json")
    def serialize_courses_in_order(self, answers: FrozenSet[Answer]):
        return sorted(answers, key=lambda answer: answer.text)

    def __str__(self) -> str:
        return (
            f"Question(id={self.id}, text={self.text}, type={self.type}, available_answers={self.available_answers},"
            f"selected_answer={self.selected_answers}, action_needed={self.action_needed})"
        )

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
