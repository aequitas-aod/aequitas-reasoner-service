from typing import List, Self

from app.domain.core.Answer import Answer
from app.domain.core.QuestionId import QuestionId
from app.domain.core.enum.Action import Action
from app.domain.core.enum.QuestionType import QuestionType


class Question:

    def __init__(
        self,
        question_id: QuestionId,
        text: str,
        question_type: QuestionType,
        available_answers: List[Answer],
        selected_answer: List[Answer] = [],
        action_needed: Action = None,
    ):
        self._id = question_id
        self._text = text
        self._type = question_type
        self._availableAnswers = available_answers
        self._selectedAnswer = selected_answer
        self._actionNeeded = action_needed

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
    def available_answers(self) -> List[Answer]:
        return self._availableAnswers

    @property
    def selected_answer(self) -> List[Answer]:
        return self._selectedAnswer

    @property
    def action_needed(self) -> Action:
        return self._actionNeeded

    def select_answer(self, answer: Answer) -> Self:
        return Question(
            self.id,
            self.text,
            self.type,
            self.available_answers,
            self.selected_answer + [answer],
            self.action_needed,
        )

    def __str__(self) -> str:
        return (
            f"Question(id={self.id}, text={self.text}, type={self.type}, available_answers={self.available_answers},"
            f"selected_answer={self.selected_answer}, action_needed={self.action_needed})"
        )

    def __eq__(self, other: Self) -> bool:
        return self.id == other.idl
