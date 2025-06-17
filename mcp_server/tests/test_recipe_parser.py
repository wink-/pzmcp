import pytest
from mcp_server.parsers.recipe_parser import RecipeParser

def test_simple_recipe():
    script_content = """
    module Base {
        recipe "Make Bread" {
            Flour,
            Water,
            Yeast,

            Result:Bread=1,
            Time:30.0,
            Sound:CraftingSound
        }
    }
    """
    parser = RecipeParser(script_content)
    expected = {
        "module": "Base",
        "recipes": [{
            "name": "Make Bread",
            "inputs": [
                {"item": "Flour", "alternatives": [], "keep": False, "quantity": None},
                {"item": "Water", "alternatives": [], "keep": False, "quantity": None},
                {"item": "Yeast", "alternatives": [], "keep": False, "quantity": None}
            ],
            "properties": {"Time": 30.0, "Sound": "CraftingSound"},
            "result": {"item": "Bread", "quantity": 1}
        }]
    }
    assert parser.parse() == expected

def test_input_item_variations():
    script_content = """
    module Cooking {
        recipe "Advanced Dish" {
            keep Bowl,
            Vegetable/Fruit,
            Meat=2,
            keep Spice/Herb=1,

            Result:GourmetMeal=1,
            Time:100
        }
    }
    """
    parser = RecipeParser(script_content)
    expected = {
        "module": "Cooking",
        "recipes": [{
            "name": "Advanced Dish",
            "inputs": [
                {"item": "Bowl", "alternatives": [], "keep": True, "quantity": None},
                {"item": "Vegetable", "alternatives": ["Fruit"], "keep": False, "quantity": None},
                {"item": "Meat", "alternatives": [], "keep": False, "quantity": 2},
                {"item": "Spice", "alternatives": ["Herb"], "keep": True, "quantity": 1}
            ],
            "properties": {"Time": 100},
            "result": {"item": "GourmetMeal", "quantity": 1}
        }]
    }
    parsed_data = parser.parse()
    assert parsed_data == expected


def test_result_property():
    script_content = """
    module Carpentry {
        recipe BuildChair { // Unquoted recipe name
            WoodPlank=4,
            Nails=4,

            Result:Chair, // Result without explicit quantity
            Time:200
        }
        recipe "Paint Chair" {
            Chair,
            PaintCan=1,

            Result:PaintedChair=1, // Result with quantity
            OnSuccess:PlaySound PaintSound
        }
    }
    """
    parser = RecipeParser(script_content)
    expected = {
        "module": "Carpentry",
        "recipes": [
            {
                "name": "BuildChair",
                "inputs": [
                    {"item": "WoodPlank", "alternatives": [], "keep": False, "quantity": 4},
                    {"item": "Nails", "alternatives": [], "keep": False, "quantity": 4}
                ],
                "properties": {"Time": 200},
                "result": {"item": "Chair", "quantity": 1}
            },
            {
                "name": "Paint Chair",
                "inputs": [
                    {"item": "Chair", "alternatives": [], "keep": False, "quantity": None},
                    {"item": "PaintCan", "alternatives": [], "keep": False, "quantity": 1}
                ],
                "properties": {"OnSuccess": "PlaySound PaintSound"},
                "result": {"item": "PaintedChair", "quantity": 1}
            }
        ]
    }
    assert parser.parse() == expected

def test_script_with_comments_and_blank_lines():
    script_content = """
    module Survival {
        /**
         * Recipe for a basic torch
         */
        recipe "Craft Torch" {
            // Inputs
            keep Rag, // Will be consumed
            TreeBranch,

            // Properties below
            Result:Torch=1, // Output
            Time:10.0, // Crafting time
            Sound:CraftingGeneric -- Sound effect
        }
    }
    // End of module
    """
    parser = RecipeParser(script_content)
    expected = {
        "module": "Survival",
        "recipes": [{
            "name": "Craft Torch",
            "inputs": [
                {"item": "Rag", "alternatives": [], "keep": True, "quantity": None},
                {"item": "TreeBranch", "alternatives": [], "keep": False, "quantity": None}
            ],
            "properties": {"Time": 10.0, "Sound": "CraftingGeneric"},
            "result": {"item": "Torch", "quantity": 1}
        }]
    }
    assert parser.parse() == expected

