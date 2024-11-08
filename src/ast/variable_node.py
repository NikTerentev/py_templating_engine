from src.token import Token
from .expression_node import ExpressionNode
from .left_bracket_node import LeftBracketNode
from .right_bracket_node import RightBracketNode


class VariableNode(ExpressionNode):

    def __init__(
        self,
        left_bracket: LeftBracketNode,
        variable: Token,
        right_bracket: RightBracketNode,
    ) -> None:
        self.left_bracket = left_bracket
        self.variable = variable
        self.right_bracket = right_bracket
