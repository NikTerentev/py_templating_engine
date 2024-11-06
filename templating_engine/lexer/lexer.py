import re

from templating_engine.token import Token
from templating_engine.token.token_type import token_types_list


class Lexer:
    position: int = 0
    token_list: list[Token] = []

    def __init__(self, file_path: str):
        self.file_path = file_path

    def lexical_analysis(self) -> list[Token]:
        with open(self.file_path) as file:
            for line in file.readlines():
                self.fill_token_list(line)

        return self.token_list

    @classmethod
    def fill_token_list(cls, file_line: str) -> None:
        local_position = 0
        while local_position + 1 < len(file_line):
            for token_type in token_types_list.values():
                match = re.search(
                    f"^{token_type.regex}",
                    file_line[local_position:]
                )
                if match:
                    new_token = Token(
                        token_type,
                        match.group(),
                        local_position + cls.position,
                    )
                    local_position += match.end()
                    cls.token_list.append(new_token)
                    break
        cls.position += local_position
