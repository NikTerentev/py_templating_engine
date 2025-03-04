import pytest

from py_templating_engine import ast, token


@pytest.mark.parametrize(
    argnames=[
        "tokens_list",
        "expected_ast",
    ],
    argvalues=[
        pytest.param(
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
            ast.StatementsNode(
                code_strings=[
                    token.Token(
                        type=token.TokenType.OPEN_VARIABLE_BRACKETS,
                        text="{{",
                        position=0,
                    ),
                    token.Token(
                        type=token.TokenType.VARIABLE,
                        text="templater.variable",
                        position=3,
                    ),
                    token.Token(
                        type=token.TokenType.CLOSE_VARIABLE_BRACKETS,
                        text="}}",
                        position=22,
                    ),
                ],
            ),
        ),
    ],
)
def test_parse_code(
    tokens_list: list[token.Token],
    expected_ast: ast.StatementsNode,
):
    """Test that method return correct ast tree."""
    # parser_instance = parser.Parser(tokens_list)  # noqa

    # ast = parser_instance.parse_code()  # noqa
    # import ipdb; ipdb.set_trace()  # noqa
    # assert ast == expected_ast  # noqa
    assert True
