import re

from py_templating_engine.token import Token
from py_templating_engine.token.token_type import token_types_list


class Lexer:
    def __init__(self, file_path: str):
        self.position: int = 0
        self.token_list: list[Token] = []
        self.file_path: str = file_path

    def lexical_analysis(self) -> list[Token]:
        with open(self.file_path) as file:
            while line := file.readline():
                self.fill_token_list(line)

        return self.token_list

    def fill_token_list(self, file_line: str) -> None:
        local_position = 0
        while local_position + 1 <= len(file_line):
            for token_type in token_types_list.values():
                match = re.search(
                    f"^{token_type.regex}", file_line[local_position:],
                )
                if match:
                    new_token = Token(
                        token_type,
                        match.group(),
                        local_position + self.position,
                    )
                    local_position += match.end()
                    self.token_list.append(new_token)
                    break
        self.position += local_position
