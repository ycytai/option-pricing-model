from dataclasses import dataclass

from common.enums import OptionType


@dataclass
class WrongOptionTypeException(Exception):
    user_input: str

    def __str__(self) -> str:
        return f'Wrong option type input. Expected {[x for x in OptionType.__members__]}, got "{self.user_input}".'
