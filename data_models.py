from typing import List, Dict, Any, Optional, Union

class ModelComponent: # Generic component for items
    def __init__(self, **kwargs):
        # Example: DisplayName = "Industrial Dye" -> self.DisplayName = "Industrial Dye"
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

class Item:
    def __init__(self, itemName: str, **kwargs):
        self.itemName: str = itemName
        # Common properties, can be expanded
        self.DisplayName: Optional[str] = None
        self.Type: Optional[str] = None
        self.Weight: Optional[Union[float, int]] = None

        self.components: Dict[str, ModelComponent] = {}

        # Dynamically assign known and extra properties
        attrs_to_skip = ['itemName'] # Already handled
        component_prefix = "component "

        for key, value in kwargs.items():
            if key in attrs_to_skip:
                continue
            if key.startswith(component_prefix) and isinstance(value, dict):
                comp_full_name = key[len(component_prefix):] # E.g. "FluidContainer"
                self.components[comp_full_name] = ModelComponent(**value)
            elif hasattr(self, key): # Check if it's a predefined attribute
                setattr(self, key, value)
            else: # Store as an additional property if not predefined
                setattr(self, key, value)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if k != 'components')
        comp_attrs = ", ".join(f"{k}={v!r}" for k, v in self.components.items())
        if comp_attrs:
            return f"Item({attrs}, components=({comp_attrs}))"
        return f"Item({attrs})"

class RecipeInput:
    def __init__(self, type: str, quantity: Union[int, float], name: Optional[str] = None, **kwargs):
        self.type: str = type # 'item' or 'fluid'
        self.quantity: Union[int, float] = quantity
        self.name: Optional[str] = name # Item name or fluid category
        self.tags: Optional[List[str]] = None
        self.categories: Optional[List[str]] = None
        self.mode: Optional[str] = None
        self.flags: Optional[List[str]] = None
        self.negative_marker: Optional[bool] = None # For inputs like "-fluid"

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"RecipeInput({attrs})"

class RecipeOutput:
    def __init__(self, type: str, quantity: Union[int, float], name: Optional[str] = None, **kwargs):
        self.type: str = type # 'item'
        self.quantity: Union[int, float] = quantity
        self.name: Optional[str] = name
        self.mapper: Optional[str] = None

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"RecipeOutput({attrs})"

class ItemMapper: # For recipe itemMappers
    def __init__(self, mapper_name: str, **kwargs):
        self.mapper_name: str = mapper_name
        self.properties: Dict[str, Any] = kwargs

    def __repr__(self):
        return f"ItemMapper(mapper_name={self.mapper_name!r}, properties={self.properties!r})"

class Recipe:
    def __init__(self, recipeName: str, **kwargs):
        self.recipeName: str = recipeName
        self.Time: Optional[Union[int, float]] = None
        self.category: Optional[str] = None
        self.inputs: List[RecipeInput] = []
        self.outputs: List[RecipeOutput] = []
        self.itemMappers: Dict[str, ItemMapper] = {} # Store itemMappers by their name

        attrs_to_skip = ['recipeName', 'inputs', 'outputs']
        item_mapper_prefix = "itemMapper "

        for key, value in kwargs.items():
            if key in attrs_to_skip:
                continue
            if key.startswith(item_mapper_prefix) and isinstance(value, dict):
                mapper_name = key[len(item_mapper_prefix):]
                self.itemMappers[mapper_name] = ItemMapper(mapper_name=mapper_name, **value)
            elif hasattr(self, key):
                setattr(self, key, value)
            else:
                setattr(self, key, value)

    def __repr__(self):
        # Basic representation, can be expanded
        return (f"Recipe(recipeName={self.recipeName!r}, Time={self.Time!r}, category={self.category!r}, "
                f"inputs={len(self.inputs)}, outputs={len(self.outputs)}, itemMappers={list(self.itemMappers.keys())})")


# --- Vehicle Related Data Models ---

class VehicleSubBlock: # Generic class for nested vehicle parts like passenger, wheel, etc.
    def __init__(self, name: Optional[str] = None, **kwargs):
        if name: # For named blocks like passenger Driver, wheel FR
            self._name: str = name

        # For properties like offset = [0.0, 0.5, 0.0] or canSwitchTo = ["Gunner1", "Gunner2"]
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

