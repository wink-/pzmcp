import re
from .base_parser import BaseParser

class ItemParser(BaseParser):
    def __init__(self, script_content: str):
        super().__init__(script_content)

    def parse(self):
        """
        Parses the script content to identify the module, imports, items, and their properties.
        Returns a structured dictionary.
        """
        parsed_data = {
            "module": None,
            "imports": [],
            "items": []
        }

        # Process the whole script content at once for multiline comments
        processed_script_content = self._strip_block_comments(self.script_content)
        lines = processed_script_content.splitlines()

        current_item = None
        in_imports_block = False

        for line_number, raw_line in enumerate(lines):
            line = self._normalize_line(raw_line) # _normalize_line now handles single-line comments

            if not line:
                continue

            # Module definition
            module_match = re.match(r"module\s+([\w.]+)\s*{?", line) # Optional { at end of line
            if module_match:
                if parsed_data["module"] is None: # Only capture the first module definition
                    parsed_data["module"] = module_match.group(1)
                # If { is on the same line, we are inside the module
                if '{' in line:
                    pass # Handled by brace counting or next lines
                continue

            # Imports block start
            if line == "imports {" or line == "imports":
                in_imports_block = True
                continue

            # Inside imports block
            if in_imports_block:
                if line == "}":
                    in_imports_block = False
                    continue
                # Assuming import names are single words/identifiers
                import_match = re.match(r"([\w.]+)", line)
                if import_match:
                    parsed_data["imports"].append(import_match.group(1))
                continue

            # Item definition
            item_match = re.match(r"item\s+(\w+)\s*{?", line) # Optional { at end of line
            if item_match:
                item_name = item_match.group(1)
                current_item = {"name": item_name, "properties": {}}
                parsed_data["items"].append(current_item)
                if '{' in line:
                    pass # Handled by brace counting or next lines
                continue

            # Property definition
            # Matches: PropertyName = Value, or PropertyName = "Value with spaces",
            # or PropertyName = 123, or PropertyName = 12.3, or PropertyName = true,
            prop_match = re.match(r"([\w\s]+)\s*=\s*(.+?),?\s*$", line)
            if prop_match and current_item:
                prop_name = prop_match.group(1).strip()
                prop_value_str = prop_match.group(2).strip().rstrip(',')

                # Attempt to convert value to a more specific type
                if prop_value_str.lower() == "true":
                    prop_value = True
                elif prop_value_str.lower() == "false":
                    prop_value = False
                elif re.match(r"^\d+$", prop_value_str):
                    prop_value = int(prop_value_str)
                elif re.match(r"^\d+\.\d+$", prop_value_str):
                    prop_value = float(prop_value_str)
                elif prop_value_str.startswith('"') and prop_value_str.endswith('"'):
                    prop_value = prop_value_str[1:-1] # Strip quotes
                else:
                    prop_value = prop_value_str # Keep as string if no other type matches

                current_item["properties"][prop_name] = prop_value
                continue

            # End of item block (if explicit and not handled by module end)
            if line == "}" and current_item:
                current_item = None # Exiting current item scope
                continue

            # End of module block (can also implicitly end an item)
            # This assumes one module per file, or that we only care about the first one's structure
            if line == "}" and not current_item and parsed_data["module"] is not None:
                # Potentially signifies end of module if not within any other block
                pass # Module scope closure is implicitly handled by end of file or next module

        # If no module was found, but there are items, this indicates a potential parsing issue
        # or a script format not strictly adhering to module > item structure.
        # For now, if items were found but no module, we keep them.
        # If no module and no items, return the empty structure.

        return parsed_data

    def _strip_block_comments(self, text: str) -> str:
        """Removes /* ... */ and /** ... */ style block comments from the entire script content."""
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        return text

    def _normalize_line(self, line: str) -> str:
        """Normalizes a line by stripping single-line comments and whitespace."""
        # This version of _normalize_line is specific to ItemParser and expects block comments to be pre-processed.
        # It only handles // and -- style comments.
        line = line.split('--', 1)[0].split('//', 1)[0].strip()
        return line
