from enum import Enum


class QuestionType(Enum):
    BOOLEAN = 0
    SINGLE_CHOICE = 1
    MULTIPLE_CHOICE = 2
    RATING = 3
