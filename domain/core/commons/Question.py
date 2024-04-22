from typing import Optional, FrozenSet

from pydantic import BaseModel, field_serializer

from domain.core.commons import Answer, QuestionId
from domain.core.commons.enum import Action
from domain.core.commons.enum import QuestionType


class Question(BaseModel):
    id: QuestionId
    text: str
    type: QuestionType
    available_answers: FrozenSet[Answer]
    action_needed: Optional[Action] = None

    @field_serializer("available_answers", when_used="json")
    def serialize_courses_in_order(self, answers: FrozenSet[Answer]):
        return sorted(answers, key=lambda answer: answer.text)

    def __str__(self) -> str:
        return (
            f"Question(id={self.id}, text={self.text}, type={self.type}, available_answers={self.available_answers},"
            f"action_needed={self.action_needed})"
        )

    def __hash__(self):
        return hash(
            (
                self.text,
                self.type,
                self.available_answers,
                self.action_needed,
            )
        )
