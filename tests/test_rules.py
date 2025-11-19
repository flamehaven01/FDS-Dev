import pytest
from fds_dev.parser import Document
from fds_dev.rules import RequireSectionLicense, SectionOrder

@pytest.fixture
def create_doc():
    """A pytest fixture to create a Document object for testing rules."""
    def _create(content: str):
        # Simplified parser logic for tests
        doc = Document(path="test.md", content=content)
        
        from fds_dev.parser import MarkdownParser
        parser = MarkdownParser()
        # Re-parse to get headers correctly
        return parser.parse(doc.path) if hasattr(doc, 'content') else doc
    
    # A bit of a hack to make the test fixture work with file content directly
    def _create_from_content(content: str):
        doc = Document(path="test.md", content=content)
        # Manually parse headers for the test document
        from fds_dev.parser import MarkdownParser
        parser = MarkdownParser()
        doc.headers = parser.parse_content(content).headers
        return doc

    def _create_from_content_with_manual_headers(content, headers):
        doc = Document(path="test.md", content=content, headers=headers)
        return doc
        
    return _create_from_content_with_manual_headers

@pytest.fixture
def create_doc_from_file(tmp_path):
    """Fixture to create a real file and then a Document object."""
    def _create_and_parse(content):
        file_path = tmp_path / "test.md"
        file_path.write_text(content, encoding="utf-8")
        
        from fds_dev.parser import MarkdownParser
        parser = MarkdownParser()
        return parser.parse(file_path)
    return _create_and_parse


# --- Tests for RequireSectionLicense Rule ---

def test_license_section_exists(create_doc_from_file):
    content = "# Project\n\n## License\n\nMIT License."
    doc = create_doc_from_file(content)
    rule = RequireSectionLicense(config={})
    errors = rule.apply(doc)
    assert len(errors) == 0

def test_license_section_missing(create_doc_from_file):
    content = "# Project\n\n## Contribution\n\nContribute here."
    doc = create_doc_from_file(content)
    rule = RequireSectionLicense(config={})
    errors = rule.apply(doc)
    assert len(errors) == 1
    assert errors[0].rule_name == "require-section-license"
    assert "missing a 'License' section" in errors[0].message

def test_license_section_case_insensitive(create_doc_from_file):
    content = "# Project\n\n## LICENSE\n\nMIT License."
    doc = create_doc_from_file(content)
    rule = RequireSectionLicense(config={})
    errors = rule.apply(doc)
    assert len(errors) == 0

# --- Tests for SectionOrder Rule ---

@pytest.fixture
def section_order_rule():
    config = {
        'order': [
            'About',
            'Installation',
            'Usage',
            'License'
        ]
    }
    return SectionOrder(config=config)

def test_section_order_correct(section_order_rule, create_doc_from_file):
    content = (
        "# About\nText.\n"
        "## Installation\nText.\n"
        "### Usage\nText.\n" # Deeper level, should still be detected
        "## License\nText."
    )
    doc = create_doc_from_file(content)
    errors = section_order_rule.apply(doc)
    assert len(errors) == 0

def test_section_order_incorrect(section_order_rule, create_doc_from_file):
    content = (
        "# About\nText.\n"
        "## License\nText.\n" # License before Installation
        "## Installation\nText."
    )
    doc = create_doc_from_file(content)
    errors = section_order_rule.apply(doc)
    assert len(errors) == 1
    assert errors[0].rule_name == "section-order"
    assert "'Installation' appears out of order" in errors[0].message
    assert "not come before 'License'" in errors[0].message
    assert errors[0].line_number == 4 # Line number of "## Installation"

def test_section_order_with_missing_sections(section_order_rule, create_doc_from_file):
    content = (
        "# About\nText.\n"
        "## Usage\nText.\n" # Installation is missing, which is fine
        "## License\nText."
    )
    doc = create_doc_from_file(content)
    errors = section_order_rule.apply(doc)
    assert len(errors) == 0

def test_section_order_with_unlisted_sections(section_order_rule, create_doc_from_file):
    content = (
        "# About\nText.\n"
        "## Unlisted Section\nText.\n" # This should be ignored
        "## Installation\nText."
    )
    doc = create_doc_from_file(content)
    errors = section_order_rule.apply(doc)
    assert len(errors) == 0

def test_section_order_no_config(create_doc_from_file):
    rule = SectionOrder(config={}) # No 'order' key in config
    content = "## B\n## A"
    doc = create_doc_from_file(content)
    errors = rule.apply(doc)
    assert len(errors) == 0, "Rule should do nothing if order is not configured"
