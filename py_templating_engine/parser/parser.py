from .. import ast, token


class Parser:
    """Performs syntactic analysis based on a sequence of tokens."""

    def __init__(self, tokens: list[token.Token]) -> None:
        self.position: int = 0
        self.tokens: list[token.Token] = tokens

    def parse_code(self) -> ast.ExpressionNode:
        root_node = ast.StatementsNode()
        while self.position < len(self.tokens):
            code_string_node = self.parse_expression()
            if code_string_node:
                root_node.add_node(code_string_node)
        return root_node

    def parse_expression(self) -> ast.ExpressionNode | None:
        if left_bracket := self.match(
            [token.TokenType.OPEN_VARIABLE_BRACKETS],
        ):
            left_bracket_node = ast.LeftBracketNode(left_bracket)

            variable = self.match([token.TokenType.VARIABLE])
            if not variable:
                self.position += 1
                variable = self.match([token.TokenType.VARIABLE])

            if variable:
                right_bracket = self.match(
                    [token.TokenType.CLOSE_VARIABLE_BRACKETS],
                )

                if not right_bracket:
                    self.position += 1
                    right_bracket = self.match(
                        [token.TokenType.CLOSE_VARIABLE_BRACKETS],
                    )

                if right_bracket:
                    right_bracket_node = ast.RightBracketNode(right_bracket)

                    variable_node = ast.VariableNode(
                        left_bracket_node,
                        variable,
                        right_bracket_node,
                    )

                    return variable_node
            else:
                if self.position > 0 and self.position < len(self.tokens):
                    self.position -= 2

                code: token.Token | None = self.match(
                    [
                        token.TokenType.OPEN_VARIABLE_BRACKETS,
                        token.TokenType.SPACE,
                        token.TokenType.VARIABLE,
                        token.TokenType.CODE,
                    ],
                )
                if code:
                    return ast.CodeNode(code)
                self.position += 1
        else:
            code: token.Token | None = self.match(
                [
                    token.TokenType.CLOSE_VARIABLE_BRACKETS,
                    token.TokenType.SPACE,
                    token.TokenType.VARIABLE,
                    token.TokenType.CODE,
                ],
            )
            if code:
                return ast.CodeNode(code)
            self.position += 1

    def match(
        self,
        expected_tokens: list[token.TokenType],
    ) -> token.Token | None:
        if self.position < len(self.tokens):
            current_token = self.tokens[self.position]
            if current_token.type in expected_tokens:
                self.position += 1
                return current_token
        return None
