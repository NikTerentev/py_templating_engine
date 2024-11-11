from .expression_node import ExpressionNode


class StatementsNode(ExpressionNode):
    def __init__(self) -> None:
        self.code_strings: list[ExpressionNode] = []

    def add_node(self, node: ExpressionNode) -> None:
        self.code_strings.append(node)
