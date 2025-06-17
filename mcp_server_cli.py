import argparse
import os
import sys
import tempfile
import shutil
import logging # Added logging
from typing import Optional

# Assuming these modules are accessible (e.g., in the same directory or Python path)
from data_repository import GameDataRepository # data_repository now uses logging
from data_models import Item, Recipe, Vehicle # For type checking and detailed printing

def print_item_details(item: Optional[Item]):
    if item:
        print(f"Item: {item.itemName}")
        for key, value in item.__dict__.items():
            if key == "itemName":
                continue
            if key == "components" and value:
                print("  Components:")
                for comp_name, comp_obj in value.items():
                    print(f"    {comp_name}:")
                    for ck, cv in comp_obj.__dict__.items():
                        print(f"      {ck}: {cv}")
            else:
                print(f"  {key}: {value}")
    else:
        print("Item not found.")

def print_recipe_details(recipe: Optional[Recipe]):
    if recipe:
        print(f"Recipe: {recipe.recipeName}")
        for key, value in recipe.__dict__.items():
            if key == "recipeName":
                continue
            if key == "inputs" and value:
                print("  Inputs:")
                for i, inp_obj in enumerate(value):
                    print(f"    Input {i+1}:")
                    for ik, iv in inp_obj.__dict__.items():
                        print(f"      {ik}: {iv}")
            elif key == "outputs" and value:
                print("  Outputs:")
                for o, out_obj in enumerate(value):
                    print(f"    Output {o+1}:")
                    for ok, ov in out_obj.__dict__.items():
                        print(f"      {ok}: {ov}")
            elif key == "itemMappers" and value:
                print("  ItemMappers:")
                for mapper_name, mapper_obj in value.items():
                    print(f"    Mapper '{mapper_name}':")
                    for mk, mv in mapper_obj.properties.items():
                         print(f"      {mk}: {mv}")
            else:
                print(f"  {key}: {value}")
    else:
        print("Recipe not found.")

def print_vehicle_details(vehicle: Optional[Vehicle]):
    if vehicle:
        print(f"Vehicle: {vehicle.vehicleName}")
        # Crude print, can be improved by iterating like Item/Recipe
        # or by enhancing __repr__ in data_models
        print(repr(vehicle))
    else:
        print("Vehicle not found.") # User-facing, keep as print

def main():
    # Configure basic logging for the CLI application
    # This will show logs from this module and any underlying modules (parser, transformer, repository)
    # if their log level is INFO or higher.
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    logger = logging.getLogger(__name__) # Logger for CLI specific messages

    parser = argparse.ArgumentParser(description="MCP Server CLI - Game Data Inspector")
    parser.add_argument("script_dir", help="Path to the root script directory.")

    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # Get item command
    getitem_parser = subparsers.add_parser("getitem", help="Get an item by its name (e.g., Base.Apple)")
    getitem_parser.add_argument("name", help="The fully qualified name of the item.")

    # Get recipe command
    getrecipe_parser = subparsers.add_parser("getrecipe", help="Get a recipe by its name")
    getrecipe_parser.add_argument("name", help="The name of the recipe.")

    # Get vehicle command
    getvehicle_parser = subparsers.add_parser("getvehicle", help="Get a vehicle by its name")
    getvehicle_parser.add_argument("name", help="The name of the vehicle.")

    # List commands
    listitems_parser = subparsers.add_parser("listitems", help="List all loaded item names")
    listrecipes_parser = subparsers.add_parser("listrecipes", help="List all loaded recipe names")
    listvehicles_parser = subparsers.add_parser("listvehicles", help="List all loaded vehicle names")

    # (Optional: findrecipes command)
    findrecipes_parser = subparsers.add_parser("findrecipes", help="Find recipes that produce a given item")
    findrecipes_parser.add_argument("item_name", help="The name of the item to find recipes for.")


    args = parser.parse_args()

    if not os.path.isdir(args.script_dir):
        logger.error(f"Script directory '{args.script_dir}' not found or is not a directory.")
        sys.exit(1)

    try:
        # Repository's __init__ now uses logging for its progress/summary.
        # A simple info message here is fine.
        logger.info(f"Attempting to initialize repository with script directory: {args.script_dir}...")
        repo = GameDataRepository(args.script_dir)
        logger.info("Repository initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize GameDataRepository: {e}", exc_info=True)
        sys.exit(1)

    # User-facing output remains print() for direct feedback
    if args.command == "getitem":
        item = repo.get_item_by_name(args.name)
        print_item_details(item)
    elif args.command == "getrecipe":
        recipe = repo.get_recipe_by_name(args.name)
        print_recipe_details(recipe)
    elif args.command == "getvehicle":
        vehicle = repo.get_vehicle_by_name(args.name)
        print_vehicle_details(vehicle) # Uses basic repr for now
    elif args.command == "listitems":
        print("\nAll Item Names:")
        all_items = repo.get_all_items()
        if all_items:
            for item in all_items:
                print(item.itemName)
        else:
            print("No items loaded.")
    elif args.command == "listrecipes":
        print("\nAll Recipe Names:")
        all_recipes = repo.get_all_recipes()
        if all_recipes:
            for recipe in all_recipes:
                print(recipe.recipeName)
        else:
            print("No recipes loaded.")
    elif args.command == "listvehicles":
        print("\nAll Vehicle Names:")
        all_vehicles = repo.get_all_vehicles()
        if all_vehicles:
            for vehicle in all_vehicles:
                print(vehicle.vehicleName)
        else:
            print("No vehicles loaded.")
    elif args.command == "findrecipes":
        print(f"\nRecipes producing item '{args.item_name}':")
        found_count = 0
        for recipe in repo.get_all_recipes():
            for output in recipe.outputs:
                if output.name == args.item_name:
                    print(f"- {recipe.recipeName}")
                    found_count +=1
                    break # Avoid listing same recipe multiple times if it produces the item multiple ways
        if found_count == 0:
            print(f"No recipes found that produce '{args.item_name}'.")

