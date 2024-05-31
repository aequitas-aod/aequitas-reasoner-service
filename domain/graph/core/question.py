from datetime import datetime
from typing import Optional, FrozenSet

from pydantic import BaseModel, field_serializer

from domain.graph.core import Answer, QuestionId, AnswerId
from domain.graph.core.enum import Action, QuestionType


class Question(BaseModel):
    id: QuestionId
    text: str
    type: QuestionType
    available_answers: FrozenSet[Answer]
    previous_question_id: Optional[QuestionId]
    enabled_by: FrozenSet[AnswerId]
    action_needed: Optional[Action]
    created_at: datetime

    @field_serializer("available_answers", when_used="json")
    def serialize_available_answers_in_order(self, answers: FrozenSet[Answer]):
        return sorted(answers, key=lambda answer: answer.text)

    @field_serializer("enabled_by", when_used="json")
    def serialize_enabled_by_in_order(self, answer_ids: FrozenSet[AnswerId]):
        return sorted(answer_ids, key=lambda answer_id: answer_id.code)

    def __str__(self) -> str:
        return (
            f"Question(\n id={self.id},\n text='{self.text}',\n type={self.type},\n previous_question_id={self.previous_question_id},\n"
            f" available_answers={self.available_answers},\n enabled_by={self.enabled_by},\n action_needed={self.action_needed}"
            f" created_at={self.created_at}\n)"
        )

    def __hash__(self):
        return hash(
            (
                self.id.code,
                self.text,
                self.type,
                self.available_answers,
                self.enabled_by,
                self.action_needed,
                self.created_at,
            )
        )
