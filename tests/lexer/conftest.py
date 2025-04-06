import pytest
from py_templating_engine import lexer


@pytest.fixture
def lexer_instance(tmp_path):
    """Return test lexer instance."""
    return lexer.Lexer(tmp_path)
