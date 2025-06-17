import pytest
from mcp_server.parsers.vehicle_parser import VehicleParser

def test_simple_vehicle_in_module():
    script_content = """
    module Base {
        vehicle CarNormal {
            mechanicType = 1,
            weight = 1300.0,
            frontEndHealth = 100,
            engineKW = 28,
        }
    }
    """
    parser = VehicleParser(script_content)
    expected = {
        "module": "Base",
        "vehicles": [{
            "name": "CarNormal",
            "inherits": None,
            "properties": {
                "mechanicType": "1",
                "weight": "1300.0",
                "frontEndHealth": "100",
                "engineKW": "28",
            },
            "skins": [],
            "parts": []
            # model, sound would be None or {} if not present, based on parser init
        }],
        "templates": []
    }
    parsed_output = parser.parse()
    assert parsed_output["module"] == expected["module"]
    assert parsed_output["templates"] == expected["templates"]
    assert len(parsed_output["vehicles"]) == 1
    # Check vehicle properties carefully, as other blocks might be auto-initialized to {} or None
    vehicle_out = parsed_output["vehicles"][0]
    vehicle_exp = expected["vehicles"][0]
    assert vehicle_out["name"] == vehicle_exp["name"]
    assert vehicle_out["inherits"] == vehicle_exp["inherits"]
    assert vehicle_out["properties"] == vehicle_exp["properties"]
    assert vehicle_out.get("skins", []) == vehicle_exp.get("skins", []) # Handle if key missing
    assert vehicle_out.get("parts", []) == vehicle_exp.get("parts", [])
    assert vehicle_out.get("model") == vehicle_exp.get("model") # Expect None if not parsed
    assert vehicle_out.get("sound") == vehicle_exp.get("sound")


def test_vehicle_with_model_skin_sound():
    script_content = """
    module Base {
        vehicle CarSport {
            model {
                file = Vehicles_CarSport,
                scale = 2.0,
            }
            skin {
                texture = Vehicles/CarSportTex,
            }
            skin {
                texture = Vehicles/CarSportTex2_Zombie,
            }
            sound {
                engine = VehicleEngineCarSport,
                horn = VehicleHornSport,
            }
        }
    }
    """
    parser = VehicleParser(script_content)
    parsed = parser.parse()
    assert parsed["module"] == "Base"
    assert len(parsed["vehicles"]) == 1
    vehicle = parsed["vehicles"][0]
    assert vehicle["name"] == "CarSport"
    assert vehicle["model"] == {"file": "Vehicles_CarSport", "scale": "2.0"}
    assert len(vehicle["skins"]) == 2
    assert vehicle["skins"][0] == {"texture": "Vehicles/CarSportTex"}
    assert vehicle["skins"][1] == {"texture": "Vehicles/CarSportTex2_Zombie"}
    assert vehicle["sound"] == {"engine": "VehicleEngineCarSport", "horn": "VehicleHornSport"}

def test_vehicle_inheritance():
    script_content = """
    module Base {
        vehicle ModernCar : CarNormal {
            maxSpeed = 120,
        }
    }
    """
    parser = VehicleParser(script_content)
    parsed = parser.parse()
    assert len(parsed["vehicles"]) == 1
    vehicle = parsed["vehicles"][0]
    assert vehicle["name"] == "ModernCar"
    assert vehicle["inherits"] == "CarNormal"
    assert vehicle["properties"] == {"maxSpeed": "120"}


def test_template_definition():
    script_content = """
    module Base {
        template StandardCar {
            frontEndHealth = 100,
            rearEndHealth = 100,
        }
    }
    """
    parser = VehicleParser(script_content)
    parsed = parser.parse()
    assert len(parsed["templates"]) == 1
    template = parsed["templates"][0]
    assert template["name"] == "StandardCar"
    assert template["properties"] == {"frontEndHealth": "100", "rearEndHealth": "100"}

