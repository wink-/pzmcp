import os
import logging # Added logging
from typing import Dict, List, Optional, Any

# Assuming these modules and classes are in the same Python environment
# and accessible via PYTHONPATH or relative imports if structured as a package.
# For simplicity, direct imports are used here, assuming files are in the same root.
import script_parser # script_parser now uses logging for its errors
import data_transformer # data_transformer now uses logging for its errors
from data_models import (
    Item, Recipe, Vehicle, VehicleModel, VehicleTemplate
)

logger = logging.getLogger(__name__) # Setup logger for this module

class GameDataRepository:
    def __init__(self, script_root_path: str):
        self.script_root_path: str = script_root_path

        self.all_items: List[Item] = []
        self.items_by_name: Dict[str, Item] = {}

        self.all_recipes: List[Recipe] = []
        self.recipes_by_name: Dict[str, Recipe] = {}

        self.all_vehicles: List[Vehicle] = []
        self.vehicles_by_name: Dict[str, Vehicle] = {}

        self.all_vehicle_models: List[VehicleModel] = []
        self.vehicle_models_by_name: Dict[str, VehicleModel] = {}

        self.all_vehicle_templates: List[VehicleTemplate] = []
        self.vehicle_templates_by_name: Dict[str, VehicleTemplate] = {}

        self._load_data()

    def _load_data(self):
        """
        Walks the script_root_path, finds .txt files, parses them,
        transforms the data, and populates the repository.
        """
        for root, _, files in os.walk(self.script_root_path):
            for filename in files:
                if filename.endswith(".txt"): # Assuming script files are .txt
                    filepath = os.path.join(root, filename)
                    logger.info(f"Attempting to load script file: {filepath}")
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()

                        if not content.strip(): # Skip empty or whitespace-only files
                            logger.info(f"Skipping empty file: {filepath}")
                            continue

                        # script_parser and data_transformer now use their own loggers for internal errors
                        parsed_data_dict = script_parser.parse_script(content)
                        transformed_data_objects = data_transformer.transform_parsed_data(parsed_data_dict)

                        for item_obj in transformed_data_objects.get("items", []):
                            if item_obj.itemName in self.items_by_name:
                                logger.warning(f"Duplicate item name '{item_obj.itemName}' found in {filepath}. Overwriting previous entry.")
                            self.all_items.append(item_obj)
                            self.items_by_name[item_obj.itemName] = item_obj

                        for recipe_obj in transformed_data_objects.get("recipes", []):
                            if recipe_obj.recipeName in self.recipes_by_name:
                                logger.warning(f"Duplicate recipe name '{recipe_obj.recipeName}' found in {filepath}. Overwriting previous entry.")
                            self.all_recipes.append(recipe_obj)
                            self.recipes_by_name[recipe_obj.recipeName] = recipe_obj

                        for vehicle_obj in transformed_data_objects.get("vehicles", []):
                            if vehicle_obj.vehicleName in self.vehicles_by_name:
                                logger.warning(f"Duplicate vehicle name '{vehicle_obj.vehicleName}' found in {filepath}. Overwriting previous entry.")
                            self.all_vehicles.append(vehicle_obj)
                            self.vehicles_by_name[vehicle_obj.vehicleName] = vehicle_obj

                        for model_obj in transformed_data_objects.get("vehicle_models", []):
                            if model_obj.modelName in self.vehicle_models_by_name:
                                logger.warning(f"Duplicate vehicle model name '{model_obj.modelName}' found in {filepath}. Overwriting previous entry.")
                            self.all_vehicle_models.append(model_obj)
                            self.vehicle_models_by_name[model_obj.modelName] = model_obj

                        for template_obj in transformed_data_objects.get("vehicle_templates", []):
                            if template_obj.templateName in self.vehicle_templates_by_name:
                                logger.warning(f"Duplicate vehicle template name '{template_obj.templateName}' found in {filepath}. Overwriting previous entry.")
                            self.all_vehicle_templates.append(template_obj)
                            self.vehicle_templates_by_name[template_obj.templateName] = template_obj

                        logger.info(f"Successfully loaded and processed: {filepath}")

                    except FileNotFoundError:
                        logger.error(f"File not found: {filepath}. Skipping.")
                    except UnicodeDecodeError:
                        logger.error(f"Could not decode file {filepath} as UTF-8. Skipping.")
                    except script_parser.SyntaxError as e: # script_parser.SyntaxError is alias for CustomParserSyntaxError
                        logger.error(f"Syntax error parsing file {filepath}: {e}. Skipping.")
                    except Exception as e: # Catch-all for other errors during file processing (e.g. transformation errors not caught internally by transformer)
                        logger.exception(f"An unexpected error occurred processing file {filepath}: {e}. Skipping.") # Use .exception to include stack trace

        logger.info("Data loading process complete.")
        logger.info(f"Loaded {len(self.all_items)} items.")
        logger.info(f"Loaded {len(self.all_recipes)} recipes.")
        logger.info(f"Loaded {len(self.all_vehicles)} vehicles.")
        logger.info(f"Loaded {len(self.all_vehicle_models)} vehicle models.")
        logger.info(f"Loaded {len(self.all_vehicle_templates)} vehicle templates.")

    # --- Getter Methods ---
    def get_item_by_name(self, name: str) -> Optional[Item]:
        return self.items_by_name.get(name)

    def get_recipe_by_name(self, name: str) -> Optional[Recipe]:
        return self.recipes_by_name.get(name)

    def get_vehicle_by_name(self, name: str) -> Optional[Vehicle]:
        return self.vehicles_by_name.get(name)

    def get_vehicle_model_by_name(self, name: str) -> Optional[VehicleModel]:
        return self.vehicle_models_by_name.get(name)

    def get_vehicle_template_by_name(self, name: str) -> Optional[VehicleTemplate]:
        return self.vehicle_templates_by_name.get(name)

    def get_all_items(self) -> List[Item]:
        return self.all_items

    def get_all_recipes(self) -> List[Recipe]:
        return self.all_recipes

    def get_all_vehicles(self) -> List[Vehicle]:
        return self.all_vehicles

    def get_all_vehicle_models(self) -> List[VehicleModel]:
        return self.all_vehicle_models

    def get_all_vehicle_templates(self) -> List[VehicleTemplate]:
        return self.all_vehicle_templates


