from typing import Optional, FrozenSet

from pydantic import BaseModel, field_serializer

from domain.graph.core import Answer, QuestionId
from domain.graph.core.enum import Action, QuestionType


class Question(BaseModel):
    id: QuestionId
    text: str
    type: QuestionType
    available_answers: FrozenSet[Answer]
    previous_question_id: Optional[QuestionId]
    action_needed: Optional[Action] = None

    @field_serializer("available_answers", when_used="json")
    def serialize_courses_in_order(self, answers: FrozenSet[Answer]):
        return sorted(answers, key=lambda answer: answer.text)

    def __str__(self) -> str:
        return (
            f"Question(id={self.id}, text={self.text}, type={self.type}, previous_question_id={self.previous_question_id},"
            f"available_answers={self.available_answers}, action_needed={self.action_needed})"
        )

    def __hash__(self):
        return hash(
            (
                self.id.code,
                self.text,
                self.type,
                self.available_answers,
                self.action_needed,
            )
        )
