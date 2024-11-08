from .expression_node import ExpressionNode


class StatementsNode(ExpressionNode):
    code_strings: list[ExpressionNode] = []

    @classmethod
    def add_node(cls, node: ExpressionNode) -> None:
        cls.code_strings.append(node)
