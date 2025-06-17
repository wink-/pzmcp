from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field

# --- Common ---
class BaseModuleData(BaseModel):
    module: Optional[str] = None

# --- Item Models ---
class ParsedItem(BaseModel):
    name: str
    properties: Dict[str, Any] = Field(default_factory=dict)

class ItemModuleData(BaseModuleData):
    imports: List[str] = Field(default_factory=list) # Item scripts can have imports
    items: List[ParsedItem] = Field(default_factory=list)

# --- Recipe Models ---
class RecipeInputItem(BaseModel):
    item: str
    keep: bool = False
    alternatives: List[str] = Field(default_factory=list)
    quantity: Optional[int] = None

class RecipeResult(BaseModel):
    item: str
    quantity: Optional[int] = 1 # Default from parser

class ParsedRecipe(BaseModel):
    name: str
    inputs: List[RecipeInputItem] = Field(default_factory=list)
    properties: Dict[str, Any] = Field(default_factory=dict)
    result: Optional[RecipeResult] = None

class RecipeModuleData(BaseModuleData):
    recipes: List[ParsedRecipe] = Field(default_factory=list)

# --- Vehicle Models ---
# Using Any for properties initially, can be refined if common properties are typed
class VehiclePropertyBlock(BaseModel): # Generic block for model, skin, sound, lua, container, table install/uninstall
    properties: Dict[str, Any] = Field(default_factory=dict)
    # If these blocks can have further nested named blocks (not just generic properties), add them here.
    # For now, assuming they are flat property dictionaries after parsing.

class VehiclePart(BaseModel):
    name: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    lua: Optional[Dict[str, Any]] = None # Was VehiclePropertyBlock, but parser returns dict
    install: Optional[Dict[str, Any]] = None
    uninstall: Optional[Dict[str, Any]] = None
    container: Optional[Dict[str, Any]] = None

class ParsedVehicle(BaseModel):
    name: str
    inherits: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    model: Optional[Dict[str, Any]] = None # Was VehiclePropertyBlock
    skins: List[Dict[str, Any]] = Field(default_factory=list) # List of VehiclePropertyBlock
    sound: Optional[Dict[str, Any]] = None # Was VehiclePropertyBlock
    parts: List[VehiclePart] = Field(default_factory=list)

class ParsedTemplate(BaseModel): # Templates are similar to vehicles in structure
    name: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    model: Optional[Dict[str, Any]] = None
    skins: List[Dict[str, Any]] = Field(default_factory=list)
    sound: Optional[Dict[str, Any]] = None
    parts: List[VehiclePart] = Field(default_factory=list)

class VehicleModuleData(BaseModuleData):
    vehicles: List[ParsedVehicle] = Field(default_factory=list)
    templates: List[ParsedTemplate] = Field(default_factory=list)

# For DataExtractor to map parser keys to Pydantic models
ALL_PARSED_DATA_MODELS = Union[ItemModuleData, RecipeModuleData, VehicleModuleData]


# --- Script Generation Models ---
class BaseTemplateParams(BaseModel):
    module_name: str = "MyNewMod"
    # Common fields that might apply to various script types

class ItemTemplateParams(BaseTemplateParams):
    item_name: str
    display_name: str = "Unnamed Item" # Added default
    icon: str = "DefaultIcon"
    weight: float = 1.0
    item_type: str = "Normal" # Corresponds to 'Type' in item script
    # Add other common item properties as optional fields, e.g.:
    min_damage: Optional[float] = None
    max_damage: Optional[float] = None
    swing_sound: Optional[str] = None
    categories: Optional[str] = None # e.g. "MeleeWeapon" or "Food"

class RecipeTemplateParams(BaseTemplateParams):
    recipe_name: str
    result_item: str
    result_quantity: int = 1
    time: int = 100 # Crafting time
    # For inputs, we can simplify for now or allow a list of strings/dicts
    input_items: List[str] # e.g., ["Log", "keep Saw"] or ["Base.Log", "keep Base.Saw"]
    category: str = "General"
    # Add other common recipe properties as optional fields, e.g.:
    skill_required: Optional[str] = None # e.g., "Woodwork=1"
    near_item: Optional[str] = None # e.g., "Campfire"
