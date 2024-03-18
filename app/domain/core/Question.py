from typing import List

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
