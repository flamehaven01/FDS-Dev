from abc import ABC, abstractmethod
from dataclasses import dataclass
import re
from pathlib import Path
from typing import List, Optional
from urllib.parse import urldefrag

import requests

from fds_dev.parser import Document, Header

@dataclass
class LintError:
    line_number: int
    message: str
    rule_name: str

class BaseRule(ABC):
    """
    The base class for all linting rules.
    """
    def __init__(self, config):
        self.config = config

    @property
    def name(self) -> str:
        # Generates a rule name from the class name, e.g., RequireLicenseSection -> require-license-section
        return ''.join(['-' + i.lower() if i.isupper() else i for i in self.__class__.__name__]).lstrip('-')

    @abstractmethod
    def apply(self, doc: Document) -> List[LintError]:
        """
        Applies the rule to a document and returns a list of errors.
        An empty list means the rule passed.
        """
        pass

# --- Example Rule Implementations ---

class RequireSectionLicense(BaseRule):
    """
    Checks if a 'License' section exists in the document.
    A 'License' section is identified by a header containing the word "License".
    """
    def apply(self, doc: Document) -> List[LintError]:
        found_license = False
        for header in doc.headers:
            if "license" in header.text.lower():
                found_license = True
                break
        
        if not found_license:
            # Report error at line 1 if the section is missing entirely.
            return [LintError(line_number=1, message="Document is missing a 'License' section.", rule_name=self.name)]
        
        return []

class SectionOrder(BaseRule):
    """
    Checks if top-level sections appear in a predefined order.
    The order is defined in the '.fdsrc.yaml' config file.
    """
    def apply(self, doc: Document) -> List[LintError]:
        errors: List[LintError] = []
        expected_order: Optional[List[str]] = self.config.get('order')

        if not expected_order:
            return [] # No order defined, so nothing to check.

        # Get only top-level (h1 or h2) headers from the document
        top_level_headers = [h for h in doc.headers if h.level <= 2]
        
        last_found_index = -1
        
        for header in top_level_headers:
            try:
                # Find the current header's text in the expected order list
                current_index = -1
                for i, expected_text in enumerate(expected_order):
                    if expected_text.lower() in header.text.lower():
                        current_index = i
                        break

                if current_index != -1:
                    if current_index < last_found_index:
                        expected_section = expected_order[last_found_index]
                        line_number = max(1, header.line_number - 1)
                        errors.append(LintError(
                            line_number=line_number,
                            message=f"Section '{header.text}' appears out of order. It should not come before '{expected_section}'.",
                            rule_name=self.name
                        ))
                    last_found_index = max(last_found_index, current_index)

            except ValueError:
                # This header is not in our defined order, so we ignore it.
                pass
        
        return errors

class BrokenLinkCheckRule(BaseRule):
    """
    Validates internal anchors, relative file references, and (optionally) external URLs.
    """
    def __init__(self, config):
        super().__init__(config or {})
        self.check_external = self.config.get("check_external", False)
        self.timeout = float(self.config.get("timeout", 3.0))
        self.allowed_statuses = set(self.config.get("allowed_statuses", [200, 201, 202, 203, 204, 205, 301, 302, 303, 307, 308]))

    def apply(self, doc: Document) -> List[LintError]:
        errors: List[LintError] = []
        if not doc.links:
            return errors

        anchor_index = self._build_anchor_index(doc.headers)
        base_dir = Path(doc.path).parent

        for link in doc.links:
            if link.kind == "anchor":
                if not self._anchor_exists(link.target, anchor_index):
                    errors.append(
                        LintError(
                            line_number=link.line_number,
                            message=f"Broken anchor link: '{link.target}' does not match any heading.",
                            rule_name=self.name,
                        )
                    )
            elif link.kind == "file":
                if not self._file_exists(base_dir, link.target):
                    errors.append(
                        LintError(
                            line_number=link.line_number,
                            message=f"Broken file link: '{link.target}' does not exist.",
                            rule_name=self.name,
                        )
                    )
            elif link.kind == "external":
                if self.check_external and not self._external_ok(link.target):
                    errors.append(
                        LintError(
                            line_number=link.line_number,
                            message=f"Broken external link: '{link.target}' is unreachable.",
                            rule_name=self.name,
                        )
                    )
        return errors

    @staticmethod
    def _build_anchor_index(headers: List[Header]) -> set:
        slugs = {BrokenLinkCheckRule._slugify(header.text) for header in headers}
        return slugs

    @staticmethod
    def _anchor_exists(target: str, slug_index: set) -> bool:
        anchor = target.lstrip("#")
        slug = BrokenLinkCheckRule._slugify(anchor)
        return slug in slug_index

    @staticmethod
    def _file_exists(base_dir: Path, target: str) -> bool:
        file_target, _ = urldefrag(target)
        if not file_target:
            return True
        resolved = (base_dir / file_target).resolve()
        return resolved.exists()

    def _external_ok(self, url: str) -> bool:
        try:
            response = requests.head(url, allow_redirects=True, timeout=self.timeout)
            if response.status_code in self.allowed_statuses:
                return True
            if response.status_code >= 400:
                response = requests.get(url, allow_redirects=True, timeout=self.timeout)
                return response.status_code in self.allowed_statuses
            return True
        except requests.RequestException:
            return False

    @staticmethod
    def _slugify(value: str) -> str:
        value = value.strip().lower()
        value = re.sub(r"[^\w\- ]", "", value)
        value = value.replace(" ", "-")
        return value
