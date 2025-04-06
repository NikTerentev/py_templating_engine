import re
from enum import Enum


class TokenType(Enum):
    """Contain types of tokens along with their regular expressions."""

    OPEN_VARIABLE_BRACKETS = re.compile(r"{{")
    CLOSE_VARIABLE_BRACKETS = re.compile(r"}}")
    SPACE = re.compile(r"[ \t\r\n]+")
    VARIABLE = re.compile(r"(templater\.\S+?)(?=}}|\s)")
    CODE = re.compile(r"(\S+?)(?={{|\s|$)")