class VehicleModelBlock(VehicleSubBlock): # For anonymous model {} inside a vehicle
    pass
class VehicleSkinBlock(VehicleSubBlock): # For skin {}
    pass
class VehicleSoundBlock(VehicleSubBlock): # For sound {}
    pass
class PassengerBlock(VehicleSubBlock): # For passenger <Name> {}
    pass
class AreaBlock(VehicleSubBlock): # For area <Name> {}
    pass
class WheelBlock(VehicleSubBlock): # For wheel <Name> {}
    pass
class PartBlock(VehicleSubBlock): # For part <Name> {}
    pass
class AttachmentBlock(VehicleSubBlock): # For attachment <Name> {}
    pass


class VehicleDefinition: # Common base for Vehicle, VehicleModel, VehicleTemplate
    def __init__(self, **kwargs):
        self.mass: Optional[Union[int, float]] = None
        self.engineForce: Optional[Union[int, float]] = None
        self.file: Optional[str] = None # For top-level model file
        self.scale: Optional[float] = None # For top-level model scale

        # Nested structures
        self.model: Optional[VehicleModelBlock] = None # For anonymous model {} block
        self.skin: Optional[VehicleSkinBlock] = None
        self.sound: Optional[VehicleSoundBlock] = None
        self.passengers: List[PassengerBlock] = []
        self.areas: List[AreaBlock] = []
        self.wheels: List[WheelBlock] = []
        self.parts: List[PartBlock] = []
        self.attachments: List[AttachmentBlock] = []

        # Catch-all for other properties
        self.additional_properties: Dict[str, Any] = {}

        # Known nested block keys and their corresponding classes and list names
        self._nested_block_configs = {
            "model": {"class": VehicleModelBlock, "list_name": None, "is_singleton": True}, # Anonymous model
            "skin": {"class": VehicleSkinBlock, "list_name": None, "is_singleton": True},
            "sound": {"class": VehicleSoundBlock, "list_name": None, "is_singleton": True},
            "passenger": {"class": PassengerBlock, "list_name": "passengers", "is_singleton": False},
            "area": {"class": AreaBlock, "list_name": "areas", "is_singleton": False},
            "wheel": {"class": WheelBlock, "list_name": "wheels", "is_singleton": False},
            "part": {"class": PartBlock, "list_name": "parts", "is_singleton": False},
            "attachment": {"class": AttachmentBlock, "list_name": "attachments", "is_singleton": False},
        }

        for key, value in kwargs.items():
            if key in self._nested_block_configs:
                config = self._nested_block_configs[key]
                if config["is_singleton"]:
                    if isinstance(value, dict): # Parsed data for the singleton block
                        setattr(self, key, config["class"](**value))
                    else: # Should not happen if parser is correct
                        print(f"Warning: Expected dict for singleton block {key}, got {type(value)}")
                else: # It's a list of blocks
                    if isinstance(value, list): # Parsed list of dicts
                        obj_list = []
                        for item_dict in value:
                            item_name = item_dict.pop('_name', None) # Extract name if present
                            obj_list.append(config["class"](name=item_name, **item_dict))
                        setattr(self, config["list_name"], obj_list)
                    else: # Should not happen
                         print(f"Warning: Expected list for block type {key}, got {type(value)}")

            elif hasattr(self, key):
                setattr(self, key, value)
            else:
                self.additional_properties[key] = value

    def __repr__(self):
        # Simplified repr for brevity
        parts = []
        for k, v in self.__dict__.items():
            if k == "additional_properties" and not v:
                continue
            if isinstance(v, list) and not v: # Don't print empty lists of sub-blocks
                continue
            if v is None: # Don't print None attributes
                continue
            if k == "_nested_block_configs": # internal helper
                continue
            parts.append(f"{k}={v!r}")
        return f"{self.__class__.__name__}({', '.join(parts)})"


class Vehicle(VehicleDefinition):
    def __init__(self, vehicleName: str, **kwargs):
        self.vehicleName: str = vehicleName
        super().__init__(**kwargs)

class VehicleModel(VehicleDefinition): # For top-level model <Name> {}
    def __init__(self, modelName: str, **kwargs):
        self.modelName: str = modelName
        super().__init__(**kwargs)

class VehicleTemplate(VehicleDefinition):
    def __init__(self, templateName: str, **kwargs):
        self.templateName: str = templateName
        super().__init__(**kwargs)
