from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import List, Union

@dataclass
class Header:
    level: int
    text: str
    line_number: int

@dataclass
class Document:
    path: Union[str, Path]
    content: str
    lines: List[str] = field(init=False)
    headers: List[Header] = field(default_factory=list)

    def __post_init__(self):
        self.lines = self.content.splitlines()
        if self.content == "":
            self.lines = [""]

class MarkdownParser:
    """
    A simple parser to extract structural elements from a Markdown file.
    """
    def __init__(self):
        # Regex to find ATX-style headers (#, ##, etc.) with optional leading spaces
        self.header_regex = re.compile(r"^\s*(#{1,6})\s+(.*\S.*)$")

    def parse(self, file_path: Union[str, Path]) -> Document:
        """
        Parses a Markdown file and returns a Document object.
        """
        path = Path(file_path)
        content = path.read_text(encoding='utf-8')
        return self.parse_content(content, path=path)

    def parse_content(self, content: str, path: Union[str, Path] = "<memory>") -> Document:
        """Parse Markdown content provided as a string."""
        doc = Document(path=path, content=content)
        self._extract_headers(doc)
        return doc

    def _extract_headers(self, doc: Document) -> None:
        for i, line in enumerate(doc.lines):
            header_match = self.header_regex.match(line)
            if header_match:
                level = len(header_match.group(1))
                text = header_match.group(2).strip()
                doc.headers.append(Header(level=level, text=text, line_number=i + 1))

if __name__ == '__main__':
    # Example usage:
    parser = MarkdownParser()
    try:
        doc = parser.parse('README.md')
        print(f"Parsed {doc.path}:")
        for header in doc.headers:
            print(f"  - L{header.line_number}: {'  ' * (header.level - 1)}[{header.level}] {header.text}")
    except FileNotFoundError:
        print("README.md not found. Create one to test the parser.")

