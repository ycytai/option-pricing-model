from enum import Enum


class OptionType(str, Enum):
    Call = 'C'
    Put = 'P'