if __name__ == '__main__':
    # Configure basic logging for standalone repository testing
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    logger.info("--- GameDataRepository Test ---") # Changed print

    # Store original os.walk and open
    original_os_walk = os.walk
    # Using original_open = open is problematic if 'open' is not imported. 'builtins.open' is better.
    # However, the test setup uses 'with open(...)' for writing, which is fine.

    # Define mock script content
    mock_scripts_content = {
        "mock_scripts/items/base_items.txt": """
            module Base {
                item Apple { DisplayName = "Red Apple"; Type = Food; Weight = 0.1; }
                item IronIngot { DisplayName = "Iron Ingot"; Type = Material; Weight = 1.0; }
            }
        """,
        "mock_scripts/recipes/metal_recipes.txt": """
            craftRecipe SmeltIronOre {
                Time = 10; category = Smelting;
                inputs { item 2 Base.IronOre; }
                outputs { item 1 Base.IronIngot; }
            }
        """,
        "mock_scripts/vehicles/cars.txt": """
            vehicle SmallCar {
                mass = 700; engineForce = 3000;
                model { file = "vehicles/small_car.mdl"; }
                passenger Driver { offset = 0 0.5 0; }
            }
            model GlobalCarModel { file = "vehicles/global_car_model.mdl"; scale = 1.0; }
            template vehicle BasicCarTemplate { mass = 600; }
        """
    }

    def mock_os_walk(path, topdown=True, onerror=None, followlinks=False):
        # Simplified mock: assumes path is "mock_scripts" and yields one level
        if path == "mock_scripts":
            dir_structure = {
                "mock_scripts": (["items", "recipes", "vehicles"], []),
                "mock_scripts/items": ([], ["base_items.txt"]),
                "mock_scripts/recipes": ([], ["metal_recipes.txt"]),
                "mock_scripts/vehicles": ([], ["cars.txt"]),
            }
            for root_dir, (dirs, files_in_dir) in dir_structure.items():
                 # Adjust root_dir to be relative to the initial path for the walk results
                if root_dir.startswith(path): # Ensure we are under the initial path
                    yield (root_dir, dirs, files_in_dir)
        else:
            yield from original_os_walk(path, topdown, onerror, followlinks)


    def mock_open_file(filepath, mode='r', encoding=None):
        # Normalize path for dictionary lookup
        normalized_filepath = filepath.replace("\\", "/")
        if normalized_filepath in mock_scripts_content:
            import io
            if mode == 'r' or mode == 'rt':
                return io.StringIO(mock_scripts_content[normalized_filepath])
            elif mode == 'rb': # Not used here, but for completeness
                return io.BytesIO(mock_scripts_content[normalized_filepath].encode(encoding or 'utf-8'))
        # If file not in mock, fallback or raise error
        # For this test, if it's not a mock path, it's an error or unhandled.
        # We could use `original_open` for real files if needed and if paths are not mock paths.
        raise FileNotFoundError(f"Mock file not found: {filepath}")

    # Apply mocks
    os.walk = mock_os_walk
    # __builtins__.open is the typical way to mock open, but direct assignment works if 'open' is imported as 'open'
    # For this script, 'open' is a builtin so this might be tricky.
    # A better way for 'open' is often `unittest.mock.patch('builtins.open', new=mock_open_file)`
    # but let's try direct assignment for this environment.
    # If 'open' is used directly without importing 'io', this won't work.
    # The code uses `with open(...)`, which refers to the built-in.
    # Let's assume for now the environment might pick up a local 'open' if we define it,
    # or that the test will use a path that the mock_os_walk handles and mock_open_file intercepts.
    # This part is tricky without `unittest.mock`.
    # For now, the `_load_data` method will be tested by how `os.walk` and `open` are used within it.
    # The `open` mock needs to be correctly patched. Let's assume script_parser uses io.open or similar if this fails.
    # The repository uses `with open(...)` which is `builtins.open`.

    # To properly mock 'open', we'd usually use a context manager or a library like unittest.mock.
    # Let's adjust the test to create a temporary directory and files instead of complex mocking of open.
    # This makes the test more reliant on file system but simpler mock-wise.

    # Create a temporary directory structure for testing
    import tempfile
    import shutil

    test_dir = tempfile.mkdtemp(prefix="gamedata_repo_test_")
    logger.info(f"Created temporary test directory: {test_dir}")

    mock_script_root = os.path.join(test_dir, "mock_scripts")
    os.makedirs(mock_script_root, exist_ok=True)

    # Using original_open from earlier capture for writing test files
    # This assumes 'original_open' correctly refers to 'builtins.open' if it was captured before any mock.
    # If 'open' was not explicitly imported, 'open' inside a function refers to 'builtins.open'.
    for rel_path, content in mock_scripts_content.items():
        abs_path = os.path.join(test_dir, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, 'w', encoding='utf-8') as f: # Use built-in open for writing
            f.write(content)

    # Restore os.walk for the GameDataRepository to use the real one on the temp dir.
    os.walk = original_os_walk

    try:
        repo = GameDataRepository(script_root_path=mock_script_root)

        logger.info("\n--- Repository Getter Tests ---") # Changed print
        apple = repo.get_item_by_name("Base.Apple")
        logger.info(f"Apple: {apple}") # Changed print

        non_existent_item = repo.get_item_by_name("NonExistent.Item")
        logger.info(f"NonExistent.Item: {non_existent_item}") # Changed print

        smelt_recipe = repo.get_recipe_by_name("SmeltIronOre")
        logger.info(f"SmeltIronOre Recipe: {smelt_recipe}") # Changed print
        if smelt_recipe:
            logger.info(f"  Inputs: {smelt_recipe.inputs}") # Changed print
            logger.info(f"  Outputs: {smelt_recipe.outputs}") # Changed print

        small_car = repo.get_vehicle_by_name("SmallCar")
        logger.info(f"SmallCar Vehicle: {small_car}") # Changed print
        if small_car:
            logger.info(f"  Model: {small_car.model}") # Changed print
            logger.info(f"  Passengers: {small_car.passengers}") # Changed print

        global_car_model = repo.get_vehicle_model_by_name("GlobalCarModel")
        logger.info(f"GlobalCarModel: {global_car_model}") # Changed print

        basic_car_template = repo.get_vehicle_template_by_name("BasicCarTemplate")
        logger.info(f"BasicCarTemplate: {basic_car_template}") # Changed print

        logger.info(f"\nTotal items loaded: {len(repo.get_all_items())}") # Changed print
        # logger.info(f"All items: {repo.get_all_items()}")

    except Exception as e:
        logger.exception(f"Error during repository test: {e}") # Changed print to logger.exception
    finally:
        # Clean up the temporary directory
        logger.info(f"Cleaning up temporary test directory: {test_dir}") # Changed print
        shutil.rmtree(test_dir)

    logger.info("\n--- GameDataRepository Test Complete ---") # Changed print
