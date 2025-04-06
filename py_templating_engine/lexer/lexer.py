import re
from pathlib import Path

from .. import token


class Lexer:
    """Responsible for converting text in a file into a sequence of tokens."""

    def __init__(self, file_path: Path) -> None:
        """Set the starting position, tokens list and compile tokens."""
        self.position = 0
        self.token_list: list[token.Token] = []
        self.file_path: Path = file_path

    def lexical_analysis(self) -> list[token.Token]:
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
            for token_type in token.TokenType:
                match: re.Match[str] | None = token_type.value.match(
                    file_line[local_position:],
                )
                if match:
                    new_token = token.Token(
                        token_type,
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