def test_multiple_recipes_in_module():
    script_content = """
    module Weapons {
        recipe "Sharpen Stick" {
            TreeBranch,
            keep Knife,
            Result:WoodenSpear=1,
            Time:5
        }

        recipe "Craft Makeshift Axe" {
            Stone,
            TreeBranch,
            Rope, // Or Twine, could be an alternative if parser supported it on non-keep
            Result:StoneAxe=1,
            Time:50,
            SkillRequired:Woodwork=0
        }
    }
    """
    parser = RecipeParser(script_content)
    expected = {
        "module": "Weapons",
        "recipes": [
            {
                "name": "Sharpen Stick",
                "inputs": [
                    {"item": "TreeBranch", "alternatives": [], "keep": False, "quantity": None},
                    {"item": "Knife", "alternatives": [], "keep": True, "quantity": None}
                ],
                "properties": {"Time": 5},
                "result": {"item": "WoodenSpear", "quantity": 1}
            },
            {
                "name": "Craft Makeshift Axe",
                "inputs": [
                    {"item": "Stone", "alternatives": [], "keep": False, "quantity": None},
                    {"item": "TreeBranch", "alternatives": [], "keep": False, "quantity": None},
                    {"item": "Rope", "alternatives": [], "keep": False, "quantity": None}
                ],
                "properties": {"Time": 50, "SkillRequired": "Woodwork=0"},
                "result": {"item": "StoneAxe", "quantity": 1}
            }
        ]
    }
    assert parser.parse() == expected

def test_pz_example_script_from_docs():
    test_script_content = """
    module Base {
        recipe "Cut Branches" {
            keep Axe/Machete, // This is a comment
            TreeBranch,

            Result:WoodenStick=4,
            Sound:ChopTree,
            Time:75.0,
            Category:Carpentry,
            SkillRequired:Woodwork=1,
            OnGiveXP:Give5WoodworkXP
        }
    }
    """
    parser = RecipeParser(test_script_content)
    expected = {
        "module": "Base",
        "recipes": [{
            "name": "Cut Branches",
            "inputs": [
                {"item": "Axe", "alternatives": ["Machete"], "keep": True, "quantity": None},
                {"item": "TreeBranch", "alternatives": [], "keep": False, "quantity": None}
            ],
            "properties": {
                "Sound": "ChopTree",
                "Time": 75.0,
                "Category": "Carpentry",
                "SkillRequired": "Woodwork=1",
                "OnGiveXP": "Give5WoodworkXP"
            },
            "result": {"item": "WoodenStick", "quantity": 4}
        }]
    }
    assert parser.parse() == expected

def test_empty_script_recipe_parser():
    script_content = ""
    parser = RecipeParser(script_content)
    expected = {"module": None, "recipes": []}
    assert parser.parse() == expected

def test_script_with_only_comments_recipe_parser():
    script_content = """
    // This is a recipe file with only comments.
    /**
     * No actual recipe definitions here.
     */
    -- Just comments.
    """
    parser = RecipeParser(script_content)
    expected = {"module": None, "recipes": []}
    assert parser.parse() == expected

def test_module_with_no_recipes():
    script_content = """
    module EmptyRecipes {
        // No recipes defined in this module.
    }
    """
    parser = RecipeParser(script_content)
    expected = {"module": "EmptyRecipes", "recipes": []}
    assert parser.parse() == expected

def test_recipe_property_value_types():
    script_content = """
    module PropertyTypesTest {
        recipe TestRecipe {
            InputItem,

            Result:OutputItem=1,
            Time:10, // int
            Heat:50.5, // float
            CanBeDoneFromFloor:true, // bool true
            Obsolete:false, // bool false
            Sound:"MyCustomSound.ogg", // quoted string
            SpecificTool:Base.Screwdriver // item-like string
        }
    }
    """
    parser = RecipeParser(script_content)
    expected = {
        "module": "PropertyTypesTest",
        "recipes": [{
            "name": "TestRecipe",
            "inputs": [{"item": "InputItem", "keep": False, "alternatives": [], "quantity": None}],
            "result": {"item": "OutputItem", "quantity": 1},
            "properties": {
                "Time": 10,
                "Heat": 50.5,
                "CanBeDoneFromFloor": True,
                "Obsolete": False,
                "Sound": "MyCustomSound.ogg",
                "SpecificTool": "Base.Screwdriver"
            }
        }]
    }
    assert parser.parse() == expected

