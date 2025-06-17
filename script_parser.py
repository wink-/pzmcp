import re
import logging # Added logging
from typing import Dict, List, Optional, Any

# Setup logger for this module
logger = logging.getLogger(__name__)

# Define custom exception at the module level
class CustomParserSyntaxError(Exception):
    pass

class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, {self.line})"

TOKEN_SPECIFICATION = [
    ('BLOCK_COMMENT', r'/\*.*?\*/'), # Block comments /* ... */
    ('LINE_COMMENT', r'//.*?$|\#.*?$'),  # Line comments // or #
    ('STRING', r'"(?:\\.|[^"\\])*"'),  # String literals
    ('NUMBER', r'-?\d+(\.\d*)?'),  # Integer or decimal numbers, allowing negative
    # Identifier: starts with optional hyphen, then letter/underscore, then letters/numbers/underscores.
    # Optionally allows '.' for qualified names like Base.ItemName, but not at start/end of dot.
    # Allows identifiers like "-fluid".
    ('IDENTIFIER', r'[-]?[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*'),
    ('LBRACE', r'\{'),  # Left brace
    ('RBRACE', r'\}'),  # Right brace
    ('EQUALS', r'='),  # Equals sign
    ('COMMA', r','),  # Comma
    ('SEMICOLON', r';'),  # Semicolon
    ('LBRACKET', r'\['), # Left bracket
    ('RBRACKET', r'\]'), # Right bracket
    ('COLON', r':'),    # Colon
    ('NEWLINE', r'\n'),  # Line endings
    ('SKIP', r'[ \t]+'),  # Skip spaces and tabs
    ('MISMATCH', r'.'),  # Any other character (this should be last)
]