if __name__ == '__main__':
    # --- Test Harness for CLI ---
    # This section sets up a temporary script directory with mock files
    # and then invokes the main() function with arguments as if run from command line.

    original_argv = sys.argv # Store original command line arguments

    mock_scripts_content = {
        "mock_scripts/globals/global_items.txt": """
            item ToolRack { DisplayName = "Tool Rack"; Type = Placeable; }
        """,
        "mock_scripts/base/base_items.txt": """
            module Base {
                item Apple { DisplayName = "Red Apple"; Type = Food; Weight = 0.1; }
                item IronIngot { DisplayName = "Iron Ingot"; Type = Material; Weight = 1.0; }
                item IronOre { DisplayName = "Iron Ore"; Type = Material; Weight = 1.5; }
            }
        """,
        "mock_scripts/base/recipes/metal_recipes.txt": """
            craftRecipe SmeltIronOre {
                Time = 10; category = Smelting;
                inputs { item 2 Base.IronOre; }
                outputs { item 1 Base.IronIngot; }
            }
            craftRecipe CraftAnvil {
                Time = 100; category = Blacksmithing;
                inputs { item 10 Base.IronIngot; }
                outputs { item 1 Base.Anvil; } // Assuming Base.Anvil is an item
            }
        """,
        "mock_scripts/vehicles/cars.txt": """
            vehicle SmallCar {
                mass = 700; engineForce = 3000;
                model { file = "vehicles/small_car.mdl"; }
                passenger Driver { offset = 0 0.5 0; }
            }
        """
    }

    test_dir = tempfile.mkdtemp(prefix="mcp_cli_test_")
    # Using a module-level logger for test harness messages
    test_harness_logger = logging.getLogger("CLITestHarness")

    test_harness_logger.info(f"Created temporary test directory: {test_dir}")

    mock_script_root_for_cli = os.path.join(test_dir, "mock_scripts")

    for rel_path, content in mock_scripts_content.items():
        abs_path = os.path.join(test_dir, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)

    # --- Test cases for error logging ---
    # 1. Non-existent directory
    non_existent_dir = os.path.join(test_dir, "non_existent_scripts")

    # 2. Malformed script file
    malformed_script_path = os.path.join(mock_script_root_for_cli, "malformed_script.txt")
    with open(malformed_script_path, 'w', encoding='utf-8') as f:
        f.write("item MalformedItem { BadSyntax = = ; }") # Known syntax error

    test_commands = [
        # Valid commands (should show INFO logs from repository)
        {"args": ["getitem", "Base.Apple"], "desc": "Get existing item"},
        {"args": ["listitems"], "desc": "List items"},
        # Command that should result in "not found" (printed to stdout, not an error log)
        {"args": ["getitem", "NonExistent.Item"], "desc": "Get non-existent item"},
        # Command that should use a malformed script (repository should log an error)
        # Note: The CLI test harness runs GameDataRepository for each command.
        # To test malformed file in isolation, we could create a separate script_dir for it.
        # For now, the malformed file will be part of the scanned files for all commands.
        # This means the "malformed_script.txt" error will appear multiple times.
        {"args": ["listrecipes"], "desc": "List recipes (malformed file will be processed)"},
    ]

    # Test for non-existent directory separately as it exits
    test_harness_logger.info(f"\n\n[CLI Test Harness] Running command with non-existent directory: mcp_server_cli.py {non_existent_dir} listitems")
    sys.argv = [sys.executable] + [non_existent_dir] + ["listitems"]
    try:
        main()
    except SystemExit as e:
        test_harness_logger.info(f"[CLI Test Harness] SystemExit: {e.code if e.code is not None else 'N/A'} (expected for non-existent dir)")
    except Exception as e:
        test_harness_logger.error(f"[CLI Test Harness] Unhandled Exception: {e}", exc_info=True)
    test_harness_logger.info("-" * 40)


    for i, test_case in enumerate(test_commands):
        cmd_args = test_case["args"]
        desc = test_case["desc"]
        test_harness_logger.info(f"\n\n[CLI Test Harness] ({i+1}) Running command ({desc}): {' '.join(['mcp_server_cli.py', mock_script_root_for_cli] + cmd_args)}")
        sys.argv = [sys.executable] + [mock_script_root_for_cli] + cmd_args
        try:
            main()
        except SystemExit as e: # argparse can cause SystemExit for --help etc.
            test_harness_logger.info(f"[CLI Test Harness] SystemExit: {e.code if e.code is not None else 'N/A'}")
        except Exception as e:
            test_harness_logger.error(f"[CLI Test Harness] Unhandled Exception: {e}", exc_info=True)
        test_harness_logger.info("-" * 40)

    # Restore original argv and clean up
    sys.argv = original_argv
    test_harness_logger.info(f"Cleaning up temporary test directory: {test_dir}")
    shutil.rmtree(test_dir)
    test_harness_logger.info("Test complete.")
