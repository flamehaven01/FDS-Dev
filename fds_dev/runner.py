import hashlib
import yaml
from typing import List, Dict, Any, Tuple, Optional

from fds_dev.parser import Document, MarkdownParser
from fds_dev.rules import BaseRule, LintError, RequireSectionLicense, SectionOrder, BrokenLinkCheckRule

# A mapping from rule names in the config to their class implementations.
AVAILABLE_RULES = {
    "require-section-license": RequireSectionLicense,
    "section-order": SectionOrder,
    "broken-link-check": BrokenLinkCheckRule,
}

def _get_file_hash(file_path: str) -> str:
    """Computes the SHA256 hash of a file's content."""
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

class LintRunner:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.rules = self._initialize_rules()
        self.parser = MarkdownParser()

    def _initialize_rules(self) -> List[BaseRule]:
        initialized_rules = []
        rules_config = self.config.get('rules', {})
        
        for name, config_value in rules_config.items():
            if name not in AVAILABLE_RULES:
                continue

            if config_value in ('off', False, None):
                continue

            if config_value in ('on', True):
                rule_config = {}
            elif isinstance(config_value, dict):
                enabled = config_value.get('enabled', True)
                if not enabled:
                    continue
                rule_config = {k: v for k, v in config_value.items() if k != 'enabled'}
            else:
                continue

            rule_instance = AVAILABLE_RULES[name](rule_config)
            initialized_rules.append(rule_instance)
        return initialized_rules

    def run(self, file_path: str, cache: Dict[str, Any]) -> Tuple[str, Optional[str], List[LintError]]:
        """
        Runs all initialized rules against a single file, utilizing a cache.
        Returns the file path, its content hash, and a list of errors.
        """
        try:
            file_hash = _get_file_hash(file_path)
            
            # Check cache
            if file_path in cache and cache[file_path].get('hash') == file_hash:
                # Return cached errors, converting them back to LintError objects
                cached_errors_data = cache[file_path].get('errors', [])
                cached_errors = [LintError(**data) for data in cached_errors_data]
                return file_path, file_hash, cached_errors

            # If not in cache or hash mismatch, run linting
            all_errors: List[LintError] = []
            document = self.parser.parse(file_path)
            
            for rule in self.rules:
                errors = rule.apply(document)
                all_errors.extend(errors)
            
            return file_path, file_hash, all_errors
                
        except FileNotFoundError:
            return file_path, None, [LintError(line_number=0, message=f"File not found: {file_path}", rule_name="runner")]
        except Exception as e:
            return file_path, None, [LintError(line_number=0, message=f"An unexpected error occurred: {e}", rule_name="runner")]
