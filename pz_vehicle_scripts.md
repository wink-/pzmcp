# Project Zomboid Vehicle Scripts Guide (Build 41)

*Compiled from Project Zomboid Wiki and community modding documentation*

**Note**: This guide covers Build 41 vehicle system. Vehicle scripts define all aspects of driveable vehicles in Project Zomboid including physics, appearance, parts, and behavior.

---

## Table of Contents

1. [Introduction to Vehicle Scripts](#introduction-to-vehicle-scripts)
2. [Basic Vehicle Structure](#basic-vehicle-structure)
3. [Core Parameters Reference](#core-parameters-reference)
4. [Physics and Handling](#physics-and-handling)
5. [Visual Components](#visual-components)
6. [Vehicle Parts System](#vehicle-parts-system)
7. [Sound and Audio](#sound-and-audio)
8. [Examples](#examples)
9. [Advanced Features](#advanced-features)
10. [Tips and Best Practices](#tips-and-best-practices)

---

## Introduction to Vehicle Scripts

Vehicle scripts in Project Zomboid Build 41 define every aspect of a vehicle's behavior, appearance, and functionality. They specify physics properties, visual models, individual parts, performance characteristics, and interaction systems that determine how vehicles operate in the game world.

### Key Concepts:
- **Vehicle Block**: Main container defining the vehicle
- **Model Block**: 3D model and visual representation
- **Part Blocks**: Individual components (engine, wheels, doors, etc.)
- **Skin Blocks**: Texture variations and color schemes
- **Physics Properties**: Mass, collision, handling characteristics
- **Performance Stats**: Speed, power, fuel consumption

### Important Notes:
- Vehicle scripts use `property = value` syntax
- Multiple skins can be defined for texture variety
- Parts have complex inheritance and dependency systems
- Physics properties directly affect gameplay mechanics

---

## Basic Vehicle Structure

### Standard Syntax
```
module ModuleName {
    vehicle VehicleName {
        mechanicType = 1,
        offRoadEfficiency = 0.8,
        engineRepairLevel = 4,
        playerDamageProtection = 0.8,
        
        model {
            file = Vehicles_ModelName,
            scale = 2.15,
            offset = 0 0.20 0,
        }
        
        skin {
            texture = Vehicles/VehicleTexture,
        }
        
        /* Physics and performance properties */
        extents = 1.75 1 4.7,
        mass = 650,
        maxSpeed = 100,
        engineForce = 4000,
        
        /* Vehicle parts */
        part Engine {
            /* Part definition */
        }
    }
}
```

### Essential Components:
1. **Vehicle Declaration**: Defines the vehicle type and name
2. **Model Block**: 3D visual representation
3. **Skin Blocks**: Texture variations
4. **Physics Properties**: Size, weight, performance
5. **Part Definitions**: Individual components

---

## Core Parameters Reference

### Vehicle Identification

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **mechanicType** | Integer | Vehicle category (0=Burnt, 1=Standard, 2=Heavy Duty, 3=Sport) | `mechanicType = 1` |
| **spawnOffsetY** | Float | Height offset for vehicle spawning | `spawnOffsetY = 0.2` |

### Performance Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **maxSpeed** | Float | Maximum vehicle speed | `maxSpeed = 120` |
| **engineForce** | Float | Engine power/torque | `engineForce = 5500` |
| **engineQuality** | Float | Engine condition modifier | `engineQuality = 70` |
| **engineLoudness** | Float | Engine noise level | `engineLoudness = 100` |
| **offRoadEfficiency** | Float | Off-road performance (0.0-1.0) | `offRoadEfficiency = 0.6` |

### Mechanical Properties

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **engineRepairLevel** | Integer | Required mechanic skill for repairs | `engineRepairLevel = 6` |
| **wheelsCountHandling** | Integer | Number of wheels affecting handling | `wheelsCountHandling = 4` |
| **brakingForce** | Float | Braking power | `brakingForce = 30` |
| **stoppingMovementForce** | Float | Force to stop movement | `stoppingMovementForce = 2.0` |
| **rollInfluence** | Float | Vehicle roll tendency | `rollInfluence = 1.0` |
| **steerAngle** | Float | Maximum steering angle | `steerAngle = 40` |

### Durability and Protection

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **playerDamageProtection** | Float | Protection from impacts (0.0-1.0) | `playerDamageProtection = 0.5` |
| **crashDamageFromSpeed** | Float | Speed-related crash damage | `crashDamageFromSpeed = 0.05` |
| **engineRepairLevel** | Integer | Mechanic skill needed for engine work | `engineRepairLevel = 4` |
| **chanceToSpawnSpecial** | Float | Special spawn variant chance | `chanceToSpawnSpecial = 10` |

---

## Physics and Handling

### Collision and Size Properties
```
vehicle SportsCar {
    /* Collision box size (width, height, length) */
    extents = 1.8 1.2 4.5,
    
    /* Physics collision shape */
    physicsChassisShape = 1.8 1.0 4.5,
    
    /* Vehicle mass in kg */
    mass = 1200,
    
    /* Center of mass offset (lower = more stable) */
    centerOfMassOffset = 0 -0.5 0.2,
    
    /* Shadow positioning */
    shadowOffset = 0.0 0.0 0.0 0.0,
}
```

### Performance Tuning
```
vehicle RaceCar {
    /* Maximum achievable speed */
    maxSpeed = 200,
    
    /* Engine power output */
    engineForce = 8000,
    
    /* Braking effectiveness */
    brakingForce = 80,
    
    /* Stopping force when not accelerating */
    stoppingMovementForce = 4.0,
    
    /* Suspension stiffness */
    suspensionStiffness = 40,
    
    /* Suspension damping */
    suspensionDamping = 2.4,
    
    /* Traction on different surfaces */
    offRoadEfficiency = 0.3,  // Poor off-road
}
```

### Stability and Control
```
vehicle StableVehicle {
    /* How much vehicle rolls in turns */
    rollInfluence = 0.8,
    
    /* Maximum steering angle */
    steerAngle = 45,
    
    /* Low center of mass for stability */
    centerOfMassOffset = 0 -0.8 0,
    
    /* Suspension travel distance */
    suspensionTravel = 0.12,
    
    /* Wheel friction modifier */
    wheelFriction = 1.6,
}
```

---

## Visual Components

### Model Definition
```
model {
    file = Vehicles_SportsCarModel,
    scale = 2.0,
    offset = 0 0.15 0,
    rotate = 0 0 0,
}
```

### Texture System
```
/* Main vehicle shell texture */
textureRust = Vehicles/SportsCar_Rust,
textureMask = Vehicles/SportsCar_Mask,
textureLights = Vehicles/SportsCar_Lights,

/* Damage overlay textures */
textureDamage1Overlay = Vehicles/SportsCar_Damage01,
textureDamage1Shell = Vehicles/SportsCar_Shell_Damage01,
textureDamage2Overlay = Vehicles/SportsCar_Damage02,
textureDamage2Shell = Vehicles/SportsCar_Shell_Damage02,
```

### Skin Variations
```
skin {
    texture = Vehicles/SportsCar_Red,
}

skin {
    texture = Vehicles/SportsCar_Blue,
}

skin {
    texture = Vehicles/SportsCar_Black,
}
```

### Color Forcing
```
vehicle ColoredVehicle {
    /* Force specific HSV color values */
    forcedColor = 0.1 0.8 0.9,  // Hue, Saturation, Value (0.0-1.0)
}
```

---

## Vehicle Parts System

### Engine Definition
```
part Engine {
    category = engine,
    
    lua {
        update = Vehicles.Update.Engine,
        create = Vehicles.Create.Engine,
        init = Vehicles.Init.Engine,
        checkEngine = true,
    }
    
    itemType = Base.SmallEngine,
    mechanicRequireKey = true,
    repairMechanic = true,
    table install {
        recipes = Intermediate Mechanics,
    }
    
    table uninstall {
        recipes = Intermediate Mechanics,
    }
}
```

### Wheel System
```
part FrontLeftWheel {
    category = wheel,
    
    wheelIndex = 0,
    canBeAttached = false,
    canBeDamaged = true,
    canBeRepaired = true,
    
    lua {
        create = Vehicles.Create.Wheel,
        update = Vehicles.Update.Wheel,
    }
    
    itemType = Base.NormalCarTire,
    
    table install {
        recipes = Intermediate Mechanics,
        factionType = player,
        requireInstalled = ,
    }
    
    table uninstall {
        recipes = Beginner Mechanics,
        factionType = player,
    }
}
```

### Door Components
```
part FrontLeftDoor {
    category = bodywork,
    specificItem = false,
    
    lua {
        create = Vehicles.Create.Door,
        use = Vehicles.Use.Door,
    }
    
    itemType = Base.CarDoor,
    mechanicRequireKey = false,
    repairMechanic = true,
    
    table install {
        recipes = Intermediate Mechanics,
        time = 300,
        tools = Wrench,
        factionType = player,
    }
    
    table uninstall {
        recipes = Beginner Mechanics,
        time = 200,
        tools = Wrench,
        factionType = player,
    }
    
    areaCenter = -1.2 0 1.5,
    area = CarDoorArea,
    parent = Seat,
    setAllModelsVisible = false,
    
    container {
        capacity = 5,
        test = Vehicles.ContainerAccess.PassengerSeat,
    }
}
```

### Fuel System
```
part GasTank {
    category = engine,
    
    lua {
        init = Vehicles.Init.GasTank,
        create = Vehicles.Create.GasTank,
    }
    
    itemType = Base.SmallGasTank,
    mechanicRequireKey = true,
    repairMechanic = true,
    
    containerCapacity = 40,
    fuelTankCapacity = 40,
    
    table install {
        recipes = Intermediate Mechanics,
        skills = Mechanics:4,
        factionType = player,
    }
    
    table uninstall {
        recipes = Intermediate Mechanics,
        skills = Mechanics:3,
        factionType = player,
    }
}
```

### Interior Components
```
part Seat {
    category = seat,
    
    lua {
        use = Vehicles.Use.Seat,
    }
    
    passenger = 0,
    isDriver = true,
    showPassenger = true,
    hasRoof = true,
    
    area = SeatFrontLeft,
    areaCenter = -0.75 0 0.5,
    
    container {
        capacity = 10,
        seat = driver,
    }
}
```

---

## Sound and Audio

### Vehicle Sound Definition
```
sound {
    engine = VehicleEngineCarNormal,
    engineStart = VehicleEngineCarNormal_Start,
    engineTurnOff = VehicleEngineCarNormal_Stop,
    horn = VehicleHornStandard,
    ignitionFail = VehicleEngineCarNormal_Fail,
}
```

### Sound Categories
```
/* Engine sounds */
engine = VehicleEngineCarNormal,      // Standard car engine
engine = VehicleEngineTruck,          // Heavy truck engine
engine = VehicleEngineSportsCar,      // High-performance engine
engine = VehicleEngineVan,            // Van/utility engine

/* Horn variations */
horn = VehicleHornStandard,           // Standard car horn
horn = VehicleHornTruck,              // Truck air horn
horn = VehicleHornSports,             // Sports car horn
horn = VehicleHornEmergency,          // Emergency vehicle horn
```

---

## Examples

### Basic Sedan
```
module Base {
    vehicle FamilySedan {
        mechanicType = 1,
        offRoadEfficiency = 0.7,
        engineRepairLevel = 2,
        playerDamageProtection = 0.4,
        
        model {
            file = Vehicles_FamilySedan,
            scale = 2.1,
            offset = 0 0.15 0,
        }
        
        skin {
            texture = Vehicles/Sedan_White,
        }
        
        skin {
            texture = Vehicles/Sedan_Blue,
        }
        
        textureRust = Vehicles/Sedan_Rust,
        textureMask = Vehicles/Sedan_Mask,
        textureLights = Vehicles/Sedan_Lights,
        
        sound {
            engine = VehicleEngineCarNormal,
            horn = VehicleHornStandard,
        }
        
        extents = 1.9 1.2 4.8,
        mass = 1400,
        physicsChassisShape = 1.9 1.0 4.8,
        centerOfMassOffset = 0 -0.3 0.2,
        shadowOffset = 0.0 0.0 0.0 0.0,
        
        maxSpeed = 110,
        engineForce = 4200,
        engineQuality = 75,
        engineLoudness = 80,
        brakingForce = 30,
        stoppingMovementForce = 2.2,
        rollInfluence = 1.0,
        steerAngle = 35,
        suspensionStiffness = 30,
        suspensionDamping = 2.83,
        maxSuspensionTravelCm = 12,
        wheelFriction = 1.6,
        
        part Engine {
            category = engine,
            lua {
                update = Vehicles.Update.Engine,
                create = Vehicles.Create.Engine,
                init = Vehicles.Init.Engine,
                checkEngine = true,
            }
            itemType = Base.SmallEngine,
            mechanicRequireKey = true,
            repairMechanic = true,
            table install {
                recipes = Intermediate Mechanics,
            }
            table uninstall {
                recipes = Intermediate Mechanics,
            }
        }
        
        part GasTank {
            category = engine,
            lua {
                init = Vehicles.Init.GasTank,
                create = Vehicles.Create.GasTank,
            }
            itemType = Base.SmallGasTank,
            mechanicRequireKey = true,
            repairMechanic = true,
            containerCapacity = 40,
            fuelTankCapacity = 40,
            table install {
                recipes = Intermediate Mechanics,
            }
            table uninstall {
                recipes = Intermediate Mechanics,
            }
        }
        
        part SeatFrontLeft {
            category = seat,
            lua {
                use = Vehicles.Use.Seat,
            }
            passenger = 0,
            isDriver = true,
            showPassenger = true,
            hasRoof = true,
            area = SeatFrontLeft,
            areaCenter = -0.75 0 0.5,
            container {
                capacity = 10,
                seat = driver,
            }
        }
    }
}
```

### Sports Car
```
module Base {
    vehicle SuperSportsCar {
        mechanicType = 3,
        offRoadEfficiency = 0.2,
        engineRepairLevel = 6,
        playerDamageProtection = 0.2,
        
        model {
            file = Vehicles_SportsCar,
            scale = 2.0,
            offset = 0 0.1 0,
        }
        
        skin {
            texture = Vehicles/SportsCar_Red,
        }
        
        sound {
            engine = VehicleEngineSportsCar,
            horn = VehicleHornSports,
        }
        
        extents = 1.8 1.0 4.2,
        mass = 1100,
        physicsChassisShape = 1.8 0.8 4.2,
        centerOfMassOffset = 0 -0.6 0.1,
        
        maxSpeed = 200,
        engineForce = 7500,
        engineQuality = 90,
        engineLoudness = 120,
        brakingForce = 50,
        stoppingMovementForce = 3.5,
        rollInfluence = 0.6,
        steerAngle = 40,
        suspensionStiffness = 50,
        suspensionDamping = 3.2,
        maxSuspensionTravelCm = 8,
        wheelFriction = 2.0,
        
        crashDamageFromSpeed = 0.08,
        chanceToSpawnSpecial = 5,
    }
}
```

### Heavy Truck
```
module Base {
    vehicle HeavyTruck {
        mechanicType = 2,
        offRoadEfficiency = 0.9,
        engineRepairLevel = 4,
        playerDamageProtection = 0.8,
        
        model {
            file = Vehicles_HeavyTruck,
            scale = 2.5,
            offset = 0 0.3 0,
        }
        
        sound {
            engine = VehicleEngineTruck,
            horn = VehicleHornTruck,
        }
        
        extents = 2.2 1.8 6.5,
        mass = 3500,
        physicsChassisShape = 2.2 1.5 6.5,
        centerOfMassOffset = 0 -0.2 0.5,
        
        maxSpeed = 90,
        engineForce = 6000,
        engineQuality = 80,
        engineLoudness = 150,
        brakingForce = 40,
        stoppingMovementForce = 1.8,
        rollInfluence = 1.2,
        steerAngle = 30,
        suspensionStiffness = 80,
        suspensionDamping = 4.0,
        maxSuspensionTravelCm = 20,
        wheelFriction = 1.8,
        
        wheelsCountHandling = 6,
        crashDamageFromSpeed = 0.02,
    }
}
```

---

## Advanced Features

### Vehicle Templates
Create base templates for similar vehicles:
```
template StandardCar {
    mechanicType = 1,
    engineRepairLevel = 3,
    playerDamageProtection = 0.4,
    
    extents = 1.9 1.2 4.6,
    mass = 1300,
    maxSpeed = 100,
    engineForce = 4000,
    brakingForce = 30,
    
    /* Standard parts */
    part Engine { /* ... */ }
    part GasTank { /* ... */ }
    /* ... other common parts */
}
```

### Conditional Spawning
```
vehicle RareVehicle {
    chanceToSpawnSpecial = 2,  // 2% chance to spawn
    
    spawnOffsetY = 0.1,
    mechanicType = 3,
    
    /* Special high-performance stats */
    maxSpeed = 180,
    engineForce = 8000,
}
```

### Multi-Variant System
```
vehicle BasePickup {
    /* Base pickup truck definition */
}

vehicle PickupPolice : BasePickup {
    /* Inherits base pickup, adds police modifications */
    forcedColor = 0.0 0.0 1.0,  // Blue
    
    part Siren {
        category = lights,
        /* Siren-specific properties */
    }
}
```

### Complex Part Dependencies
```
part Headlight {
    category = lights,
    specificItem = false,
    
    lua {
        create = Vehicles.Create.Headlight,
        update = Vehicles.Update.Headlight,
    }
    
    itemType = Base.Headlight,
    repairMechanic = true,
    
    table install {
        recipes = Intermediate Mechanics,
        requireInstalled = Battery,  // Requires battery to function
        skills = Electricity:2,
    }
    
    electricalPower = 5,
    lightDistance = 25,
    lightStrength = 0.8,
}
```

---

## Tips and Best Practices

### Performance Optimization

1. **Reasonable Physics Values**: Don't use extreme values that break physics
   ```
   mass = 1500,           // Reasonable for car
   engineForce = 5000,    // Balanced power
   maxSpeed = 120,        // Realistic top speed
   ```

2. **Efficient Part System**: Only include necessary parts
   ```
   // Essential parts only
   part Engine { /* ... */ }
   part GasTank { /* ... */ }
   part SeatFrontLeft { /* ... */ }
   // Add others as needed
   ```

### Balance Considerations

1. **Vehicle Classes**: Maintain clear distinctions
   ```
   // Economy car
   maxSpeed = 90, engineForce = 3500, mass = 1200
   
   // Sports car  
   maxSpeed = 180, engineForce = 7000, mass = 1100
   
   // Truck
   maxSpeed = 80, engineForce = 5500, mass = 2800
   ```

2. **Trade-offs**: Balance speed vs. durability vs. capacity
   ```
   // Fast but fragile
   maxSpeed = 200, playerDamageProtection = 0.1
   
   // Slow but tough
   maxSpeed = 70, playerDamageProtection = 0.9
   ```

### Common Issues and Solutions

1. **Physics Mismatch Warning**: Ensure extents match physicsChassisShape
   ```
   extents = 1.8 1.2 4.5,
   physicsChassisShape = 1.8 1.0 4.5,  // Similar dimensions
   ```

2. **Unstable Vehicles**: Lower center of mass
   ```
   centerOfMassOffset = 0 -0.7 0,  // Lower = more stable
   ```

3. **Poor Handling**: Adjust suspension and friction
   ```
   suspensionStiffness = 40,
   wheelFriction = 1.6,
   rollInfluence = 0.8,
   ```

### Testing Guidelines

1. **Spawn Testing**: Use debug mode to test vehicles
   ```
   // Enable with -debug launch parameter
   // Right-click vehicle -> [DEBUG] Vehicle -> Set Script
   ```

2. **Performance Testing**: Check various scenarios
   - Highway driving
   - Off-road performance  
   - Collision damage
   - Part functionality

3. **Balance Testing**: Compare to vanilla vehicles
   - Acceleration rates
   - Top speeds
   - Fuel consumption
   - Durability

### File Organization

```
mod_folder/
├── media/
│   ├── models_X/
│   │   └── vehicles/
│   │       ├── MySportsCar.X
│   │       └── MyTruck.X
│   ├── scripts/
│   │   └── vehicles/
│   │       ├── mysportscar.txt
│   │       └── mytruck.txt
│   └── textures/
│       └── vehicles/
│           ├── MySportsCar_Shell.png
│           ├── MySportsCar_Rust.png
│           └── MySportsCar_Lights.png
```

### Debugging Vehicles

1. **Console Errors**: Check for script syntax errors
2. **Missing Models**: Verify file paths and model files exist
3. **Physics Issues**: Test extents vs physicsChassisShape alignment
4. **Part Problems**: Ensure all required items exist in item scripts
5. **Performance Issues**: Monitor FPS impact of complex vehicles

---

This guide covers the comprehensive Build 41 vehicle system in Project Zomboid. Vehicle creation requires understanding physics, visual design, and complex part systems. Proper vehicle scripting creates balanced, fun, and immersive transportation options that enhance the survival experience while maintaining game stability and performance.