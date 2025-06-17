import re
from .base_parser import BaseParser

class RecipeParser(BaseParser):
    def __init__(self, script_content: str):
        super().__init__(script_content)

    def parse(self):
        parsed_data = {
            "module": None,
            "recipes": []
        }

        processed_script_content = self._strip_block_comments(self.script_content)
        lines = processed_script_content.splitlines()

        current_recipe_data = None
        in_recipe_block = False
        parsing_inputs = False # Flag to differentiate between input items and properties

        for raw_line in lines:
            normalized_line = self._normalize_line(raw_line) # Handles single-line comments

            if not normalized_line: # Blank line or comment-only line
                # If it's a blank line (not just a stripped comment) and we are parsing inputs, it signifies end of inputs.
                if raw_line.strip() == "" and in_recipe_block and parsing_inputs:
                    parsing_inputs = False
                continue # Skip blank lines and comment-only lines

            line = normalized_line # Use the normalized line for actual parsing logic

            # Module definition
            module_match = re.match(r"module\s+([\w.]+)\s*{?", line)
            if module_match:
                if parsed_data["module"] is None:
                    parsed_data["module"] = module_match.group(1)
                continue

            # Recipe definition
            # recipe "Recipe Name" { or recipe RecipeName {
            recipe_match = re.match(r'recipe\s+(?:"([^"]+)"|([\w\s]+))\s*{?', line)
            if recipe_match:
                recipe_name = recipe_match.group(1) or recipe_match.group(2) # Quoted or unquoted
                current_recipe_data = {
                    "name": recipe_name.strip(),
                    "inputs": [],
                    "properties": {},
                    "result": None
                }
                parsed_data["recipes"].append(current_recipe_data)
                in_recipe_block = True
                parsing_inputs = True # Start by parsing inputs
                if '{' in line:
                    pass # Brace on same line
                continue

            if not in_recipe_block or current_recipe_data is None:
                continue

            # End of recipe block
            if line == "}":
                in_recipe_block = False
                parsing_inputs = False
                current_recipe_data = None
                continue

            # Inside a recipe block
            if parsing_inputs:
                # Check if it's a property line (contains ':'), means inputs are done
                if ':' in line:
                    parsing_inputs = False
                    # Reprocess this line as a property
                else:
                    input_item = self._parse_input_item(line)
                    if input_item:
                        current_recipe_data["inputs"].append(input_item)
                    continue # Continue to next line for more inputs or blank line

            # If not parsing inputs (or switched from inputs to properties)
            if not parsing_inputs:
                prop_match = re.match(r"([\w\s./]+)\s*:\s*(.+)", line)
                if prop_match:
                    prop_name = prop_match.group(1).strip()
                    prop_value = prop_match.group(2).strip()

                    if prop_name.lower() == "result":
                        current_recipe_data["result"] = self._parse_result(prop_value)
                    else:
                        # Further parse specific known properties if needed (e.g., SkillRequired)
                        # For now, store as string
                        current_recipe_data["properties"][prop_name] = self._attempt_type_conversion(prop_value)
                # else: might be a malformed line or comment already stripped

        return parsed_data

    def _parse_input_item(self, line: str):
        """Parses a single input item line."""
        line = self._normalize_line(line)
        if not line:
            return None

        # Remove trailing comma from the original normalized line first
        line = line.rstrip(',')

        item_data = {"item": None, "keep": False, "alternatives": [], "quantity": None}

        # Check for 'keep'
        if line.lower().startswith("keep "):
            item_data["keep"] = True
            line = line[5:].strip()
            # Trailing comma for keep line might be after item name, e.g. "keep Item,"
            line = line.rstrip(',')


        # Check for quantity (e.g., Item=3) first, as item name might have spaces
        quantity_match = re.match(r"(.+?)\s*=\s*(\d+)$", line)
        if quantity_match:
            line = quantity_match.group(1).strip()
            item_data["quantity"] = int(quantity_match.group(2))

        # Check for alternatives
        # Try splitting by ' / ' (space-padded slash) first for structure like "Item A" / AltB
        space_slash_parts = re.split(r'\s+/\s+', line, maxsplit=1)
        if len(space_slash_parts) > 1: # Successfully split by ' / '
            item_data["item"] = space_slash_parts[0].strip()
            # The alternative part might be a chain like AltB/AltC
            item_data["alternatives"] = [alt.strip().rstrip(',') for alt in space_slash_parts[1].strip().split('/')]
        else: # No ' / ' found (or it's at an edge). Fall back to simple '/' split for ItemA/AltB cases.
            simple_slash_parts = line.split('/')
            item_data["item"] = simple_slash_parts[0].strip()
            if len(simple_slash_parts) > 1:
                item_data["alternatives"] = [alt.strip().rstrip(',') for alt in simple_slash_parts[1:]]

        # Decision: Keep quotes around item names and alternatives if they were originally quoted.
        # The tests (specifically test_input_item_edge_cases) expect quoted names to remain quoted.
        # Unquoting can be a separate step later if needed (e.g. when converting to Pydantic models).

        if not item_data["item"]:
            return None

        return item_data

    def _parse_result(self, result_str: str):
        """Parses the Result:Item=quantity string."""
        result_str = result_str.rstrip(',') # Remove trailing comma
        match = re.match(r"([\w\s.]+)(?:=(\d+))?", result_str)
        if match:
            item_name = match.group(1).strip()
            quantity_str = match.group(2)
            return {
                "item": item_name,
                "quantity": int(quantity_str) if quantity_str else 1
            }
        return {"item": result_str, "quantity": 1}

    def _attempt_type_conversion(self, value_str: str):
        """Attempts to convert a string value to bool, int, or float."""
        value_str = value_str.rstrip(',') # Remove trailing comma before type conversion

        if value_str.lower() == "true":
            return True
        if value_str.lower() == "false":
            return False
        if re.match(r"^\d+$", value_str):
            return int(value_str)
        if re.match(r"^\d+\.\d+$", value_str):
            return float(value_str)
        if value_str.startswith('"') and value_str.endswith('"'):
             return value_str[1:-1]
        return value_str


    def _strip_block_comments(self, text: str) -> str:
        """Removes /* ... */ and /** ... */ style block comments from the entire script content."""
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        return text

    def _normalize_line(self, line: str) -> str:
        """Normalizes a line by stripping single-line comments (//, --) and whitespace."""
        line = line.split('--', 1)[0].split('//', 1)[0].strip()
        return line
