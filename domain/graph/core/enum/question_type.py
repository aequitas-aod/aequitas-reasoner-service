from enum import Enum


class QuestionType(Enum):
    BOOLEAN = 'boolean'
    SINGLE_CHOICE = 'single'
    MULTIPLE_CHOICE = 'multiple'
    RATING = 'rating'
