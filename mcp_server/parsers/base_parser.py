class BaseParser:
    def __init__(self, script_content: str):
        self.script_content = script_content
        self.lines = script_content.splitlines()

    def parse(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def _strip_comments(self, line: str) -> str:
        """Removes comments from a line."""
        # Remove block comments first (/** ... */ or /* ... */)
        line = re.sub(r'/\*.*?\*/', '', line)
        # Remove single-line comments (// or --)
        line = line.split('--', 1)[0].split('//', 1)[0].strip()
        return line

    def _normalize_line(self, line: str) -> str:
        """Normalizes a line by stripping comments and whitespace."""
        return self._strip_comments(line).strip()
