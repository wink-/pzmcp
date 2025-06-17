import pytest
import os
import json
from mcp_server.core.script_generator import ScriptGenerator
from mcp_server.core.models import ItemTemplateParams, RecipeTemplateParams

# Utility to create dummy template files for testing
def create_dummy_template(templates_dir, name, content):
    template_path = os.path.join(templates_dir, f"{name}.json")
    os.makedirs(os.path.dirname(template_path), exist_ok=True) # Ensure directory exists
    with open(template_path, 'w') as f:
        json.dump(content, f)
    return template_path

@pytest.fixture(scope="module")
def script_generator_with_temps(tmp_path_factory):
    # Create a temporary directory for templates for this test module
    temp_templates_dir = tmp_path_factory.mktemp("test_templates")

    # Create dummy item template
    create_dummy_template(
        temp_templates_dir,
        "test_item_template",
        {
            "template_type": "item",
            "description": "A test item.",
            "script_format": [
                "module {module_name} {{",
                "    item {item_name} {{",
                "        Type = {item_type},",
                "        DisplayName = {display_name},",
                "        Icon = {icon},",
                "        Weight = {weight},",
                "    }}",
                "}}"
            ]
        }
    )

    # Create dummy recipe template
    create_dummy_template(
        temp_templates_dir,
        "test_recipe_template",
        {
            "template_type": "recipe",
            "description": "A test recipe.",
            "script_format": [
                "module {module_name} {{",
                "    recipe \"{recipe_name}\" {{",
                "{input_items_formatted}",
                "        ",
                "        Result:{result_item}={result_quantity},",
                "        Time:{time},",
                "        Category:{category},",
                "    }}",
                "}}"
            ]
        }
    )
    return ScriptGenerator(templates_dir=str(temp_templates_dir))

def test_load_template_found(script_generator_with_temps: ScriptGenerator):
    template_data = script_generator_with_temps._load_template("test_item_template")
    assert template_data["description"] == "A test item."
    template_data_json = script_generator_with_temps._load_template("test_item_template.json")
    assert template_data_json["description"] == "A test item."


def test_load_template_not_found(script_generator_with_temps: ScriptGenerator):
    with pytest.raises(FileNotFoundError):
        script_generator_with_temps._load_template("non_existent_template")

def test_generate_item_script(script_generator_with_temps: ScriptGenerator):
    params = ItemTemplateParams(
        module_name="TestMod",
        item_name="TestItem",
        display_name="My Test Item",
        icon="TestIcon.png",
        weight=0.75,
        item_type="Junk"
    )
    script = script_generator_with_temps.generate_script_from_template("test_item_template", params)
    assert "module TestMod" in script
    assert "item TestItem" in script
    assert "DisplayName = My Test Item" in script
    assert "Weight = 0.75" in script
    assert "Type = Junk" in script

def test_generate_recipe_script(script_generator_with_temps: ScriptGenerator):
    params = RecipeTemplateParams(
        module_name="TestRecipes",
        recipe_name="Craft Test Item",
        input_items=["Wood=2", "keep Hammer"],
        result_item="TestMod.TestItem",
        result_quantity=1,
        time=50,
        category="Testing"
    )
    script = script_generator_with_temps.generate_script_from_template("test_recipe_template", params)
    assert "module TestRecipes" in script
    assert "recipe \"Craft Test Item\"" in script # Note: recipe name is quoted in template
    assert "        Wood=2," in script
    assert "        keep Hammer," in script
    assert "Result:TestMod.TestItem=1" in script
    assert "Time:50" in script
    assert "Category:Testing" in script

def test_generate_script_missing_placeholder_in_params(script_generator_with_temps: ScriptGenerator):
    # Create a template with a placeholder not in ItemTemplateParams
    create_dummy_template(
        script_generator_with_temps.templates_dir, # Use the temp dir from the fixture
        "custom_placeholder_template",
        {
            "template_type": "item",
            "script_format": ["item {item_name} {{ CustomProp = {custom_placeholder}; }}"] # Added semicolon for clarity
        }
    )
    params = ItemTemplateParams(item_name="TestItem", module_name="AnyMod") # module_name is required by BaseTemplateParams
    script = script_generator_with_temps.generate_script_from_template("custom_placeholder_template", params)
    # Default behavior in ScriptGenerator is to keep the placeholder if param not found (and print warning)
    assert "CustomProp = {custom_placeholder};" in script # Semicolon helps verify exact match
    assert "item TestItem" in script

def test_format_input_items(script_generator_with_temps: ScriptGenerator):
    inputs = ["Wood=2", "keep Hammer", "MetalScraps=5/IronScraps=3", "  Food.RottenApple  , "] # Test with spaces and trailing comma
    formatted = script_generator_with_temps._format_input_items(inputs)
    expected = ("        Wood=2,\n"
                "        keep Hammer,\n"
                "        MetalScraps=5/IronScraps=3,\n"
                "        Food.RottenApple,") # Expects comma, and stripping of external spaces/commas
    assert formatted == expected

def test_generate_script_with_optional_params_not_provided(script_generator_with_temps: ScriptGenerator):
    # Template that uses optional fields from RecipeTemplateParams
    create_dummy_template(
        script_generator_with_temps.templates_dir,
        "recipe_optional_template",
        {
            "template_type": "recipe",
            "description": "A test recipe with optional skill.",
            "script_format": [
                "module {module_name} {{",
                "    recipe \"{recipe_name}\" {{",
                "{input_items_formatted}",
                "        ",
                "        Result:{result_item}={result_quantity},",
                "        Time:{time},",
                "        Category:{category},",
                "        SkillRequired:{skill_required},", # This line might be removed by generator if skill_required is None
                "        NearItem:{near_item},",           # This line might be removed by generator if near_item is None
                "    }}",
                "}}"
            ]
        }
    )
    params = RecipeTemplateParams(
        module_name="TestOptional",
        recipe_name="EasyRecipe",
        input_items=["Stick"],
        result_item="PointyStick",
        # skill_required and near_item are deliberately not provided (will be None)
    )
    script = script_generator_with_temps.generate_script_from_template("recipe_optional_template", params)
    assert "module TestOptional" in script
    assert "recipe \"EasyRecipe\"" in script
    assert "        Stick," in script
    assert "Result:PointyStick=1" in script
    # Check that lines with None-valued optional params are removed by the generator's logic
    assert "SkillRequired:" not in script
    assert "NearItem:" not in script

def test_generate_script_with_optional_params_provided(script_generator_with_temps: ScriptGenerator):
    params = RecipeTemplateParams(
        module_name="TestOptional",
        recipe_name="HardRecipe",
        input_items=["Metal=5"],
        result_item="MetalBar",
        skill_required="Metalworking=2",
        near_item="Anvil"
    )
    # Using recipe_optional_template created in the previous test
    script = script_generator_with_temps.generate_script_from_template("recipe_optional_template", params)
    assert "module TestOptional" in script
    assert "recipe \"HardRecipe\"" in script
    assert "        Metal=5," in script
    assert "Result:MetalBar=1" in script
    assert "SkillRequired:Metalworking=2," in script
    assert "NearItem:Anvil," in script
