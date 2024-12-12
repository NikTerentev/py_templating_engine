from py_templating_engine.token import Token

from .expression_node import ExpressionNode


class LeftBracketNode(ExpressionNode):
    def __init__(self, bracket: Token) -> None:
        self.bracket = bracket
