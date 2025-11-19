from dataclasses import dataclass, field
import re
from typing import List

@dataclass
class Header:
    level: int
    text: str
    line_number: int

@dataclass
class Link:
    text: str
    target: str
    line_number: int
    kind: str

@dataclass
class Document:
    path: str
    content: str
    lines: List[str] = field(init=False)
    headers: List[Header] = field(default_factory=list)
    links: List[Link] = field(default_factory=list)

    def __post_init__(self):
        self.lines = self.content.splitlines()
        if self.content == "":
            self.lines = [""]

class MarkdownParser:
    """
    A simple parser to extract structural elements from a Markdown file.
    """
    def __init__(self):
        self.header_regex = re.compile(r"^\s*(#{1,6})\s+(.*)")
        self.link_regex = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

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

        doc.links = self._extract_links(doc.lines)
        
        return doc

    def _extract_links(self, lines: List[str]) -> List[Link]:
        links: List[Link] = []
        for line_number, line in enumerate(lines, start=1):
            for match in self.link_regex.finditer(line):
                text = match.group(1).strip()
                target = match.group(2).strip()
                kind = self._classify_link(target)
                links.append(Link(text=text, target=target, line_number=line_number, kind=kind))
        return links

    @staticmethod
    def _classify_link(target: str) -> str:
        lowered = target.lower()
        if lowered.startswith(("http://", "https://", "mailto:")):
            return "external"
        if lowered.startswith("#"):
            return "anchor"
        return "file"

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

