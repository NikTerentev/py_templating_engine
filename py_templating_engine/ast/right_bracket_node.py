from py_templating_engine.token import Token

from .expression_node import ExpressionNode


class RightBracketNode(ExpressionNode):
    def __init__(self, bracket: Token):
        self.bracket = bracket
