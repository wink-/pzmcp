import os
import logging
from pathlib import Path
from pydantic import ValidationError
from mcp_server.parsers import ItemParser, RecipeParser, VehicleParser
from .models import ItemModuleData, RecipeModuleData, VehicleModuleData
from .database import engine, insert_item_module_data, insert_recipe_module_data, insert_vehicle_module_data

# Import the path manager from project root
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from pz_path_manager import PZPathManager

logger = logging.getLogger(__name__)

class EnhancedDataExtractor:
    """Enhanced data extractor that uses PZ path manager for flexible script discovery"""
    
    def __init__(self, scripts_directory=None, use_path_manager=True):
        self.use_path_manager = use_path_manager
        
        if use_path_manager and scripts_directory is None:
            # Use path manager to find best scripts directory
            try:
                self.path_manager = PZPathManager()
                self.scripts_directory = self.path_manager.get_scripts_directory()
                logger.info(f"Using scripts directory from path manager: {self.scripts_directory}")
            except Exception as e:
                logger.error(f"Path manager failed: {e}")
                self.scripts_directory = "./media/scripts"  # fallback
        else:
            self.scripts_directory = scripts_directory or "./media/scripts"
            self.path_manager = None
        
        # Map parser keys to a tuple of (ParserClass, PydanticModelClass)
        self.parser_model_mapping = {
            "items": (ItemParser, ItemModuleData),
            "recipes": (RecipeParser, RecipeModuleData),
            "vehicles": (VehicleParser, VehicleModuleData),
        }
        
        # Enhanced file mapping - supports both individual files and directories
        self.file_to_parser_key_mapping = {
            "items.txt": "items",
            "recipes.txt": "recipes", 
            "vehicles.txt": "vehicles",
            # Directory mappings for comprehensive extraction
            "items/": "items",
            "recipes/": "recipes",
            "vehicles/": "vehicles",
        }

    def extract_all_data(self, validate_with_models=False, comprehensive=True):
        """
        Extract all data from scripts directory
        
        Args:
            validate_with_models: Whether to validate with Pydantic models
            comprehensive: If True, process individual files in subdirectories
        """
        all_extracted_data = {}
        
        if not os.path.exists(self.scripts_directory):
            logger.error(f"Scripts directory not found: {self.scripts_directory}")
            return all_extracted_data
        
        logger.info(f"Starting data extraction from: {self.scripts_directory}")
        
        if comprehensive:
            return self._extract_comprehensive_data(validate_with_models)
        else:
            return self._extract_basic_data(validate_with_models)
    
    def _extract_comprehensive_data(self, validate_with_models=False):
        """Extract data from all relevant files in subdirectories"""
        all_extracted_data = {}
        processed_counts = {"items": 0, "recipes": 0, "vehicles": 0}
        
        # Process items directory
        items_dir = os.path.join(self.scripts_directory, "items")
        if os.path.exists(items_dir):
            items_count = self._process_directory(items_dir, "items", validate_with_models)
            processed_counts["items"] = items_count
            logger.info(f"Processed {items_count} item files")
        
        # Process recipes directory
        recipes_dir = os.path.join(self.scripts_directory, "recipes")
        if os.path.exists(recipes_dir):
            recipes_count = self._process_directory(recipes_dir, "recipes", validate_with_models)
            processed_counts["recipes"] = recipes_count
            logger.info(f"Processed {recipes_count} recipe files")
        
        # Process vehicles directory
        vehicles_dir = os.path.join(self.scripts_directory, "vehicles")
        if os.path.exists(vehicles_dir):
            vehicles_count = self._process_directory(vehicles_dir, "vehicles", validate_with_models)
            processed_counts["vehicles"] = vehicles_count
            logger.info(f"Processed {vehicles_count} vehicle files")
        
        # Also process main files if they exist
        for filename, parser_key in self.file_to_parser_key_mapping.items():
            if not filename.endswith("/"):  # Skip directory entries
                filepath = os.path.join(self.scripts_directory, filename)
                if os.path.exists(filepath):
                    self._process_single_file(filepath, filename, parser_key, validate_with_models)
        
        all_extracted_data["summary"] = processed_counts
        return all_extracted_data
    
    def _process_directory(self, directory_path, parser_key, validate_with_models):
        """Process all .txt files in a directory"""
        count = 0
        
        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                filepath = os.path.join(directory_path, filename)
                try:
                    self._process_single_file(filepath, filename, parser_key, validate_with_models)
                    count += 1
                except Exception as e:
                    logger.error(f"Failed to process {filepath}: {e}")
        
        return count
    
    def _process_single_file(self, filepath, filename, parser_key, validate_with_models):
        """Process a single script file"""
        parser_info = self.parser_model_mapping.get(parser_key)
        if not parser_info:
            logger.warning(f"No parser found for key: {parser_key}")
            return
        
        parser_class, model_class = parser_info
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parser = parser_class(content)
            raw_parsed_data = parser.parse()
            
            # Check if any data was actually parsed
            data_key = f"{parser_key[:-1] if parser_key.endswith('s') else parser_key}s"  # items, recipes, vehicles
            if not raw_parsed_data.get(data_key):
                logger.debug(f"No {parser_key} found in {filename}")
                return
            
            logger.debug(f"Successfully parsed {filename} with {parser_class.__name__}")
            
            # Create model instance for database insertion
            if validate_with_models:
                try:
                    validated_model_instance = model_class(**raw_parsed_data)
                    data_to_insert = validated_model_instance
                    logger.debug(f"Successfully validated {filename} with {model_class.__name__}")
                except ValidationError as ve:
                    logger.warning(f"Validation error for {filename}: {ve}")
                    # Try to create model without validation for DB insertion
                    try:
                        data_to_insert = model_class(**raw_parsed_data)
                    except:
                        logger.error(f"Cannot create model instance for {filename}")
                        return
            else:
                try:
                    data_to_insert = model_class(**raw_parsed_data)
                except ValidationError:
                    logger.error(f"Raw data for {filename} not compatible with {model_class.__name__}")
                    return
            
            # Insert into database
            if data_to_insert:
                with engine.connect() as connection:
                    try:
                        if parser_key == "items" and isinstance(data_to_insert, ItemModuleData):
                            insert_item_module_data(connection, data_to_insert)
                        elif parser_key == "recipes" and isinstance(data_to_insert, RecipeModuleData):
                            insert_recipe_module_data(connection, data_to_insert)
                        elif parser_key == "vehicles" and isinstance(data_to_insert, VehicleModuleData):
                            insert_vehicle_module_data(connection, data_to_insert)
                        
                        connection.commit()
                        
                        # Log count of items inserted
                        items_count = len(raw_parsed_data.get(data_key, []))
                        if items_count > 0:
                            logger.debug(f"Inserted {items_count} {parser_key} from {filename}")
                        
                    except Exception as db_e:
                        logger.error(f"Database error for {filename}: {db_e}")
                        connection.rollback()
        
        except Exception as e:
            logger.error(f"Error processing {filepath}: {e}")
    
    def _extract_basic_data(self, validate_with_models=False):
        """Basic extraction using original DataExtractor logic"""
        all_extracted_data = {}
        
        for filename, parser_key in self.file_to_parser_key_mapping.items():
            if filename.endswith("/"):  # Skip directory entries
                continue
                
            filepath = os.path.join(self.scripts_directory, filename)
            if os.path.exists(filepath):
                self._process_single_file(filepath, filename, parser_key, validate_with_models)
            else:
                logger.debug(f"File not found: {filepath}")
        
        return all_extracted_data
    
    def get_path_info(self):
        """Get information about the scripts path being used"""
        info = {
            "scripts_directory": self.scripts_directory,
            "using_path_manager": self.use_path_manager,
            "exists": os.path.exists(self.scripts_directory)
        }
        
        if self.path_manager:
            path, source = self.path_manager.find_pz_scripts_directory()
            info.update({
                "detected_path": path,
                "source": source,
                "available_paths": self.path_manager.list_available_paths()
            })
        
        return info

# Convenience function for backward compatibility
def extract_with_path_manager(comprehensive=True, validate_with_models=False):
    """Extract data using the path manager system"""
    extractor = EnhancedDataExtractor(use_path_manager=True)
    return extractor.extract_all_data(validate_with_models=validate_with_models, 
                                     comprehensive=comprehensive)