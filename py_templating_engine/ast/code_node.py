from py_templating_engine.token import Token

from .expression_node import ExpressionNode


class CodeNode(ExpressionNode):
    def __init__(self, code: Token) -> None:
        self.variable = code
