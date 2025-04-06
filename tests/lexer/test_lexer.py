from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from py_templating_engine import lexer, token


@pytest.mark.parametrize(
    argnames=[
        "test_file_string",
        "expected_token_list",
    ],
    argvalues=[
        pytest.param(
            "{{ templater.variable }}",
            [
                token.Token(
                    type=token.TokenType.OPEN_VARIABLE_BRACKETS,
                    text="{{",
                    position=0,
                ),
                token.Token(
                    type=token.TokenType.SPACE,
                    text=" ",
                    position=2,
                ),
                token.Token(
                    type=token.TokenType.VARIABLE,
                    text="templater.variable",
                    position=3,
                ),
                token.Token(
                    type=token.TokenType.SPACE,
                    text=" ",
                    position=21,
                ),
                token.Token(
                    type=token.TokenType.CLOSE_VARIABLE_BRACKETS,
                    text="}}",
                    position=22,
                ),
            ],
            id="one-simple-variable-in-brackets",
        ),
        pytest.param(
            "{{templater.variable}}",
            [
                token.Token(
                    type=token.TokenType.OPEN_VARIABLE_BRACKETS,
                    text="{{",
                    position=0,
                ),
                token.Token(
                    type=token.TokenType.VARIABLE,
                    text="templater.variable",
                    position=2,
                ),
                token.Token(
                    type=token.TokenType.CLOSE_VARIABLE_BRACKETS,
                    text="}}",
                    position=20,
                ),
            ],
            id="one-simple-variable-without-spaces-in-brackets",
        ),
        pytest.param(
            "{{      templater.variable  }}",
            [
                token.Token(
                    type=token.TokenType.OPEN_VARIABLE_BRACKETS,
                    text="{{",
                    position=0,
                ),
                token.Token(
                    type=token.TokenType.SPACE,
                    text="      ",
                    position=2,
                ),
                token.Token(
                    type=token.TokenType.VARIABLE,
                    text="templater.variable",
                    position=8,
                ),
                token.Token(
                    type=token.TokenType.SPACE,
                    text="  ",
                    position=26,
                ),
                token.Token(
                    type=token.TokenType.CLOSE_VARIABLE_BRACKETS,
                    text="}}",
                    position=28,
                ),
            ],
            id="one-simple-variable-with-different-spaces-in-brackets",
        ),
    ],
)
def test_fill_token_list(
    test_file_string: str,
    expected_token_list: list[token.Token],
    lexer_instance: lexer.Lexer,
):
    """Test fill token list works correctly."""
    lexer_instance.fill_token_list(test_file_string)

    assert lexer_instance.token_list == expected_token_list


def test_lexical_analysis_with_valid_file(template_file: Path):
    """Test lexical analysis process template file correctly."""
    lexer_instance = lexer.Lexer(template_file)

    tokens_list = lexer_instance.lexical_analysis()

    assert tokens_list


def test_lexical_analysis_unexisted_file():
    """Test lexical analysis handle unexisted file."""
    file_name = "non_existed_file.txt"
    lexer_instance = lexer.Lexer(Path("non_existed_file.txt"))

    with pytest.raises(
        FileNotFoundError,
        match=f"File not found: {file_name}",
    ):
        lexer_instance.lexical_analysis()


def test_lexical_analysis_os_error(mocker: MockerFixture):
    """Test lexical analysis handle os error."""
    mocker.patch.object(Path, "open", side_effect=OSError("Mocked error"))
    lexer_instance = lexer.Lexer(Path("some_file.txt"))

    with pytest.raises(
        RuntimeError,
        match="Error reading file some_file.txt: Mocked error",
    ):
        lexer_instance.lexical_analysis()
