from typing import Optional, FrozenSet

from pydantic import BaseModel
from typing_extensions import Self

from app.domain.core.Answer import Answer
from app.domain.core.QuestionId import QuestionId
from app.domain.core.enum.Action import Action
from app.domain.core.enum.QuestionType import QuestionType


class Question(BaseModel):

    def __init__(
        self,
        text: str,
        question_type: QuestionType,
        available_answers: FrozenSet[Answer],
        selected_answers: FrozenSet[Answer] = frozenset(),
        action_needed: Optional[Action] = None,
    ):
        super().__init__()
        self._text: str = text
        self._type: QuestionType = question_type
        self._available_answers: FrozenSet[Answer] = available_answers
        self._selected_answers: FrozenSet[Answer] = selected_answers
        self._action_needed: Optional[Action] = action_needed
        self._id = QuestionId(str(hash(self)))

    @property
    def id(self) -> QuestionId:
        return self._id

    @property
    def text(self) -> str:
        return self._text

    @property
    def type(self) -> QuestionType:
        return self._type

    @property
    def available_answers(self) -> FrozenSet[Answer]:
        return self._available_answers

    @property
    def selected_answers(self) -> FrozenSet[Answer]:
        return self._selected_answers

    @property
    def action_needed(self) -> Optional[Action]:
        return self._action_needed

    def select_answer(self, answer: Answer) -> Self:
        """Return a new question with the selected answer added to the selected answers set.
        If the answer is already in the selected answers set, the same question is returned.
        :param answer: the answer to be added to the selected answers set
        :raises ValueError: if the answer is not in the available answers set
        """
        if answer not in self.available_answers:
            raise ValueError(f"Answer {answer} is not available for this question")

        return Question(
            self.text,
            self.type,
            self.available_answers,
            self.selected_answers.union({answer}),
            self.action_needed,
        )

    def deselect_answer(self, answer: Answer) -> Self:
        return Question(
            self.text,
            self.type,
            self.available_answers,
            self.selected_answers.difference({answer}),
            self.action_needed,
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
