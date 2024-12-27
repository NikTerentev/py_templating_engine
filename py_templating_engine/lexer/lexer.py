import re
from pathlib import Path

from py_templating_engine.token import Token
from py_templating_engine.token.token_type import token_types_list


class Lexer:
    """Responsible for converting text in a file into a sequence of tokens."""

    def __init__(self, file_path: Path) -> None:
        """Set the starting position, tokens list and compile tokens."""
        self.position = 0
        self.token_list: list[Token] = []
        self.file_path: Path = file_path
        self.compiled_tokens: dict[str, re.Pattern[str]] = {
            token_name: re.compile(token.regex)
            for token_name, token in token_types_list.items()
        }

    def lexical_analysis(self) -> list[Token]:
        """Send each line in the file to be parsed into tokens."""
        try:
            with self.file_path.open() as file:
                while line := file.readline():
                    self.fill_token_list(line)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {self.file_path}") from e
        except OSError as e:
            raise RuntimeError(
                f"Error reading file {self.file_path}: {e}",
            ) from e
        return self.token_list

    def fill_token_list(self, file_line: str) -> None:
        """Break the file line into 'tokens'."""
        local_position = 0
        while local_position + 1 <= len(file_line):
            for token_type, regex in self.compiled_tokens.items():
                match: re.Match[str] | None = regex.match(
                    file_line[local_position:],
                )
                if match:
                    new_token = Token(
                        token_types_list[token_type],
                        match.group(),
                        local_position + self.position,
                    )
                    local_position += match.end()
                    self.token_list.append(new_token)
                    break
            else:
                raise ValueError(
                    f"Unrecognized sequence at position {local_position}: "
                    f"{file_line[local_position:local_position+10]}",
                )
        self.position += local_position
