import json
from pathlib import Path

from src.token import Token
from src import ast
from src import token


class Parser:
    position: int = 0

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens

    def match(self, expected_tokens: list[token.TokenType]) -> Token | None:
        if (self.position < len(self.tokens)):
            current_token = self.tokens[self.position]
            if current_token.type in expected_tokens:
                self.position += 1
                return current_token
        return None

    def parse_expression(self) -> ast.ExpressionNode | None:
        if left_bracket := self.match(
            [token.token_types_list["OPEN_VARIABLE_BRACKETS"]]
        ):
            left_bracket_node = ast.LeftBracketNode(left_bracket)

            variable = self.match(
                [token.token_types_list["VARIABLE"]]
            )
            skipped = False
            if not variable:
                skipped = True
                self.position += 1
                variable = self.match(
                    [token.token_types_list["VARIABLE"]]
                )

            if variable:
                right_bracket = self.match(
                    [token.token_types_list["CLOSE_VARIABLE_BRACKETS"]]
                )

                if not right_bracket:
                    self.position += 1
                    right_bracket = self.match(
                        [token.token_types_list["CLOSE_VARIABLE_BRACKETS"]]
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
                    ]
                )
                if code:
                    return ast.CodeNode(code)
                else:
                    self.position += 1
        else:
            code: Token | None = self.match(
                [
                    token.token_types_list["CLOSE_VARIABLE_BRACKETS"],
                    token.token_types_list["SPACE"],
                    token.token_types_list["VARIABLE"],
                    token.token_types_list["CODE"],
                ]
            )
            if code:
                return ast.CodeNode(code)
            else:
                self.position += 1

    def parse_code(self) -> ast.ExpressionNode:
        root_node = ast.StatementsNode()
        while self.position < len(self.tokens):
            code_string_node = self.parse_expression()
            if code_string_node:
                root_node.add_node(code_string_node)
        return root_node

    def render(
        self,
        root_node: ast.ExpressionNode,
        file_path: str,
        config_file_path: str = "templater.json",
    ) -> None:
        with open(config_file_path, "r") as config_file:
            config = json.load(config_file)
        rendered_dir = "rendered_files"
        Path(rendered_dir).mkdir()
        result_path = Path(rendered_dir) / Path(file_path)
        with open(result_path, "w") as result_file:
            for code_string in root_node.code_strings:
                if code_string.variable.type == token.token_types_list[
                    "VARIABLE"
                ]:
                    code_string.variable.text = config.get(
                        code_string.variable.text.replace(
                            "templater.", "", 1
                        )
                    )
                result_file.write(code_string.variable.text)
