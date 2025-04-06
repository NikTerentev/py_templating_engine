from .expression_node import ExpressionNode


class StatementsNode(ExpressionNode):
    def __init__(
        self,
        code_strings: list[ExpressionNode] | None = None,
    ) -> None:
        if code_strings is None:
            code_strings = []

        self.code_strings = code_strings

    def add_node(self, node: ExpressionNode) -> None:
        self.code_strings.append(node)
