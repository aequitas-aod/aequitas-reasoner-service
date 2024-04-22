from typing import FrozenSet

from pydantic import field_serializer
from typing_extensions import Self

from domain.core import Answer
from domain.core.commons import Question, QuestionId, QuestionType
from domain.core.project.selection import SelectionStrategy, SingleSelectionStrategy


class SelectableQuestion(Question):
    selection_strategy: SelectionStrategy
    selected_answers: FrozenSet[Answer] = frozenset()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def select_answer(self, answer: Answer) -> Self:
        if answer not in self.available_answers:
            raise ValueError(f"Answer {answer} is not available for this question")
        selected_answers = self.selection_strategy.select_answer(answer, self.selected_answers)
        return SelectableQuestion(
            id=self.id,
            text=self.text,
            type=self.type,
            available_answers=self.available_answers,
            action_needed=self.action_needed,
            selection_strategy=self.selection_strategy,
            selected_answers=selected_answers,
        )

    def deselect_answer(self, answer: Answer) -> Self:
        selected_answers = self.selection_strategy.deselect_answer(answer, self.selected_answers)
        return SelectableQuestion(
            id=self.id,
            text=self.text,
            type=self.type,
            available_answers=self.available_answers,
            action_needed=self.action_needed,
            selection_strategy=self.selection_strategy,
            selected_answers=selected_answers,
        )

    @field_serializer("selected_answers", when_used="json")
    def serialize_courses_in_order(self, answers: FrozenSet[Answer]):
        return sorted(answers, key=lambda answer: answer.text)

    def __str__(self) -> str:
        return (
            f"SelectableQuestion(id={self.id}, text={self.text}, type={self.type}, available_answers={self.available_answers},"
            f"action_needed={self.action_needed}, selection_strategy={self.selection_strategy}, selected_answers={self.selected_answers})"
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


if __name__ == '__main__':
    print(SelectableQuestion(
        id=QuestionId(code="question_id"),
        text="Do you practice TDD?",
        type=QuestionType.SINGLE_CHOICE,
        available_answers=frozenset(
            {
                Answer(text="Always", value="always"),
                Answer(text="Never", value="never"),
            }
        ),
        action_needed=None,
        selection_strategy=SingleSelectionStrategy(),
    ))
