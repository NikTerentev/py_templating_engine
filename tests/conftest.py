import pytest


@pytest.fixture
def template_file(tmp_path):
    """Test template file with small content."""
    content = "{{ templater.variable }}"
    template_file = tmp_path / "template_file.txt"
    template_file.write_text(content)
    return template_file
