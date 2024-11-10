from dataclasses import dataclass
from .token_type import TokenType


@dataclass
class Token:
    type: TokenType
    text: str
    position: int
