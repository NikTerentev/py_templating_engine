from py_templating_engine import ast, token
from py_templating_engine.token import Token


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.position: int = 0
        self.tokens = tokens

    def match(self, expected_tokens: list[token.TokenType]) -> Token | None:
        if self.position < len(self.tokens):
            current_token = self.tokens[self.position]
            if current_token.type in expected_tokens:
                self.position += 1
                return current_token
        return None

    def parse_expression(self) -> ast.ExpressionNode | None:
        if left_bracket := self.match(
            [token.token_types_list["OPEN_VARIABLE_BRACKETS"]],
        ):
            left_bracket_node = ast.LeftBracketNode(left_bracket)

            variable = self.match([token.token_types_list["VARIABLE"]])
            skipped = False
            if not variable:
                skipped = True
                self.position += 1
                variable = self.match([token.token_types_list["VARIABLE"]])

            if variable:
                right_bracket = self.match(
                    [token.token_types_list["CLOSE_VARIABLE_BRACKETS"]],
                )

                if not right_bracket:
                    self.position += 1
                    right_bracket = self.match(
                        [token.token_types_list["CLOSE_VARIABLE_BRACKETS"]],
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
                self.position -= 2 if skipped else -1
                code: Token | None = self.match(
                    [
                        token.token_types_list["OPEN_VARIABLE_BRACKETS"],
                        token.token_types_list["SPACE"],
                        token.token_types_list["VARIABLE"],
                        token.token_types_list["CODE"],
                    ],
                )
                if code:
                    return ast.CodeNode(code)
                self.position += 1
        else:
            code: Token | None = self.match(
                [
                    token.token_types_list["CLOSE_VARIABLE_BRACKETS"],
                    token.token_types_list["SPACE"],
                    token.token_types_list["VARIABLE"],
                    token.token_types_list["CODE"],
                ],
            )
            if code:
                return ast.CodeNode(code)
            self.position += 1

    def parse_code(self) -> ast.ExpressionNode:
        root_node = ast.StatementsNode()
        while self.position < len(self.tokens):
            code_string_node = self.parse_expression()
            if code_string_node:
                root_node.add_node(code_string_node)
        return root_node