def test_vehicle_with_parts_and_nested_blocks():
    script_content = """
    module Base {
        vehicle TruckBed {
            part Trunk {
                category = trunk,
                parent = Bed,
                container {
                    capacity = 150,
                    contentType = Base.TruckBedTrunk,
                }
                lua {
                    update = Vehicles.Update.Trunk,
                }
            }
            part "Spare Tire" { // Quoted part name
                parent = Bed,
                table install {
                    item = Tire,
                    requires = LugWrench,
                }
                table uninstall {
                    item = Tire,
                    requires = LugWrench,
                }
            }
        }
    }
    """
    parser = VehicleParser(script_content)
    parsed = parser.parse()
    assert len(parsed["vehicles"]) == 1
    vehicle = parsed["vehicles"][0]
    assert vehicle["name"] == "TruckBed"
    assert len(vehicle["parts"]) == 2

    part1 = vehicle["parts"][0]
    assert part1["name"] == "Trunk"
    assert part1["properties"] == {"category": "trunk", "parent": "Bed"}
    assert part1["container"] == {"capacity": "150", "contentType": "Base.TruckBedTrunk"}
    assert part1["lua"] == {"update": "Vehicles.Update.Trunk"}
    assert part1["install"] is None # or {} depending on parser's handling of missing blocks
    assert part1["uninstall"] is None

    part2 = vehicle["parts"][1]
    assert part2["name"] == "Spare Tire"
    assert part2["properties"] == {"parent": "Bed"}
    assert part2["install"] == {"item": "Tire", "requires": "LugWrench"}
    assert part2["uninstall"] == {"item": "Tire", "requires": "LugWrench"}
    assert part2["container"] is None
    assert part2["lua"] is None

def test_properties_with_multi_value_strings_and_comments():
    script_content = """
    module Base {
        vehicle VanSeats {
            physicsSphere = 0.25, // Single value
            offset = 0 0.35 0,   // Multi-value
            extents = 1.5 1.0 2.5, // Multi-value with floats
            // Another comment
            mass = 200.0,
            /* Block comment
               here */
            anotherProp = "quoted string value",
        }
    }
    """
    parser = VehicleParser(script_content)
    parsed = parser.parse()
    assert len(parsed["vehicles"]) == 1
    vehicle = parsed["vehicles"][0]
    assert vehicle["properties"] == {
        "physicsSphere": "0.25",
        "offset": "0 0.35 0",
        "extents": "1.5 1.0 2.5",
        "mass": "200.0",
        "anotherProp": "quoted string value",
    }

def test_empty_script_vehicle_parser():
    script_content = ""
    parser = VehicleParser(script_content)
    expected = {"module": None, "vehicles": [], "templates": []}
    assert parser.parse() == expected

def test_script_with_only_comments_vehicle_parser():
    script_content = """
    // Module for testing
    /**
     * vehicle TestVehicle {
     *   prop = val
     * }
    **/
    -- End of file
    """
    parser = VehicleParser(script_content)
    expected = {"module": None, "vehicles": [], "templates": []}
    assert parser.parse() == expected

def test_module_with_no_vehicles_or_templates():
    script_content = "module TestModule { }"
    parser = VehicleParser(script_content)
    parsed = parser.parse()
    assert parsed["module"] == "TestModule"
    assert parsed["vehicles"] == []
    assert parsed["templates"] == []

def test_complex_vehicle_from_pz_example():
    # Simplified from a real PZ script for brevity, focusing on structure
    script_content = """
    module Base
    {
        vehicle CarLuxury
        {
            physicsSphere = 0.25,
            mass = 200.0, // mass of the chassis
            model
            {
                file = Vehicles_CarLuxury,
                scale = 2.15,
            }
            sound
            {
                horn = VehicleHornLuxury,
                engine = VehicleEngineCarNormal,
                engineStart = VehicleEngineStartCarNormal,
                engineTurnOff = VehicleEngineStopCarNormal,
            }
            part FrontDoor // Example of a part
            {
                area = "1,1,2,2", // Just a string for now
                container
                {
                    capacity = 10,
                    seat = frontleft,
                }
                mechanicRequire = MetalWelding=1,
            }
            part Engine
            {
                sound = vehicle_engine_van_01,
            }
        }
    }
    """
    parser = VehicleParser(script_content)
    parsed = parser.parse()

    assert parsed["module"] == "Base"
    assert len(parsed["vehicles"]) == 1
    vehicle = parsed["vehicles"][0]
    assert vehicle["name"] == "CarLuxury"
    assert vehicle["properties"]["physicsSphere"] == "0.25"
    assert vehicle["properties"]["mass"] == "200.0"

    assert vehicle["model"]["file"] == "Vehicles_CarLuxury"
    assert vehicle["model"]["scale"] == "2.15"

    assert vehicle["sound"]["horn"] == "VehicleHornLuxury"

    assert len(vehicle["parts"]) == 2
    part_front_door = next(p for p in vehicle["parts"] if p["name"] == "FrontDoor")
    part_engine = next(p for p in vehicle["parts"] if p["name"] == "Engine")

    assert part_front_door["properties"]["area"] == "1,1,2,2" # Stays as string
    assert part_front_door["properties"]["mechanicRequire"] == "MetalWelding=1"
    assert part_front_door["container"]["capacity"] == "10"
    assert part_front_door["container"]["seat"] == "frontleft"

    assert part_engine["properties"]["sound"] == "vehicle_engine_van_01"
    assert part_engine["container"] is None # Or {}
    assert part_engine["lua"] is None # Or {}
