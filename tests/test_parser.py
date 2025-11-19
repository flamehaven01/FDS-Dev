import os
import pytest
from fds_dev.parser import MarkdownParser

@pytest.fixture
def create_test_markdown_file(tmp_path):
    """A pytest fixture to create a temporary markdown file for testing."""
    def _create_file(content):
        file_path = tmp_path / "test.md"
        file_path.write_text(content, encoding="utf-8")
        return file_path
    return _create_file

def test_parse_empty_file(create_test_markdown_file):
    file_path = create_test_markdown_file("")
    parser = MarkdownParser()
    doc = parser.parse(file_path)
    assert doc.content == ""
    assert doc.headers == []
    assert doc.lines == [''] # splitlines on empty string returns ['']

def test_parse_headers(create_test_markdown_file):
    content = (
        "# Title\n"
        "Some text.\n"
        "## Subtitle 1\n"
        "### Deeper Title\n"
        "Another line.\n"
        "## Subtitle 2"
    )
    file_path = create_test_markdown_file(content)
    parser = MarkdownParser()
    doc = parser.parse(file_path)
    
    assert len(doc.headers) == 4
    
    assert doc.headers[0].level == 1
    assert doc.headers[0].text == "Title"
    assert doc.headers[0].line_number == 1
    
    assert doc.headers[1].level == 2
    assert doc.headers[1].text == "Subtitle 1"
    assert doc.headers[1].line_number == 3

    assert doc.headers[2].level == 3
    assert doc.headers[2].text == "Deeper Title"
    assert doc.headers[2].line_number == 4

    assert doc.headers[3].level == 2
    assert doc.headers[3].text == "Subtitle 2"
    assert doc.headers[3].line_number == 6

def test_header_with_extra_whitespace(create_test_markdown_file):
    content = "  ##    Spaced Out Header   "
    file_path = create_test_markdown_file(content)
    parser = MarkdownParser()
    doc = parser.parse(file_path)

    assert len(doc.headers) == 1
    assert doc.headers[0].level == 2
    assert doc.headers[0].text == "Spaced Out Header"

def test_line_without_header(create_test_markdown_file):
    content = "This is not a header."
    file_path = create_test_markdown_file(content)
    parser = MarkdownParser()
    doc = parser.parse(file_path)
    assert len(doc.headers) == 0

def test_file_not_found():
    parser = MarkdownParser()
    with pytest.raises(FileNotFoundError):
        parser.parse("non_existent_file.md")
