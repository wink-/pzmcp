import re
from .base_parser import BaseParser

class VehicleParser(BaseParser):
    def __init__(self, script_content: str):
        super().__init__(script_content)
        self.lines = []
        self.current_line_idx = 0

    def _strip_block_comments(self, text: str) -> str:
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        return text

    def _normalize_line(self, line: str) -> str:
        line = line.split('--', 1)[0].split('//', 1)[0].strip()
        return line

    def _get_next_line(self):
        if self.current_line_idx < len(self.lines):
            line = self.lines[self.current_line_idx]
            self.current_line_idx += 1
            return line
        return None

    def _parse_block(self, block_terminator='}'):
        """Parses a generic block of key = value pairs or nested blocks."""
        data = {"properties": {}, "nested_blocks": {}} # Use nested_blocks for specific named blocks

        while True:
            line = self._get_next_line()
            if line is None or line == block_terminator:
                break # End of current block or file

            if not line: continue # Skip empty lines

            # Property: key = value
            prop_match = re.match(r'([\w\s./"-]+?)\s*=\s*(.+)', line)
            if prop_match:
                key = prop_match.group(1).strip()
                value = prop_match.group(2).strip().rstrip(',')

                # Unquote value if it's a quoted string
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                # TODO: Handle multi-value strings like "0 0.20 0" - currently stored as string
                data["properties"][key] = value
                continue

            # Nested block start: blockName {
            # More specific block names like 'part PartName {' are handled by callers
            block_start_match = re.match(r'(\w+)\s*{', line)
            if block_start_match:
                block_name = block_start_match.group(1)
                parsed_block_content = self._parse_block() # Recursive call

                # Store known nested blocks by name, others can go into a generic dict if needed
                if block_name in ["model", "sound", "lua", "container"] and block_name not in data: # Single blocks
                     data[block_name] = parsed_block_content
                elif block_name in ["skin", "part"]: # Blocks that can appear multiple times
                    if block_name not in data:
                        data[block_name] = []
                    # For 'part', the name is part of the definition, handled by _parse_vehicle_content
                    data[block_name].append(parsed_block_content)
                else: # Generic nested block storage
                    if "generic_nested" not in data: data["generic_nested"] = {}
                    if block_name not in data["generic_nested"]: data["generic_nested"][block_name] = []
                    data["generic_nested"][block_name].append(parsed_block_content)
                continue

        # Clean up return structure: if only properties, return that. If known blocks, return them.
        # This basic _parse_block might be too generic; specific parsers are better.
        # For now, let's simplify: it mostly parses properties. Callers handle specific blocks.
        return data["properties"]


    def _parse_vehicle_content(self, entity_data):
        """Parses content within a vehicle or template block."""
        # entity_data is the dict for the current vehicle/template
        entity_data.setdefault("properties", {})
        entity_data.setdefault("skins", [])
        entity_data.setdefault("parts", [])

        while True:
            line = self._get_next_line()
            if line is None or line == "}": # End of vehicle/template block
                break
            if not line: continue

            # model {? ... }
            if line.strip() == "model" or line.strip() == "model {":
                if '{' not in line:
                    brace_line = self._get_next_line()
                    if brace_line is None or brace_line.strip() != '{': continue # Error or unexpected
                entity_data["model"] = self._parse_block()
                continue

            # skin {? ... }
            if line.strip() == "skin" or line.strip() == "skin {":
                if '{' not in line:
                    brace_line = self._get_next_line()
                    if brace_line is None or brace_line.strip() != '{': continue # Error or unexpected
                entity_data["skins"].append(self._parse_block())
                continue

            # sound {? ... }
            if line.strip() == "sound" or line.strip() == "sound {":
                if '{' not in line:
                    brace_line = self._get_next_line()
                    if brace_line is None or brace_line.strip() != '{': continue # Error or unexpected
                entity_data["sound"] = self._parse_block()
                continue

            # part PartName {? ... } or part "Part Name" {? ... }
            part_match = re.match(r'part\s+(?:"([^"]+)"|([\w.]+))\s*{?', line)
            if part_match:
                if '{' not in line: # Check if brace was on the same line
                    brace_line = self._get_next_line()
                    if brace_line is None or brace_line.strip() != '{': continue # Error or unexpected
                part_name = part_match.group(1) or part_match.group(2)
                current_part = {"name": part_name.strip(), "properties": {}, "lua": None, "install": None, "uninstall": None, "container": None}
                self._parse_part_content(current_part)
                entity_data["parts"].append(current_part)
                continue

            # Direct properties of vehicle/template
            prop_match = re.match(r'([\w\s./"-]+?)\s*=\s*(.+)', line) # Keep this regex as is
            if prop_match:
                key = prop_match.group(1).strip()
                value = prop_match.group(2).strip().rstrip(',')
                if value.startswith('"') and value.endswith('"'): value = value[1:-1]
                entity_data["properties"][key] = value
                continue

    def _parse_part_content(self, part_data):
        """Parses content within a part block."""
        part_data.setdefault("properties", {})
        while True:
            line = self._get_next_line()
            if line is None or line == "}": # End of part block
                break
            if not line: continue

            if line.strip() == "lua" or line.strip() == "lua {":
                if '{' not in line:
                    brace_line = self._get_next_line()
                    if brace_line is None or brace_line.strip() != '{': continue
                part_data["lua"] = self._parse_block()
                continue

            if line.strip() == "table install" or line.strip() == "table install {":
                if '{' not in line: # The keyword is "table install"
                    brace_line = self._get_next_line()
                    if brace_line is None or brace_line.strip() != '{': continue
                part_data["install"] = self._parse_block()
                continue

            if line.strip() == "table uninstall" or line.strip() == "table uninstall {":
                if '{' not in line:
                    brace_line = self._get_next_line()
                    if brace_line is None or brace_line.strip() != '{': continue
                part_data["uninstall"] = self._parse_block()
                continue

            if line.strip() == "container" or line.strip() == "container {":
                if '{' not in line:
                    brace_line = self._get_next_line()
                    if brace_line is None or brace_line.strip() != '{': continue
                part_data["container"] = self._parse_block()
                continue

            # Direct properties of part
            prop_match = re.match(r'([\w\s./"-]+?)\s*=\s*(.+)', line) # Keep this regex as is
            if prop_match:
                key = prop_match.group(1).strip()
                value = prop_match.group(2).strip().rstrip(',')
                if value.startswith('"') and value.endswith('"'): value = value[1:-1]
                part_data["properties"][key] = value
                continue

    def parse(self):
        processed_content = self._strip_block_comments(self.script_content)
        self.lines = [self._normalize_line(l) for l in processed_content.splitlines()]
        self.current_line_idx = 0

        parsed_data = {
            "module": None,
            "vehicles": [],
            "templates": []
        }

        while True:
            line = self._get_next_line()
            if line is None: break # End of file
            if not line: continue # Skip empty lines

            # Module definition
            module_match = re.match(r"module\s+([\w.]+)\s*{?", line)
            if module_match:
                if parsed_data["module"] is None:
                    parsed_data["module"] = module_match.group(1)
                # Assuming module block doesn't need its own content parsing beyond containing vehicles/templates
                # If module has direct properties or other blocks, this needs adjustment.
                # For now, we just note the module name and continue parsing for vehicles/templates.
                # The module's '}' will be consumed naturally by the loop.
                continue

            # Vehicle definition: vehicle VehicleName {? or vehicle VehicleName : BaseVehicle {?
            vehicle_match = re.match(r'vehicle\s+([\w\.]+)(?:\s*:\s*([\w\.]+))?\s*{?', line)
            if vehicle_match:
                # Consume opening brace if it's on the next line
                if '{' not in line:
                    brace_line = self._get_next_line()
                    if brace_line is None or brace_line.strip() != '{':
                        # This is an error or unexpected format, skip this vehicle
                        continue
                vehicle_name = vehicle_match.group(1)
                inherits_from = vehicle_match.group(2)
                current_vehicle = {"name": vehicle_name, "inherits": inherits_from, "skins": [], "parts": []}
                self._parse_vehicle_content(current_vehicle)
                parsed_data["vehicles"].append(current_vehicle)
                continue

            # Template definition: template TemplateName {?
            template_match = re.match(r'template\s+([\w\.]+)\s*{?', line)
            if template_match:
                # Consume opening brace if it's on the next line
                if '{' not in line:
                    brace_line = self._get_next_line()
                    if brace_line is None or brace_line.strip() != '{':
                        # Error or unexpected format
                        continue
                template_name = template_match.group(1)
                current_template = {"name": template_name, "skins": [], "parts": []}
                # Templates can have similar content to vehicles (model, skin, parts, etc.)
                self._parse_vehicle_content(current_template) # Reuse vehicle content parser
                parsed_data["templates"].append(current_template)
                continue

        return parsed_data
