from dataclasses import dataclass, field
import re
from typing import List

@dataclass
class Header:
    level: int
    text: str
    line_number: int

@dataclass
class Document:
    path: str
    content: str
    lines: List[str] = field(init=False)
    headers: List[Header] = field(default_factory=list)

    def __post_init__(self):
        self.lines = self.content.splitlines()

class MarkdownParser:
    """
    A simple parser to extract structural elements from a Markdown file.
    """
    def __init__(self):
        # Regex to find ATX-style headers (#, ##, etc.)
        self.header_regex = re.compile(r"^(#{1,6})\s+(.*)")

    def parse(self, file_path: str) -> Document:
        """
        Parses a Markdown file and returns a Document object.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        doc = Document(path=file_path, content=content)
        
        for i, line in enumerate(doc.lines):
            header_match = self.header_regex.match(line)
            if header_match:
                level = len(header_match.group(1))
                text = header_match.group(2).strip()
                doc.headers.append(Header(level=level, text=text, line_number=i + 1))
        
        return doc

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

