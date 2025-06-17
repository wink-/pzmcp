import os
from pydantic import ValidationError
from mcp_server.parsers import ItemParser, RecipeParser, VehicleParser
from .models import ItemModuleData, RecipeModuleData, VehicleModuleData
from .database import engine, insert_item_module_data, insert_recipe_module_data, insert_vehicle_module_data

class DataExtractor:
    def __init__(self, scripts_directory):
        self.scripts_directory = scripts_directory
        # Map parser keys to a tuple of (ParserClass, PydanticModelClass)
        self.parser_model_mapping = {
            "items": (ItemParser, ItemModuleData),
            "recipes": (RecipeParser, RecipeModuleData),
            "vehicles": (VehicleParser, VehicleModuleData),
        }
        # In a real scenario, we might have more complex ways to map files to parsers
        self.file_to_parser_key_mapping = {
            "items.txt": "items",
            "recipes.txt": "recipes",
            "vehicles.txt": "vehicles",
        }

    def extract_all_data(self, validate_with_models=False):
        all_extracted_data = {}
        if not os.path.exists(self.scripts_directory):
            print(f"Error: Scripts directory not found: {self.scripts_directory}")
            return all_extracted_data

        for filename, parser_key in self.file_to_parser_key_mapping.items():
            filepath = os.path.join(self.scripts_directory, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                parser_info = self.parser_model_mapping.get(parser_key)
                if parser_info:
                    parser_class, model_class = parser_info
                    parser = parser_class(content)
                    raw_parsed_data = None
                    validated_model_instance = None

                    try:
                        raw_parsed_data = parser.parse()
                        print(f"Successfully parsed {filename} with {parser_class.__name__}.")

                        if validate_with_models and model_class:
                            try:
                                validated_model_instance = model_class(**raw_parsed_data)
                                # Store the Pydantic model instance directly for DB insertion,
                                # or its dict representation for API response.
                                all_extracted_data[parser_key] = validated_model_instance.model_dump(mode='json')
                                print(f"Successfully validated {filename} with {model_class.__name__}.")
                            except ValidationError as ve:
                                print(f"Validation error for {filename} with {model_class.__name__}: {ve}")
                                all_extracted_data[parser_key] = raw_parsed_data # Store raw if validation fails
                                print(f"Stored raw parsed data for {filename} due to validation error.")
                        else:
                            all_extracted_data[parser_key] = raw_parsed_data
                            if not model_class: print(f"No Pydantic model specified for {parser_key}.")

                        # Database insertion if data is available (either validated or raw)
                        if validated_model_instance: # Prefer validated data for DB
                            data_to_insert = validated_model_instance
                        elif not validate_with_models and raw_parsed_data and model_class:
                            # If not validating, but a model exists, try to create instance for DB
                            try:
                                data_to_insert = model_class(**raw_parsed_data)
                            except ValidationError: # If raw data doesn't fit model, skip DB for this item
                                print(f"Raw data for {filename} not compatible with {model_class.__name__} for DB insertion. Skipping DB.")
                                data_to_insert = None
                        else: # No model or validation failed and storing raw
                            data_to_insert = None
                            print(f"Skipping DB insertion for {filename} as no compatible model instance was prepared.")

                        if data_to_insert:
                            with engine.connect() as connection:
                                try:
                                    if parser_key == "items" and isinstance(data_to_insert, ItemModuleData):
                                        print(f"Preparing and inserting item data into FTS5-enabled table for {filename}...")
                                        insert_item_module_data(connection, data_to_insert)
                                    elif parser_key == "recipes" and isinstance(data_to_insert, RecipeModuleData):
                                        insert_recipe_module_data(connection, data_to_insert)
                                    elif parser_key == "vehicles" and isinstance(data_to_insert, VehicleModuleData):
                                        insert_vehicle_module_data(connection, data_to_insert)
                                    else:
                                        print(f"No specific DB insertion logic for parser key: {parser_key}")
                                    connection.commit()
                                    print(f"Data from {filename} committed to database.")
                                except Exception as db_e:
                                    print(f"Database error for {filename}: {db_e}")
                                    connection.rollback()

                    except Exception as parse_e:
                        print(f"Error parsing {filename} with {parser_class.__name__}: {parse_e}")
                else:
                    print(f"No parser or model info found for {parser_key} (file: {filename})")
            else:
                print(f"File not found: {filepath}")

        return all_extracted_data

if __name__ == "__main__":
    # This is just for demonstration.
    # In a real app, this path would be configured or more dynamic.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    vanilla_scripts_path = os.path.join(current_dir, "..", "data", "vanilla_scripts")
    vanilla_scripts_path = os.path.normpath(vanilla_scripts_path)

    print(f"Attempting to load scripts from: {vanilla_scripts_path}")

    extractor = DataExtractor(vanilla_scripts_path)
    # Demonstrate with validation enabled
    data = extractor.extract_all_data(validate_with_models=True)

    import json
    if data:
        print("\nExtracted Data (after Pydantic validation if applicable):")
        print(json.dumps(data, indent=4)) # Data is already dict from model_dump or raw
    else:
        print("\nNo data extracted or an error occurred.")
