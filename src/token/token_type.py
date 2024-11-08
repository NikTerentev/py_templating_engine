from dataclasses import dataclass


@dataclass
class TokenType:
    name: str
    regex: str


token_types_list = {
    "OPEN_VARIABLE_BRACKETS": TokenType("OPEN_VARIABLE_BRACKETS", "{{"),
    "CLOSE_VARIABLE_BRACKETS": TokenType("CLOSE_VARIABLE_BRACKETS", "}}"),
    "SPACE": TokenType("SPACE", r"[ \t\r\n]+"),
    "VARIABLE": TokenType("VARIABLE", r"(templater\.\S+?)(?=}}|\s)"),
    "CODE": TokenType("CODE", r"(\S+?)(?={{|\s|$)")
}
