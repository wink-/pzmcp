import json
import os
from typing import Dict, Any, List
from pydantic import BaseModel

# Corrected TEMPLATES_DIR path construction relative to this file (script_generator.py)
# mcp_server/core/script_generator.py -> mcp_server/templates/
TEMPLATES_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates"))

class ScriptGenerator:
    def __init__(self, templates_dir: str = TEMPLATES_DIR):
        self.templates_dir = templates_dir
        if not os.path.exists(self.templates_dir):
            # This was in the original plan, but for a library, it might be better to error if not found
            # rather than creating it, as the templates should be packaged with the app.
            # However, for development or if templates are user-supplied later, makedirs is fine.
            print(f"Templates directory '{self.templates_dir}' not found. Creating it.")
            os.makedirs(self.templates_dir, exist_ok=True)

    def _load_template(self, template_name: str) -> Dict[str, Any]:
        if not template_name.endswith(".json"):
            template_name_json = f"{template_name}.json"
        else:
            template_name_json = template_name

        template_path = os.path.join(self.templates_dir, template_name_json)
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template '{template_name_json}' not found in {self.templates_dir}")

        with open(template_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _format_input_items(self, input_items: List[str]) -> str:
        # Formats list of input items for recipe script, ensuring comma at the end of each
        # and stripping extra spaces around the item string itself.
        return "\n".join([f"        {item.strip().rstrip(',').strip()}," for item in input_items if item.strip()])


    def generate_script_from_template(self, template_name: str, params: BaseModel) -> str:
        template_config = self._load_template(template_name)
        script_format_lines: List[str] = template_config.get("script_format", [])

        param_dict = params.model_dump(exclude_none=False) # Keep None values to identify them

        # Ensure input_items_formatted is available in param_dict for formatting
        if "input_items" in param_dict and isinstance(param_dict.get("input_items"), list):
            param_dict["input_items_formatted"] = self._format_input_items(param_dict.get("input_items") or [])
        else:
            # Provide a default empty string if not a recipe or input_items is not relevant
            param_dict.setdefault("input_items_formatted", "")

        final_lines = []
        for line in script_format_lines:
            placeholders = re.findall(r"\{(\w+)\}", line)
            should_skip_line = False

            # Determine if the line should be skipped due to optional fields being None
            for ph in placeholders:
                if ph in param_dict and param_dict[ph] is None:
                    # Common patterns for optional lines: "Key: {ph}," or "Key = {ph}," or just "{ph}"
                    if re.match(rf"^\s*\w+\s*[:=]\s*{{{ph}}}\s*,?\s*$", line.strip()) or \
                       line.strip() == f"{{{ph}}}":
                        should_skip_line = True
                        break

            if should_skip_line:
                # print(f"DEBUG: Skipping line due to resolved None placeholder: {line}")
                continue

            # For formatting, create a dictionary where original None values are now empty strings
            # This dict (format_params) will be used with .format()
            # Iteratively format the line for known placeholders
            # Unknown placeholders (not in param_dict) will be left as is.
            formatted_line = line
            if placeholders:
                for ph in placeholders:
                    if ph in param_dict: # Check if placeholder is a known model field
                        value_to_format = param_dict[ph] if param_dict[ph] is not None else ""
                        formatted_line = formatted_line.replace(f"{{{ph}}}", str(value_to_format))
                    # else: placeholder 'ph' is not in param_dict (not a model field),
                    # so it's left as is in formatted_line during this iteration.

            final_lines.append(formatted_line)

        return "\n".join(final_lines)

# Need to import 're' for the new logic
import re

if __name__ == '__main__':
    from mcp_server.core.models import ItemTemplateParams, RecipeTemplateParams

    generator = ScriptGenerator()
    print(f"Using templates from: {os.path.abspath(generator.templates_dir)}")

    # Item example
    item_data = ItemTemplateParams(
        module_name="MyItems",
        item_name="AwesomeSword",
        display_name="Awesome Sword of Power",
        icon="SwordIcon",
        weight=2.5,
        item_type="Weapon" # This will be used by basic_item, simple_weapon will override Type directly
    )
    # For simple_weapon, we might want to set weapon-specific fields
    item_data_for_weapon = ItemTemplateParams(
        module_name="MyWeapons",
        item_name="BasicMace",
        display_name="Basic Mace",
        icon="MaceIcon",
        weight=3.0,
        item_type="Weapon", # Used by basic_item if that template was used. simple_weapon has Type=Weapon hardcoded.
                            # For simple_weapon template, these are the important ones:
        min_damage=1.5,
        max_damage=2.8,
        swing_sound="HeavySwing",
        categories="BluntWeapon"
    )

    generated_item_script = generator.generate_script_from_template("basic_item", item_data)
    print("\n--- Generated Item Script (basic_item with AwesomeSword) ---")
    print(generated_item_script)

    generated_weapon_script = generator.generate_script_from_template("simple_weapon", item_data_for_weapon)
    print("\n--- Generated Item Script (simple_weapon with BasicMace) ---")
    print(generated_weapon_script)

    # Recipe example
    recipe_data = RecipeTemplateParams(
        module_name="MyRecipes",
        recipe_name="Craft Awesome Sword",
        result_item="MyItems.AwesomeSword", # Assuming item from above
        result_quantity=1,
        time=300,
        input_items=["Base.SteelIngot=5", "keep Base.MagicHammer", "Gems.PowerStone=1"],
        category="Weapons",
        skill_required="Metalworking=5", # Optional field example
        near_item = None # Example of explicitly setting an optional field to None
    )
    generated_recipe_script = generator.generate_script_from_template("basic_recipe", recipe_data)
    print("\n--- Generated Recipe Script ---")
    print(generated_recipe_script)

    # Test recipe with no optional fields
    recipe_data_simple = RecipeTemplateParams(
        module_name="MyCookbook",
        recipe_name="Make Toast",
        result_item="Food.Toast",
        input_items=["Food.BreadSlice"]
    )
    generated_simple_recipe_script = generator.generate_script_from_template("basic_recipe", recipe_data_simple)
    print("\n--- Generated Simple Recipe Script (no optional props) ---")
    print(generated_simple_recipe_script)
