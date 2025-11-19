from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from fds_dev.parser import Document

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
                        line_number = header.line_number
                        if line_number > 1:
                            # Point to the line separating sections for easier context.
                            line_number -= 1

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