def test_input_item_edge_cases():
    script_content = """
    module EdgeCases {
        recipe EdgeRecipe {
            keep ItemWithNoSpace=1, // keep, item, quantity
            ItemSpaced = 2, // item with space, quantity
            keep ItemWithSpaceAndAlternative / AltItem =3, // keep, item with space, alt, quantity
            "Quoted Item Name" = 4, // Quoted item name with quantity
            keep "Another Quoted/WithSlash" / AndAlternative = 5, // Keep, quoted item with slash, alternative, quantity

            Result:Final=1
        }
    }
    """
    parser = RecipeParser(script_content)
    # Note: Current _parse_input_item might have trouble with spaces in item names before '=' or '/'
    # and with quotes around item names. Let's define expected based on robust parsing.
    # The regex `(.+)=(\d+)` for quantity is greedy.
    # `ItemSpaced = 2` -> line=`ItemSpaced`, quantity=2
    # `keep ItemWithSpaceAndAlternative / AltItem =3`
    #   keep=True, line=`ItemWithSpaceAndAlternative / AltItem =3`
    #   quantity_match on `ItemWithSpaceAndAlternative / AltItem =3` -> group1=`ItemWithSpaceAndAlternative / AltItem`, group2=`3`
    #   line=`ItemWithSpaceAndAlternative / AltItem`, quantity=3
    #   alternatives on `ItemWithSpaceAndAlternative / AltItem` -> item=`ItemWithSpaceAndAlternative`, alts=['AltItem']
    # This seems to work.

    # For quoted item names:
    # `"Quoted Item Name" = 4` -> line=`"Quoted Item Name"`, quantity=4
    #   item=`"Quoted Item Name"`. We might want to unquote this.
    # The current _parse_input_item doesn't explicitly unquote.
    # Let's assume for now it keeps quotes if they are part of the item name.
    # However, PZ scripts typically don't quote simple item names in recipes.

    expected = {
        "module": "EdgeCases",
        "recipes": [{
            "name": "EdgeRecipe",
            "inputs": [
                {"item": "ItemWithNoSpace", "keep": True, "alternatives": [], "quantity": 1},
                {"item": "ItemSpaced", "keep": False, "alternatives": [], "quantity": 2},
                {"item": "ItemWithSpaceAndAlternative", "keep": True, "alternatives": ["AltItem"], "quantity": 3},
                {"item": '"Quoted Item Name"', "keep": False, "alternatives": [], "quantity": 4},
                {"item": '"Another Quoted/WithSlash"', "keep": True, "alternatives": ["AndAlternative"], "quantity": 5},
            ],
            "properties": {},
            "result": {"item": "Final", "quantity": 1}
        }]
    }
    # Let's adjust the expectation for item names to be unquoted if they were quoted,
    # assuming the parser should handle this. The current parser does NOT unquote input item names.
    # So the test needs to expect quoted names if that's what the parser does.
    # The `_attempt_type_conversion` does unquote for properties, but not for input items.
    # Sticking to what the current parser does for inputs:
    assert parser.parse() == expected

def test_recipe_name_with_spaces_unquoted():
    script_content = """
    module TestModule {
        recipe My Recipe With Spaces {
            Ingredient,
            Result:Output=1
        }
    }
    """
    parser = RecipeParser(script_content)
    expected = {
        "module": "TestModule",
        "recipes": [{
            "name": "My Recipe With Spaces",
            "inputs": [{"item": "Ingredient", "keep": False, "alternatives": [], "quantity": None}],
            "properties": {},
            "result": {"item": "Output", "quantity": 1}
        }]
    }
    assert parser.parse() == expected
