from typing import Dict, List, Any
import logging # Added logging
from data_models import (
    Item, Recipe, RecipeInput, RecipeOutput,
    Vehicle, VehicleModel, VehicleTemplate, ModelComponent
    # VehicleSubBlock and its children are mostly handled by VehicleDefinition's init
)

logger = logging.getLogger(__name__) # Setup logger

def transform_item(item_dict: Dict[str, Any]) -> Item:
    # itemName is mandatory and passed directly to constructor
    # Other properties are passed as kwargs
    return Item(**item_dict)

def transform_recipe(recipe_dict: Dict[str, Any]) -> Recipe:
    # Make a copy to modify (pop inputs/outputs)
    recipe_data_copy = recipe_dict.copy()

    raw_inputs = recipe_data_copy.pop('inputs', [])
    raw_outputs = recipe_data_copy.pop('outputs', [])

    # recipeName is mandatory
    recipe_obj = Recipe(**recipe_data_copy)

    for input_data in raw_inputs:
        recipe_obj.inputs.append(RecipeInput(**input_data))

    for output_data in raw_outputs:
        recipe_obj.outputs.append(RecipeOutput(**output_data))

    # ItemMappers are already handled by Recipe.__init__ if parser nests them well
    return recipe_obj

def transform_vehicle(vehicle_dict: Dict[str, Any]) -> Vehicle:
    return Vehicle(**vehicle_dict)

def transform_vehicle_model(model_dict: Dict[str, Any]) -> VehicleModel:
    return VehicleModel(**model_dict)

def transform_vehicle_template(template_dict: Dict[str, Any]) -> VehicleTemplate:
    return VehicleTemplate(**template_dict)


def transform_parsed_data(parsed_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Any]]:
    """
    Transforms the entire parsed data dictionary into a dictionary of data model object lists.
    """
    transformed_data = {
        "items": [],
        "recipes": [],
        "vehicles": [],
        "vehicle_models": [],
        "vehicle_templates": []
    }

    if "items" in parsed_data:
        for item_dict in parsed_data["items"]:
            item_name_for_log = item_dict.get('itemName', 'UnknownItem')
            try:
                transformed_data["items"].append(transform_item(item_dict))
            except Exception as e:
                logger.error(f"Error transforming item '{item_name_for_log}': {e}", exc_info=True)

    if "recipes" in parsed_data:
        for recipe_dict in parsed_data["recipes"]:
            recipe_name_for_log = recipe_dict.get('recipeName', 'UnknownRecipe')
            try:
                transformed_data["recipes"].append(transform_recipe(recipe_dict))
            except Exception as e:
                logger.error(f"Error transforming recipe '{recipe_name_for_log}': {e}", exc_info=True)

    if "vehicles" in parsed_data:
        for vehicle_dict in parsed_data["vehicles"]:
            vehicle_name_for_log = vehicle_dict.get('vehicleName', 'UnknownVehicle')
            try:
                transformed_data["vehicles"].append(transform_vehicle(vehicle_dict))
            except Exception as e:
                logger.error(f"Error transforming vehicle '{vehicle_name_for_log}': {e}", exc_info=True)

    if "vehicle_models" in parsed_data:
        for model_dict in parsed_data["vehicle_models"]:
            model_name_for_log = model_dict.get('modelName', 'UnknownModel')
            try:
                transformed_data["vehicle_models"].append(transform_vehicle_model(model_dict))
            except Exception as e:
                logger.error(f"Error transforming vehicle model '{model_name_for_log}': {e}", exc_info=True)

    if "vehicle_templates" in parsed_data:
        for template_dict in parsed_data["vehicle_templates"]:
            template_name_for_log = template_dict.get('templateName', 'UnknownTemplate')
            try:
                transformed_data["vehicle_templates"].append(transform_vehicle_template(template_dict))
            except Exception as e:
                logger.error(f"Error transforming vehicle template '{template_name_for_log}': {e}", exc_info=True)

    return transformed_data