TOKEN_REGEX = re.compile('|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION), re.MULTILINE | re.DOTALL)

def tokenize(script_content: str) -> list[Token]:
    tokens = []
    line_num = 1
    line_start = 0
    for mo in TOKEN_REGEX.finditer(script_content):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start # column of token start

        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            tokens.append(Token(kind, value, line_num -1)) # Newline token refers to the line it ends
        elif kind == 'SKIP' or kind == 'LINE_COMMENT' or kind == 'BLOCK_COMMENT':
            if kind == 'BLOCK_COMMENT':
                line_num += value.count('\n')
                if '\n' in value:
                    line_start = mo.start() + value.rfind('\n') + 1
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character {value!r} on line {line_num} column {column+1}')
        else:
            tokens.append(Token(kind, value, line_num))
    return tokens


class Parser:
    # Removed inner Parser.SyntaxError class

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def _advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def _skip_newlines(self):
        while self.current_token and self.current_token.type == 'NEWLINE':
            self._advance()

    def _eat(self, token_type):
        token_to_eat = self.current_token
        if token_to_eat and token_to_eat.type == token_type:
            self._advance()
            return token_to_eat
        else:
            expected_type_str = token_type
            found_type_str = token_to_eat.type if token_to_eat else "EOF"
            line = token_to_eat.line if token_to_eat else "N/A"
            value_str = token_to_eat.value if token_to_eat else 'N/A'
            raise CustomParserSyntaxError(
                f"Expected token {expected_type_str} but found {found_type_str} "
                f"on line {line} (value: {value_str!r})"
            )

    def parse(self) -> dict:
        parsed_data = {
            "items": [], "recipes": [], "vehicles": [],
            "vehicle_models": [], "vehicle_templates": []
        }
        while self.current_token:
            self._skip_newlines()
            if not self.current_token: break
            if self.current_token.type == 'IDENTIFIER':
                if self.current_token.value == 'module':
                    self.parse_module(parsed_data["items"])
                elif self.current_token.value == 'item':
                    parsed_data["items"].append(self.parse_item())
                elif self.current_token.value == 'craftRecipe':
                    parsed_data["recipes"].append(self.parse_recipe())
                elif self.current_token.value == 'vehicle':
                    parsed_data["vehicles"].append(self.parse_vehicle_definition())
                elif self.current_token.value == 'model':
                    parsed_data["vehicle_models"].append(self.parse_vehicle_model_definition())
                elif self.current_token.value == 'template':
                    next_token_idx = self.pos + 1
                    if next_token_idx < len(self.tokens) and \
                       self.tokens[next_token_idx].type == 'IDENTIFIER' and \
                       self.tokens[next_token_idx].value == 'vehicle':
                        parsed_data["vehicle_templates"].append(self.parse_template_vehicle_definition())
                    else: self._advance()
                else: self._advance()
            else: self._advance()
        return parsed_data

    def parse_module(self, items_list: list[dict]):
        self._eat('IDENTIFIER')
        module_name_token = self._eat('IDENTIFIER')
        module_prefix = module_name_token.value + "."
        self._skip_newlines()
        self._eat('LBRACE')
        self._skip_newlines()
        while self.current_token and self.current_token.type != 'RBRACE':
            if self.current_token.type == 'IDENTIFIER' and self.current_token.value == 'item':
                items_list.append(self.parse_item(module_name_prefix=module_prefix))
            elif self.current_token.type == 'NEWLINE':
                self._skip_newlines()
            else:
                raise CustomParserSyntaxError(f"Unexpected token {self.current_token.value!r} inside module on line {self.current_token.line}")
        self._eat('RBRACE')
        self._skip_newlines()

    def parse_item(self, module_name_prefix: Optional[str] = None) -> dict:
        self._eat('IDENTIFIER')
        item_name_token = self._eat('IDENTIFIER')
        item_actual_name = item_name_token.value
        if module_name_prefix and not item_actual_name.startswith(module_name_prefix):
            if '.' not in item_actual_name:
                 item_actual_name = module_name_prefix + item_actual_name
        item_data = {'itemName': item_actual_name}
        self._skip_newlines(); self._eat('LBRACE'); self._skip_newlines()
        while self.current_token and self.current_token.type != 'RBRACE':
            if self.current_token.type == 'IDENTIFIER':
                key_token = self._eat('IDENTIFIER')
                key = key_token.value
                if self.current_token and self.current_token.type == 'IDENTIFIER':
                    component_type = key
                    component_name = self._eat('IDENTIFIER').value
                    item_data[f"{component_type} {component_name}"] = self.parse_block_as_dict()
                else:
                    self._eat('EQUALS')
                    value_token = self.current_token
                    if value_token.type == 'STRING': self._eat('STRING'); item_data[key] = value_token.value[1:-1]
                    elif value_token.type == 'NUMBER': self._eat('NUMBER'); item_data[key] = float(value_token.value) if '.' in value_token.value else int(value_token.value)
                    elif value_token.type == 'IDENTIFIER': self._eat('IDENTIFIER'); item_data[key] = value_token.value
                    else: raise CustomParserSyntaxError(f"Unexpected token type for value: {self.current_token} on line {self.current_token.line}")
                    value_line = value_token.line
                    if self.current_token and self.current_token.type == 'SEMICOLON': self._eat('SEMICOLON')
                    elif not (self.current_token and (self.current_token.type == 'NEWLINE' or self.current_token.type == 'RBRACE')) and self.current_token: # Not newline, RBRACE, or EOF
                        raise CustomParserSyntaxError(f"Expected SEMICOLON, NEWLINE, or RBRACE after value for key '{key}' on line {value_line}, but found {self.current_token.type} ('{self.current_token.value}') on line {self.current_token.line}")
            elif self.current_token.type == 'NEWLINE': self._skip_newlines()
            else: raise CustomParserSyntaxError(f"Unexpected token {self.current_token} in item block on line {self.current_token.line}")
            self._skip_newlines()
        self._eat('RBRACE'); self._skip_newlines()
        return item_data

    def parse_recipe(self) -> dict:
        self._eat('IDENTIFIER')
        recipe_name_token = self._eat('IDENTIFIER')
        recipe_data = {'recipeName': recipe_name_token.value}
        self._skip_newlines(); self._eat('LBRACE'); self._skip_newlines()
        while self.current_token and self.current_token.type != 'RBRACE':
            self._skip_newlines()
            if not self.current_token or self.current_token.type == 'RBRACE': break
            if self.current_token.type == 'IDENTIFIER':
                key_token = self.current_token; key = key_token.value
                if key == 'inputs' or key == 'outputs':
                    self._eat('IDENTIFIER'); recipe_data[key] = self.parse_inputs_outputs_block(key)
                elif key == 'itemMapper':
                    self._eat('IDENTIFIER'); mapper_name = self._eat('IDENTIFIER').value
                    recipe_data[f"{key} {mapper_name}"] = self.parse_block_as_dict()
                else:
                    self._eat('IDENTIFIER'); self._eat('EQUALS')
                    value_token = self.current_token
                    if value_token.type == 'STRING': self._eat('STRING'); recipe_data[key] = value_token.value[1:-1]
                    elif value_token.type == 'NUMBER': self._eat('NUMBER'); recipe_data[key] = float(value_token.value) if '.' in value_token.value else int(value_token.value)
                    elif value_token.type == 'IDENTIFIER': self._eat('IDENTIFIER'); recipe_data[key] = value_token.value
                    else: raise CustomParserSyntaxError(f"Unexpected value token {self.current_token} for key '{key}' in recipe on line {self.current_token.line}")
                    value_line = value_token.line
                    if self.current_token and self.current_token.type == 'SEMICOLON': self._eat('SEMICOLON')
                    elif not (self.current_token and (self.current_token.type == 'NEWLINE' or self.current_token.type == 'RBRACE')) and self.current_token:
                        raise CustomParserSyntaxError(f"Expected SEMICOLON, NEWLINE, or RBRACE after value for key '{key}' in recipe on line {value_line}, but found {self.current_token.type} ('{self.current_token.value}') on line {self.current_token.line}")
            else: raise CustomParserSyntaxError(f"Unexpected token {self.current_token.value!r} in recipe block on line {self.current_token.line}")
            self._skip_newlines()
        self._eat('RBRACE'); self._skip_newlines()
        return recipe_data

    def parse_inputs_outputs_block(self, block_type: str) -> list[dict]:
        entries = []
        self._skip_newlines(); self._eat('LBRACE'); self._skip_newlines()
        while self.current_token and self.current_token.type != 'RBRACE':
            self._skip_newlines()
            if not self.current_token or self.current_token.type == 'RBRACE': break
            entry = {}
            # Skipping the '-' logic for now as IDENTIFIER regex handles -fluid
            first_token = self._eat('IDENTIFIER')
            if first_token.value == 'item': entry['type'] = 'item'
            elif first_token.value == 'fluid' or first_token.value == '-fluid':
                entry['type'] = 'fluid'
                if first_token.value == '-fluid': entry['negative_marker'] = True
            else: raise CustomParserSyntaxError(f"Expected 'item' or 'fluid' in {block_type} block, got {first_token.value!r} on line {first_token.line}")

            qty_token_val = self._eat('NUMBER').value
            try: entry['quantity'] = float(qty_token_val) if '.' in qty_token_val else int(qty_token_val)
            except ValueError: raise CustomParserSyntaxError(f"Invalid number format for quantity {qty_token_val!r} on line {first_token.line}")

            if self.current_token and self.current_token.type == 'IDENTIFIER' and self.current_token.value not in ['tags', 'categories', 'mode', 'flags', 'mapper']:
                entry['name'] = self._eat('IDENTIFIER').value

            while self.current_token and self.current_token.type == 'IDENTIFIER':
                attr_keyword_token = self.current_token; attr_keyword = attr_keyword_token.value
                if attr_keyword in ['tags', 'categories', 'flags']:
                    self._eat('IDENTIFIER'); self._eat('LBRACKET'); values = []
                    while self.current_token and self.current_token.type != 'RBRACKET':
                        if self.current_token.type == 'IDENTIFIER': values.append(self._eat('IDENTIFIER').value)
                        elif self.current_token.type == 'SEMICOLON': self._eat('SEMICOLON')
                        else: raise CustomParserSyntaxError(f"Unexpected token {self.current_token.value!r} inside {attr_keyword} list on line {self.current_token.line}")
                    self._eat('RBRACKET'); entry[attr_keyword] = values
                elif attr_keyword == 'mode':
                    self._eat('IDENTIFIER'); self._eat('COLON'); entry['mode'] = self._eat('IDENTIFIER').value
                elif attr_keyword == 'mapper' and block_type == 'outputs':
                    self._eat('IDENTIFIER'); self._eat('COLON'); entry['mapper'] = self._eat('IDENTIFIER').value
                else:
                    if 'name' not in entry: entry['name'] = self._eat('IDENTIFIER').value
                    else: raise CustomParserSyntaxError(f"Unexpected attribute keyword {attr_keyword!r} on line {attr_keyword_token.line} in {block_type} entry.")

            if self.current_token and self.current_token.type == 'SEMICOLON': self._eat('SEMICOLON')
            elif not (self.current_token and (self.current_token.type == 'NEWLINE' or self.current_token.type == 'RBRACE')) and self.current_token :
                 raise CustomParserSyntaxError(f"Expected SEMICOLON, NEWLINE, or RBRACE after {block_type} entry on line {first_token.line}, but found {self.current_token.type} ('{self.current_token.value}')")
            entries.append(entry)
            self._skip_newlines()
        self._eat('RBRACE'); self._skip_newlines()
        return entries

    def _parse_value(self, key_name_for_error: str, owner_line: int):
        values = []
        if self.current_token and self.current_token.type == 'LBRACKET':
            self._eat('LBRACKET'); list_values = []
            while self.current_token and self.current_token.type != 'RBRACKET':
                self._skip_newlines()
                if self.current_token.type == 'RBRACKET': break
                if self.current_token.type == 'IDENTIFIER': list_values.append(self._eat('IDENTIFIER').value)
                elif self.current_token.type == 'STRING': list_values.append(self._eat('STRING').value[1:-1])
                elif self.current_token.type == 'NUMBER':
                    num_token = self._eat('NUMBER')
                    list_values.append(float(num_token.value) if '.' in num_token.value else int(num_token.value))
                else: raise CustomParserSyntaxError(f"Unexpected token {self.current_token.value!r} in list for key '{key_name_for_error}' on line {self.current_token.line}")
                self._skip_newlines()
                if self.current_token and self.current_token.type == 'SEMICOLON': self._eat('SEMICOLON')
                elif not (self.current_token and (self.current_token.type == 'RBRACKET' or self.current_token.type == 'NEWLINE')):
                    raise CustomParserSyntaxError(f"Expected SEMICOLON or RBRACKET after list item in '{key_name_for_error}', found {self.current_token.type if self.current_token else 'EOF'} on line {self.current_token.line if self.current_token else owner_line}")
            self._eat('RBRACKET'); return list_values

        while self.current_token and \
              (self.current_token.type == 'NUMBER' or self.current_token.type == 'STRING' or self.current_token.type == 'IDENTIFIER') and \
              self.current_token.type not in ['SEMICOLON', 'NEWLINE', 'RBRACE', 'LBRACE', 'EQUALS', 'LBRACKET']:
            token = self.current_token
            if token.type == 'STRING': values.append(token.value[1:-1])
            elif token.type == 'NUMBER': values.append(float(token.value) if '.' in token.value else int(token.value))
            else: values.append(token.value)
            self._advance()
        if not values:
            found_token_type = self.current_token.type if self.current_token else 'EOF'
            found_token_value = self.current_token.value if self.current_token else 'N/A'
            found_token_line = self.current_token.line if self.current_token else owner_line
            raise CustomParserSyntaxError(f"Expected a value for key '{key_name_for_error}' (on line {owner_line}), but found {found_token_type} ('{found_token_value}') on line {found_token_line}")
        return values[0] if len(values) == 1 else values

    def _parse_generic_block_content(self, data: dict, block_name_for_error: str):
        while self.current_token and self.current_token.type != 'RBRACE':
            self._skip_newlines()
            if not self.current_token or self.current_token.type == 'RBRACE': break
            if self.current_token.type == 'IDENTIFIER':
                key_token = self._eat('IDENTIFIER'); key = key_token.value
                if self.current_token and (self.current_token.type == 'IDENTIFIER' or self.current_token.type == 'LBRACE'):
                    block_is_named = self.current_token.type == 'IDENTIFIER'
                    nested_block_keys = ["passenger", "area", "wheel", "part", "attachment", "model", "skin", "sound"]
                    if key in nested_block_keys:
                        nested_block_name = None; current_key_line = key_token.line
                        if block_is_named and self.current_token.type == 'IDENTIFIER':
                            nested_block_name = self._eat('IDENTIFIER').value
                        elif key not in ["model", "skin", "sound"] and not (self.current_token.type == 'LBRACE'):
                            raise CustomParserSyntaxError(f"Expected name or LBRACE for '{key}' block defined on line {current_key_line}, found {self.current_token.type} '{self.current_token.value}' on line {self.current_token.line}")
                        self._skip_newlines()
                        if self.current_token and self.current_token.type == 'LBRACE':
                            block_content = self.parse_block_as_dict(is_component_or_mapper=False)
                            if key in ["model", "skin", "sound"]: data[key] = block_content
                            else:
                                if key not in data: data[key] = []
                                entry_to_add = block_content
                                if nested_block_name: entry_to_add['_name'] = nested_block_name
                                data[key].append(entry_to_add)
                            if self.current_token and self.current_token.type == 'SEMICOLON': self._eat('SEMICOLON')
                            continue
                        elif nested_block_name is not None:
                             raise CustomParserSyntaxError(f"Expected LBRACE for '{key} {nested_block_name}' block defined on line {current_key_line}, but found {self.current_token.type if self.current_token else 'EOF'}")
                self._eat('EQUALS'); data[key] = self._parse_value(key, key_token.line)
                if self.current_token and self.current_token.type == 'SEMICOLON': self._eat('SEMICOLON')
                elif not (self.current_token and (self.current_token.type == 'NEWLINE' or self.current_token.type == 'RBRACE')) and self.current_token:
                    raise CustomParserSyntaxError(f"Expected SEMICOLON, NEWLINE, or RBRACE after value for key '{key}' in {block_name_for_error} block on line {key_token.line}, but found {self.current_token.type} ('{self.current_token.value}') on line {self.current_token.line}")
            else: raise CustomParserSyntaxError(f"Unexpected token {self.current_token.value!r} in {block_name_for_error} block on line {self.current_token.line}")
            self._skip_newlines()

    def parse_block_as_dict(self, is_component_or_mapper=True) -> dict:
        data = {}; block_start_line = self.current_token.line if self.current_token else "N/A"
        self._skip_newlines(); self._eat('LBRACE'); self._skip_newlines()
        if is_component_or_mapper:
            while self.current_token and self.current_token.type != 'RBRACE':
                self._skip_newlines()
                if not self.current_token or self.current_token.type == 'RBRACE': break
                if self.current_token.type == 'IDENTIFIER':
                    key_token = self._eat('IDENTIFIER'); key = key_token.value
                    self._eat('EQUALS'); data[key] = self._parse_value(key, key_token.line)
                    value_line_approx = key_token.line
                    if self.current_token and self.current_token.type == 'SEMICOLON': self._eat('SEMICOLON')
                    elif not (self.current_token and (self.current_token.type == 'NEWLINE' or self.current_token.type == 'RBRACE')) and self.current_token:
                        raise CustomParserSyntaxError(f"Expected SEMICOLON, NEWLINE, or RBRACE after value for key '{key}' in simple block on line {value_line_approx}, but found {self.current_token.type} ('{self.current_token.value}') on line {self.current_token.line if self.current_token else 'N/A'}")
                else: raise CustomParserSyntaxError(f"Unexpected token {self.current_token.value!r} in simple block on line {self.current_token.line if self.current_token else 'N/A'}")
                self._skip_newlines()
        else: self._parse_generic_block_content(data, "vehicle-related")
        self._eat('RBRACE'); self._skip_newlines()
        return data

    def parse_vehicle_definition(self) -> dict:
        self._eat('IDENTIFIER'); name_token = self._eat('IDENTIFIER')
        data = {'vehicleName': name_token.value}
        self._skip_newlines(); self._eat('LBRACE'); self._skip_newlines()
        self._parse_generic_block_content(data, f"vehicle '{name_token.value}'")
        self._eat('RBRACE'); self._skip_newlines()
        return data

    def parse_vehicle_model_definition(self) -> dict:
        self._eat('IDENTIFIER'); name_token = self._eat('IDENTIFIER')
        data = {'modelName': name_token.value}
        self._skip_newlines(); self._eat('LBRACE'); self._skip_newlines()
        self._parse_generic_block_content(data, f"model '{name_token.value}'")
        self._eat('RBRACE'); self._skip_newlines()
        return data

    def parse_template_vehicle_definition(self) -> dict:
        self._eat('IDENTIFIER'); self._eat('IDENTIFIER'); name_token = self._eat('IDENTIFIER')
        data = {'templateName': name_token.value}
        self._skip_newlines(); self._eat('LBRACE'); self._skip_newlines()
        self._parse_generic_block_content(data, f"template vehicle '{name_token.value}'")
        self._eat('RBRACE'); self._skip_newlines()
        return data

SyntaxError = CustomParserSyntaxError # Alias for external use

def parse_script(script_content: str) -> dict:
    tokens = tokenize(script_content)
    if not tokens: return {"items": [], "recipes": [], "vehicles": [], "vehicle_models": [], "vehicle_templates": []}
    parser = Parser(tokens)
    try: return parser.parse()
    except CustomParserSyntaxError as e: # Catching the custom error
        logger.error(f"Parser Syntax Error: {e}")
        return {"items": [], "recipes": [], "vehicles": [], "vehicle_models": [], "vehicle_templates": []}
    except RuntimeError as e: # From tokenizer
        logger.error(f"Tokenizer Runtime Error: {e}")
        return {"items": [], "recipes": [], "vehicles": [], "vehicle_models": [], "vehicle_templates": []}

if __name__ == '__main__':
    example_script = """
module Base {
    item BathTowel { DisplayName = "Bath Towel"; Type = Normal; Weight = 0.2; }
    item IndustrialDye { DisplayName = "Industrial Dye"; Type = Chemical; Weight = 0.5; component FluidContainer { Capacity = 100; ContentType = Dye; } }
}
item LooseScrew { DisplayName = "Loose Screw"; Type = Junk; Weight = 0.01; }
    """
    print("--- Parsing main example script (Items) ---")
    parsed_data = parse_script(example_script)
    if parsed_data["items"]:
        import json
        for item_dict in parsed_data["items"]: print(json.dumps(item_dict, indent=2))
    else: print("No items parsed from main example script or error occurred.")
    if parsed_data["recipes"]: print(f"Recipes from item script (should be empty): {parsed_data['recipes']}")

    example_script_missing_semicolon = """
    item TestItem { Prop1 = "Value1" Prop2 = 123 }
    item AnotherTest { Prop3 = "Value3"; Prop4 = "Value4" }"""
    print("\n--- Test with missing semicolon (Items) ---")
    parsed_data_missing_semi = parse_script(example_script_missing_semicolon)
    if parsed_data_missing_semi["items"]:
        import json
        for item_dict in parsed_data_missing_semi["items"]: print(json.dumps(item_dict, indent=2))
    else: print("Parsing failed or no items from script with missing semicolon.")

    example_script_syntax_error = "item ErrorItem { BadProperty = = }"
    print("\n--- Test with syntax error (extra equals, Items) ---")
    parse_script(example_script_syntax_error)

    example_script_complex = """
module Core {
    item AdvancedTool {
        DisplayName = "Advanced Multi-Tool"; Type = Tool; Weight = 1.5; Durability = 500;
        icon = "UI/Icons/Tool.png"; Stackable = false;
        component PowerSource { Capacity = 1000; ChargeRate = 50; }
        action Repair { ToolRequired = Screwdriver; SkillRequired = Mechanics; Time = 10.0; }
    }
}"""
    print("\n--- Test with component and more fields (complex item, Items) ---")
    parsed_complex_data = parse_script(example_script_complex)
    if parsed_complex_data["items"]:
        import json
        for item_dict in parsed_complex_data["items"]: print(json.dumps(item_dict, indent=2))
    else: print("No items parsed from complex script or error occurred.")

    empty_script = ""
    print("\n--- Test empty script ---")
    parsed_empty_data = parse_script(empty_script); print(f"Parsed empty script: {parsed_empty_data}")

    comment_script = "// Comment only"
    print("\n--- Test script with only comments and newlines (Items) ---")
    parsed_comments_data = parse_script(comment_script); print(f"Parsed comment script: {parsed_comments_data}")

    malformed_component_script = "item Malformed { component MissingBrace Capacity = 10; }"
    print("\n--- Test with malformed component (missing LBRACE, Items) ---")
    parse_script(malformed_component_script)

    malformed_property_script = 'item MalformedProp { PropA = "ValueA" PropB = "ValueB" }'
    print("\n--- Test with unexpected token after property value (missing semicolon AND not on newline, Items) ---")
    parse_script(malformed_property_script)

    escaped_string_script = 'item EscapedStringItem { Description = "String with \\"escaped quotes\\""; }'
    print("\n--- Test with string containing escaped quotes (Items) ---")
    parsed_escaped_string_data = parse_script(escaped_string_script)
    if parsed_escaped_string_data["items"]:
        import json
        for item_dict in parsed_escaped_string_data["items"]: print(json.dumps(item_dict, indent=2))

    item_outside_module_script = 'item StandaloneItem { Feature = "WorksOutsideModule"; }'
    print("\n--- Test with item outside module (should still parse if not in module block, Items) ---")
    parsed_standalone_data = parse_script(item_outside_module_script)
    if parsed_standalone_data["items"]:
        import json
        for item_dict in parsed_standalone_data["items"]: print(json.dumps(item_dict, indent=2))

    example_recipe_script = """
    craftRecipe MyAwesomeRecipe {
        Time = 120; category = CraftingBench;
        inputs { item 2 Base.IronIngot; item 1 tags[Hammer] mode:keep flags[HeavyDuty]; -fluid 5.5 categories[Water] mode:consume; }
        outputs { item 1 Base.IronPlate; item 1 mapper:bonusOutputItem; }
        itemMapper bonusOutputItem { Result1 = Base.BonusParts; Result2 = Base.ScrapMetal; Default = Base.NothingSpecial; }
    }"""
    # Configure logging for standalone parser testing if needed
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    print("\n--- Parsing example recipe script ---")
    parsed_recipe_data = parse_script(example_recipe_script)
    if parsed_recipe_data["recipes"]:
        import json; logger.info("\n--- Parsed Recipes (raw) ---") # Changed print to logger.info for consistency
        for recipe_dict in parsed_recipe_data["recipes"]: logger.info(json.dumps(recipe_dict, indent=2))
    else: logger.warning("No recipes parsed from example recipe script or error occurred.") # Changed print
    if parsed_recipe_data["items"]: logger.info(f"Items from recipe script: {parsed_recipe_data['items']}") # Changed print

    # The data transformation part is more for testing the transformer and models,
    # but if kept here, its prints could also become logs or be conditional.
    # For now, focusing on parser's own prints.
    # print("\n\n" + "="*30 + " STARTING DATA TRANSFORMATION " + "="*30)
    # from data_transformer import transform_parsed_data

    example_vehicle_script = """
    vehicle CarNormal {
        mass = 800; engineForce = 4000;
        model { file = "Vehicles/CarNormal_model"; }
        passenger Driver { offset = 0.0 0.5 0.0; canSwitchTo = [Gunner1;Gunner2]; }
        wheel FR { offset = 0.3626 -0.3022 0.8516; radius = 0.35; }
        part Engine { health = 100; item = Base.CarEngineItem; }
        skin { texture = "vehicles/car_normal_diff.png"; material = "Metal"; }
    }
    model CarPoliceModel { file = "Vehicles/CarPolice_model"; scale = 1.05; }
    template vehicle BaseCarTemplate { mass = 750; area DamageAreaHood { shape = box; extent = 0.5 0.5 0.5; offset = 0.0 1.0 0.0; } }
    """
    print("--- Parsing example vehicle script ---") # This can remain print for CLI-like testing
    parsed_vehicle_data = parse_script(example_vehicle_script)
    # Using logger for raw parsed data output if desired for debugging
    if parsed_vehicle_data["vehicles"]: import json; logger.debug("\n--- Parsed Vehicles (raw) ---"); [logger.debug(json.dumps(v_dict, indent=2)) for v_dict in parsed_vehicle_data["vehicles"]]
    if parsed_vehicle_data["vehicle_models"]: import json; logger.debug("\n--- Parsed Vehicle Models (raw) ---"); [logger.debug(json.dumps(m_dict, indent=2)) for m_dict in parsed_vehicle_data["vehicle_models"]]
    if parsed_vehicle_data["vehicle_templates"]: import json; logger.debug("\n--- Parsed Vehicle Templates (raw) ---"); [logger.debug(json.dumps(t_dict, indent=2)) for t_dict in parsed_vehicle_data["vehicle_templates"]]

    # The transformation part is more for integration testing, its verbosity can be reduced or made conditional.
    # For this subtask, the key is that the parser itself uses logging for its errors.
    # The `if __name__ == '__main__'` in script_parser.py is primarily for testing the parser itself.
    # The actual transformation and use of data models happen in data_repository.py and mcp_server_cli.py.

    # If you want to see the transformation output when running script_parser.py directly:
    if True: # Set to False to hide transformation details when running parser tests
        print("\n\n" + "="*30 + " STARTING DATA TRANSFORMATION (for parser direct test) " + "="*30)
        from data_transformer import transform_parsed_data # Import locally for this test block

        full_parsed_data = { "items": [], "recipes": [], "vehicles": [], "vehicle_models": [], "vehicle_templates": [] }

        # logger.info("\n--- (Re-parsing items for full transformation test) ---")
        item_script_data = parse_script(example_script)
        full_parsed_data["items"].extend(item_script_data["items"])

        # logger.info("\n--- (Re-parsing recipes for full transformation test) ---")
        recipe_script_data = parse_script(example_recipe_script)
        full_parsed_data["recipes"].extend(recipe_script_data["recipes"])

        # logger.info("\n--- (Using previously parsed vehicle data for full transformation test) ---")
        full_parsed_data["vehicles"].extend(parsed_vehicle_data["vehicles"])
        full_parsed_data["vehicle_models"].extend(parsed_vehicle_data["vehicle_models"])
        full_parsed_data["vehicle_templates"].extend(parsed_vehicle_data["vehicle_templates"])

        transformed_data_objects = transform_parsed_data(full_parsed_data)

        print("\n\n" + "="*30 + " TRANSFORMED DATA OBJECTS (for parser direct test) " + "="*30)
        print("\n--- Transformed Items (Objects) ---")
        if transformed_data_objects["items"]: [print(repr(obj)) for obj in transformed_data_objects["items"]]
        else: print("No items transformed.")
        print("\n--- Transformed Recipes (Objects) ---")
        if transformed_data_objects["recipes"]: [print(repr(obj)) for obj in transformed_data_objects["recipes"]]
        else: print("No recipes transformed.")
        # ... and so on for other types if desired ...