if __name__ == '__main__':
    # Configure basic logging for standalone transformer testing
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    logger.info("--- Data Transformer Example ---") # Changed print to logger.info

    dummy_parsed_data = {
        "items": [
            {"itemName": "TestTowel", "DisplayName": "Test Towel", "Type": "Normal", "Weight": 0.2,
             "component Fabric": {"Density": 10, "Material": "Cotton"}}
        ],
        "recipes": [
            {
                "recipeName": "CraftTestTowel", "Time": 60, "category": "Tailoring",
                "inputs": [
                    {"type": "item", "quantity": 2, "name": "Base.CottonFabric"},
                    {"type": "item", "quantity": 1, "name": "Base.Needle", "mode": "keep"}
                ],
                "outputs": [
                    {"type": "item", "quantity": 1, "name": "TestTowel"}
                ],
                "itemMapper BonusOutput": {"Default": "Base.Nothing"}
            }
        ],
        "vehicles": [
            {
                "vehicleName": "TestCar", "mass": 1000, "engineForce": 5000,
                "model": {"file": "Vehicles/TestCar_model.fbx"}, # Anonymous model
                "passenger": [{"_name": "Driver", "offset": [0, 0.5, 0], "type": "DriverSeat"}]
            }
        ],
        "vehicle_models": [
            {"modelName": "GlobalTestModel", "file": "Global/Models/Test.mdl", "scale": 1.0}
        ],
        "vehicle_templates": [
            {"templateName": "BasicCarFrame", "mass": 500, "part": [{"_name": "Frame", "health": 200}]}
        ]
    }

    transformed_objects = transform_parsed_data(dummy_parsed_data)

    logger.info("\n--- Transformed Items ---") # Changed print
    for item_obj in transformed_objects["items"]:
        logger.info(repr(item_obj)) # Changed print

    logger.info("\n--- Transformed Recipes ---") # Changed print
    for recipe_obj in transformed_objects["recipes"]:
        logger.info(repr(recipe_obj)) # Changed print
        for inp in recipe_obj.inputs:
            logger.info(f"  Input: {repr(inp)}") # Changed print
        for outp in recipe_obj.outputs:
            logger.info(f"  Output: {repr(outp)}") # Changed print
        for mapper_name, mapper_obj in recipe_obj.itemMappers.items():
            logger.info(f"  Mapper '{mapper_name}': {repr(mapper_obj)}") # Changed print


    logger.info("\n--- Transformed Vehicles ---") # Changed print
    for vehicle_obj in transformed_objects["vehicles"]:
        logger.info(repr(vehicle_obj)) # Changed print

    logger.info("\n--- Transformed Vehicle Models ---") # Changed print
    for model_obj in transformed_objects["vehicle_models"]:
        logger.info(repr(model_obj)) # Changed print

    logger.info("\n--- Transformed Vehicle Templates ---") # Changed print
    for template_obj in transformed_objects["vehicle_templates"]:
        logger.info(repr(template_obj)) # Changed print

    logger.info("\n--- Example of accessing transformed data ---") # Changed print
    if transformed_objects["items"]:
        first_item = transformed_objects["items"][0]
        logger.info(f"First item name: {first_item.itemName}") # Changed print
        if hasattr(first_item, 'DisplayName'):
            logger.info(f"First item DisplayName: {first_item.DisplayName}") # Changed print
        if first_item.components:
            logger.info(f"First item components: {first_item.components}") # Changed print
            if "Fabric" in first_item.components:
                 logger.info(f"Fabric Density: {first_item.components['Fabric'].Density}") # Changed print


    if transformed_objects["vehicles"]:
        first_vehicle = transformed_objects["vehicles"][0]
        logger.info(f"First vehicle name: {first_vehicle.vehicleName}") # Changed print
        if first_vehicle.model:
            logger.info(f"First vehicle model file: {first_vehicle.model.file}") # Changed print
        if first_vehicle.passengers:
            logger.info(f"First vehicle passenger name: {first_vehicle.passengers[0]._name}") # Changed print
            logger.info(f"First vehicle passenger offset: {first_vehicle.passengers[0].offset}") # Changed print

    # Example with error (missing mandatory field for a class if its __init__ was stricter)
    dummy_parsed_data_error = {
         "items": [{"DisplayName": "Incomplete Item"}] # Missing itemName
    }
    logger.info("\n--- Test Error Handling (Example) ---") # Changed print
    transformed_error_data = transform_parsed_data(dummy_parsed_data_error)
    # Error for item 'UnknownItem' should be logged by transform_parsed_data
    # logger.info(transformed_error_data["items"])
