# Project Zomboid Multistagebuild Scripts Guide (Build 41)

*Compiled from Project Zomboid Wiki and community modding documentation*

**Note**: This guide covers Build 41 multistagebuild system. Multistagebuild scripts define constructable buildings and structures that can be built in multiple stages or levels.

---

## Table of Contents

1. [Introduction to Multistagebuild Scripts](#introduction-to-multistagebuild-scripts)
2. [Basic Structure](#basic-structure)
3. [Core Parameters Reference](#core-parameters-reference)
4. [Construction Progression](#construction-progression)
5. [Visual and Audio Properties](#visual-and-audio-properties)
6. [Skill and Recipe Integration](#skill-and-recipe-integration)
7. [Examples](#examples)
8. [Advanced Features](#advanced-features)
9. [Special Construction Types](#special-construction-types)
10. [Tips and Best Practices](#tips-and-best-practices)

---

## Introduction to Multistagebuild Scripts

Multistagebuild scripts in Project Zomboid Build 41 define construction projects that can be built in multiple stages or upgraded over time. They handle everything from basic walls and windows to complex structures like stairs and doors, allowing players to progressively improve their constructions with better materials and higher skill levels.

### Key Concepts:
- **Stage Progression**: Buildings can be constructed in levels (Level 1, Level 2, Level 3)
- **Prerequisites**: Each stage requires specific previous stages to be completed
- **Skill Requirements**: Different stages require different skill levels
- **Material Consumption**: Items are consumed during construction
- **Health Bonuses**: Each stage adds structural integrity
- **Visual Evolution**: Sprites change as construction progresses

### Important Notes:
- Multistagebuild scripts use `property:value` syntax (similar to recipes)
- Multiple previous stages can be specified with semicolons
- Tools can be kept using `ItemsToKeep` parameter
- Construction time affects gameplay balance

---

## Basic Structure

### Standard Syntax
```
module ModuleName {
    multistagebuild BuildingName {
        PreviousStage:RequiredStage1;RequiredStage2,
        Name:FinalStageName,
        TimeNeeded:constructionTime,
        BonusHealth:healthIncrease,
        SkillRequired:SkillName=level,
        ItemsRequired:Item1=quantity;Item2=quantity,
        ItemsToKeep:ToolName,
        Sprite:spriteID,
        NorthSprite:northSpriteID,
        CraftingSound:soundName,
        ID:menuDisplayName,
        XP:SkillName=xpAmount,
    }
}
```

### Essential Elements:
1. **PreviousStage**: What must exist before this can be built
2. **Name**: Internal identifier for the completed stage
3. **TimeNeeded**: Construction time in game time units
4. **BonusHealth**: HP added to the structure
5. **SkillRequired**: Required skill and level
6. **ItemsRequired**: Materials consumed during construction
7. **Sprite**: Visual appearance after completion

---

## Core Parameters Reference

### Stage Control Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **PreviousStage** | String | Required previous stage(s) | `PreviousStage:WoodenWallFrame;MetalWallFrame` |
| **Name** | String | Internal name for completed stage | `Name:WoodenWallLvl1` |
| **ID** | String | Display name in construction menu | `ID:Create Wooden Wall Lvl 1` |

### Construction Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **TimeNeeded** | Integer | Construction time (10 = 1 second) | `TimeNeeded:250` |
| **BonusHealth** | Integer | HP added to structure | `BonusHealth:400` |
| **BonusSkill** | Boolean | Whether skill bonus applies | `BonusSkill:FALSE` |

### Skill and Experience

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **SkillRequired** | String | Required skill and level | `SkillRequired:Woodwork=2` |
| **XP** | String | Experience reward | `XP:Woodwork=10` |
| **KnownRecipe** | String | Required known recipe | `KnownRecipe:Make Metal Walls` |

### Material Requirements

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **ItemsRequired** | String | Items consumed (semicolon separated) | `ItemsRequired:Base.Plank=2;Base.Nails=4` |
| **ItemsToKeep** | String | Tools not consumed | `ItemsToKeep:Base.Hammer` |

### Visual Properties

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **Sprite** | String | Main sprite after completion | `Sprite:walls_exterior_wooden_01_44` |
| **NorthSprite** | String | North-facing sprite | `NorthSprite:walls_exterior_wooden_01_45` |

### Audio Properties

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **CraftingSound** | String | Sound during construction | `CraftingSound:Hammering` |
| **CompletionSound** | String | Sound when finished | `CompletionSound:BuildWoodStructureMedium` |
| **ThumpSound** | String | Sound when hit/damaged | `ThumpSound:ZombieThumpMetal` |

### Special Properties

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **WallType** | String | Special wall behavior | `WallType:doorframe` |
| **CanBarricade** | Boolean | Can be barricaded | `CanBarricade:true` |
| **CanBePlastered** | Boolean | Can have plaster applied | `CanBePlastered:true` |

---

## Construction Progression

### Linear Progression
Most constructions follow a linear upgrade path:
```
Frame → Level 1 → Level 2 → Level 3
```

### Initial Construction
Creating the first level from a frame:
```
multistagebuild CreateWoodenWall_1 {
    PreviousStage:WoodenWallFrame;MetalWallFrame,
    Name:WoodenWallLvl1,
    TimeNeeded:250,
    BonusHealth:400,
    SkillRequired:Woodwork=2,
    ItemsRequired:Base.Plank=2;Base.Nails=4,
    ItemsToKeep:Base.Hammer,
    Sprite:walls_exterior_wooden_01_44,
    NorthSprite:walls_exterior_wooden_01_45,
    CraftingSound:Hammering,
    ID:Create Wooden Wall Lvl 1,
    XP:Woodwork=10,
}
```

### Upgrading Existing Structures
Improving an existing construction:
```
multistagebuild UpgradeWoodenWall_1To2 {
    PreviousStage:WoodenWallLvl1,
    Name:WoodenWallLvl2,
    TimeNeeded:200,
    BonusHealth:100,
    BonusSkill:FALSE,
    SkillRequired:Woodwork=4,
    ItemsRequired:Base.Plank=1;Base.Nails=4,
    ItemsToKeep:Base.Hammer,
    Sprite:walls_exterior_wooden_01_40,
    NorthSprite:walls_exterior_wooden_01_41,
    CraftingSound:Hammering,
    ID:Upgrade to Wooden Wall Lvl 2,
    XP:Woodwork=10,
}
```

### Direct Construction
Building higher levels directly (skip intermediate stages):
```
multistagebuild CreateWoodenWall_2 {
    PreviousStage:WoodenWallFrame;MetalWallFrame,
    Name:WoodenWallLvl2,
    TimeNeeded:450,  // Longer time for direct construction
    BonusHealth:500,  // Full bonus health
    SkillRequired:Woodwork=4,
    ItemsRequired:Base.Plank=3;Base.Nails=8,  // More materials
    ItemsToKeep:Base.Hammer,
    Sprite:walls_exterior_wooden_01_40,
    NorthSprite:walls_exterior_wooden_01_41,
    CraftingSound:Hammering,
    ID:Create Wooden Wall Lvl 2,
    XP:Woodwork=20,  // More XP for direct construction
}
```

---

## Visual and Audio Properties

### Sprite System
```
multistagebuild VisualExample {
    /* Main sprite (facing south/east) */
    Sprite:constructedobjects_01_64,
    
    /* North-facing variant */
    NorthSprite:constructedobjects_01_65,
    
    /* Some constructions use different sprite categories */
    Sprite:walls_exterior_wooden_01_52,
    NorthSprite:walls_exterior_wooden_01_53,
}
```

### Sound Integration
```
multistagebuild AudioExample {
    /* Sound during construction */
    CraftingSound:Hammering,        // Carpentry work
    CraftingSound:BlowTorch,        // Metalworking
    CraftingSound:Sawing,           // Sawing wood
    
    /* Sound when construction completes */
    CompletionSound:BuildWoodStructureMedium,
    CompletionSound:BuildMetalStructureMedium,
    
    /* Sound when damaged by zombies */
    ThumpSound:ZombieThumpMetal,
    ThumpSound:ZombieThumpGeneric,
}
```

### Conditional Sprites
Based on facing direction and construction level:
```
multistagebuild DirectionalSprites {
    /* Different sprites for different orientations */
    Sprite:walls_exterior_wooden_01_44,      // South/East facing
    NorthSprite:walls_exterior_wooden_01_45, // North/West facing
}
```

---

## Skill and Recipe Integration

### Skill Requirements
```
multistagebuild SkillProgression {
    /* Basic carpentry */
    SkillRequired:Woodwork=2,
    
    /* Advanced carpentry */
    SkillRequired:Woodwork=6,
    
    /* Metalworking */
    SkillRequired:MetalWelding=5,
    
    /* Multiple skills (rare) */
    SkillRequired:Woodwork=4;Electricity=2,
}
```

### Experience Rewards
```
multistagebuild ExperienceRewards {
    /* Basic XP */
    XP:Woodwork=10,
    
    /* Higher XP for advanced construction */
    XP:MetalWelding=15,
    
    /* Multiple skill XP */
    XP:Woodwork=10;Electricity=5,
}
```

### Recipe Requirements
```
multistagebuild RecipeGated {
    /* Must know specific recipe */
    KnownRecipe:Make Metal Walls,
    KnownRecipe:Advanced Carpentry,
    KnownRecipe:Electrical Work,
}
```

---

## Examples

### Basic Wooden Wall System
```
module Base {
    /* Create Level 1 Wooden Wall */
    multistagebuild CreateWoodenWall_1 {
        PreviousStage:WoodenWallFrame;MetalWallFrame,
        Name:WoodenWallLvl1,
        TimeNeeded:250,
        BonusHealth:400,
        SkillRequired:Woodwork=2,
        ItemsRequired:Base.Plank=2;Base.Nails=4,
        ItemsToKeep:Base.Hammer,
        Sprite:walls_exterior_wooden_01_44,
        NorthSprite:walls_exterior_wooden_01_45,
        CraftingSound:Hammering,
        ID:Create Wooden Wall Lvl 1,
        XP:Woodwork=10,
    }
    
    /* Upgrade to Level 2 */
    multistagebuild UpgradeWoodenWall_1To2 {
        PreviousStage:WoodenWallLvl1,
        Name:WoodenWallLvl2,
        TimeNeeded:200,
        BonusHealth:100,
        BonusSkill:FALSE,
        SkillRequired:Woodwork=4,
        ItemsRequired:Base.Plank=1;Base.Nails=4,
        ItemsToKeep:Base.Hammer,
        Sprite:walls_exterior_wooden_01_40,
        NorthSprite:walls_exterior_wooden_01_41,
        CraftingSound:Hammering,
        ID:Upgrade to Wooden Wall Lvl 2,
        XP:Woodwork=10,
    }
    
    /* Direct construction to Level 2 */
    multistagebuild CreateWoodenWall_2 {
        PreviousStage:WoodenWallFrame;MetalWallFrame,
        Name:WoodenWallLvl2,
        TimeNeeded:450,
        BonusHealth:500,
        SkillRequired:Woodwork=4,
        ItemsRequired:Base.Plank=3;Base.Nails=8,
        ItemsToKeep:Base.Hammer,
        Sprite:walls_exterior_wooden_01_40,
        NorthSprite:walls_exterior_wooden_01_41,
        CraftingSound:Hammering,
        ID:Create Wooden Wall Lvl 2,
        XP:Woodwork=20,
    }
}
```

### Metal Wall Construction
```
module Base {
    /* Create Level 1 Metal Wall */
    multistagebuild CreateMetalWall_1 {
        PreviousStage:WoodenWallFrame;MetalWallFrame,
        Name:MetalWallLvl1,
        TimeNeeded:250,
        BonusHealth:650,
        SkillRequired:MetalWelding=2,
        ItemsRequired:Base.SheetMetal=3;Base.BlowTorch=7,
        ItemsToKeep:Base.BlowTorch,
        Sprite:constructedobjects_01_64,
        NorthSprite:constructedobjects_01_65,
        KnownRecipe:Make Metal Walls,
        ThumpSound:ZombieThumpMetal,
        CraftingSound:BlowTorch,
        CompletionSound:BuildMetalStructureMedium,
        ID:Create Metal Wall Lvl 1,
        XP:MetalWelding=15,
    }
    
    /* Upgrade to Level 2 */
    multistagebuild UpgradeMetalWall_1To2 {
        PreviousStage:MetalWallLvl1,
        Name:MetalWallLvl2,
        TimeNeeded:200,
        BonusHealth:100,
        BonusSkill:FALSE,
        SkillRequired:MetalWelding=8,
        ItemsRequired:Base.SheetMetal=1;Base.BlowTorch=3,
        ItemsToKeep:Base.BlowTorch,
        Sprite:constructedobjects_01_48,
        NorthSprite:constructedobjects_01_49,
        KnownRecipe:Make Metal Walls,
        ThumpSound:ZombieThumpMetal,
        CraftingSound:BlowTorch,
        CompletionSound:BuildMetalStructureMedium,
        ID:Upgrade to Metal Wall Lvl 2,
        XP:MetalWelding=15,
    }
}
```

### Window Construction
```
module Base {
    /* Create Level 1 Wooden Window */
    multistagebuild CreateWoodenWindow_1 {
        PreviousStage:WoodenWallFrame;MetalWallFrame,
        Name:WoodenWindowLvl1,
        TimeNeeded:250,
        BonusHealth:400,
        SkillRequired:Woodwork=2,
        ItemsRequired:Base.Plank=2;Base.Nails=4,
        ItemsToKeep:Base.Hammer,
        Sprite:walls_exterior_wooden_01_52,
        NorthSprite:walls_exterior_wooden_01_53,
        CraftingSound:Hammering,
        ID:Create Wooden Window Lvl 1,
        XP:Woodwork=10,
        CanBarricade:true,
    }
    
    /* Metal Window */
    multistagebuild CreateMetalWindow_1 {
        PreviousStage:WoodenWallFrame;MetalWallFrame,
        Name:MetalWindowLvl1,
        TimeNeeded:250,
        BonusHealth:650,
        SkillRequired:MetalWelding=5,
        ItemsRequired:Base.SheetMetal=3;Base.BlowTorch=7,
        ItemsToKeep:Base.BlowTorch,
        Sprite:constructedobjects_01_72,
        NorthSprite:constructedobjects_01_73,
        KnownRecipe:Make Metal Walls,
        ThumpSound:ZombieThumpMetal,
        CraftingSound:BlowTorch,
        CompletionSound:BuildMetalStructureMedium,
        ID:Create Metal Window Lvl 1,
        XP:MetalWelding=15,
        CanBarricade:true,
    }
}
```

### Door Frame Construction
```
module Base {
    /* Upgrade Wooden Door Frame Level 1 to 2 */
    multistagebuild UpgradeWoodenDoorFrame_1To2 {
        PreviousStage:WoodenDoorFrameLvl1,
        Name:WoodenDoorFrameLvl2,
        TimeNeeded:200,
        BonusHealth:200,
        SkillRequired:Woodwork=4,
        ItemsRequired:Base.Plank=1;Base.Nails=4,
        ItemsToKeep:Base.Hammer,
        WallType:doorframe,
        Sprite:walls_exterior_wooden_01_50,
        NorthSprite:walls_exterior_wooden_01_51,
        CraftingSound:Hammering,
        ID:Upgrade to Wooden Door Frame Lvl 2,
        XP:Woodwork=5,
    }
    
    /* Upgrade to Level 3 */
    multistagebuild UpgradeWoodenDoorFrame_2To3 {
        PreviousStage:WoodenDoorFrameLvl2,
        Name:WoodenDoorFrameLvl3,
        TimeNeeded:200,
        BonusHealth:100,
        BonusSkill:FALSE,
        SkillRequired:Woodwork=6,
        ItemsRequired:Base.Plank=1;Base.Nails=4,
        ItemsToKeep:Base.Hammer,
        WallType:doorframe,
        Sprite:walls_exterior_wooden_01_46,
        NorthSprite:walls_exterior_wooden_01_47,
        CraftingSound:Hammering,
        ID:Upgrade to Wooden Door Frame Lvl 3,
        XP:Woodwork=5,
    }
}
```

---

## Advanced Features

### Multiple Previous Stages
Allow construction from different starting points:
```
multistagebuild FlexibleConstruction {
    /* Can be built on either wooden or metal frames */
    PreviousStage:WoodenWallFrame;MetalWallFrame,
    
    /* Can upgrade from multiple previous levels */
    PreviousStage:BasicWallLvl1;ReinforcedWallLvl1;ConcreteWallLvl1,
}
```

### Special Wall Types
```
multistagebuild DoorFrameExample {
    WallType:doorframe,  // Special behavior for doors
    /* Door frames allow passage through them */
}
```

### Material Efficiency
```
multistagebuild MaterialOptimized {
    /* Basic construction */
    ItemsRequired:Base.Plank=2;Base.Nails=4,
    ItemsToKeep:Base.Hammer,  // Tool preserved
    
    /* Advanced construction with multiple tools */
    ItemsRequired:Base.SheetMetal=3;Base.BlowTorch=7,
    ItemsToKeep:Base.BlowTorch;Base.WeldingRods,  // Multiple tools kept
}
```

### Bonus Health Calculation
```
multistagebuild HealthProgression {
    /* Level 1: Base health + 400 */
    BonusHealth:400,
    
    /* Level 2: Previous health + 100 additional */
    BonusHealth:100,
    BonusSkill:FALSE,  // Don't apply skill multiplier
}
```

---

## Special Construction Types

### Stairs Construction
```
multistagebuild BuildWoodenStairs {
    PreviousStage:nothing,  // Can be built on empty ground
    Name:WoodenStairs,
    TimeNeeded:500,
    BonusHealth:300,
    SkillRequired:Woodwork=6,
    ItemsRequired:Base.Plank=15;Base.Nails=15,
    ItemsToKeep:Base.Hammer;Base.Saw,
    Sprite:stairs_wooden_01,
    NorthSprite:stairs_wooden_01_north,
    CraftingSound:Hammering,
    CompletionSound:BuildWoodStructureLarge,
    ID:Build Wooden Stairs,
    XP:Woodwork=25,
}
```

### Floor Construction
```
multistagebuild BuildWoodenFloor {
    PreviousStage:nothing,
    Name:WoodenFloor,
    TimeNeeded:100,
    BonusHealth:150,
    SkillRequired:Woodwork=1,
    ItemsRequired:Base.Plank=1;Base.Nails=2,
    ItemsToKeep:Base.Hammer,
    Sprite:floors_wooden_01,
    CraftingSound:Hammering,
    ID:Build Wooden Floor,
    XP:Woodwork=5,
}
```

### Roof Construction
```
multistagebuild BuildWoodenRoof {
    PreviousStage:WoodenWallLvl1;WoodenWallLvl2;WoodenWallLvl3,
    Name:WoodenRoof,
    TimeNeeded:300,
    BonusHealth:200,
    SkillRequired:Woodwork=4,
    ItemsRequired:Base.Plank=4;Base.Nails=8;Base.RoofingNails=6,
    ItemsToKeep:Base.Hammer,
    Sprite:roof_wooden_01,
    CraftingSound:Hammering,
    CompletionSound:BuildWoodStructureMedium,
    ID:Build Wooden Roof,
    XP:Woodwork=15,
}
```

---

## Tips and Best Practices

### Design Guidelines

1. **Logical Progression**: Each level should feel like a meaningful upgrade
   ```
   Level 1: Basic construction (Skill 2, basic materials)
   Level 2: Improved version (Skill 4, more materials)
   Level 3: Advanced version (Skill 6, premium materials)
   ```

2. **Balanced Time Requirements**: Construction time should reflect complexity
   ```
   Simple walls: 250 time units
   Complex structures: 500+ time units
   Upgrades: 200 time units (faster than new construction)
   ```

3. **Health Progression**: Each level should add meaningful durability
   ```
   Level 1: 400-500 bonus health
   Level 2: 100-200 additional health
   Level 3: 100-150 additional health
   ```

### Material Balance

1. **Resource Economy**: Consider material availability
   ```
   Common materials: Planks, Nails (easy to find)
   Uncommon materials: Sheet Metal, Blow Torch uses (harder to find)
   Rare materials: Welding Rods, Special Tools (very limited)
   ```

2. **Tool Preservation**: Always preserve expensive tools
   ```
   ItemsToKeep:Base.Hammer,        // Common, but should preserve
   ItemsToKeep:Base.BlowTorch,     // Expensive, definitely preserve
   ItemsToKeep:Base.Saw,           // Useful, preserve when possible
   ```

### Skill Integration

1. **Skill Requirements**: Match skill level to construction complexity
   ```
   Carpentry 1-2: Basic frames, floors
   Carpentry 3-4: Walls, windows
   Carpentry 5-6: Advanced structures, stairs
   
   Metalworking 2-3: Basic metal walls
   Metalworking 4-6: Advanced metal construction
   Metalworking 7-8: Master-level metalwork
   ```

2. **Experience Rewards**: Balance XP with effort required
   ```
   Basic construction: 5-10 XP
   Intermediate construction: 10-15 XP
   Advanced construction: 15-25 XP
   Master construction: 25+ XP
   ```

### Visual Consistency

1. **Sprite Progression**: Visual improvement should match functional improvement
   ```
   Level 1: Basic, rough appearance
   Level 2: More refined, additional details
   Level 3: Professional, polished appearance
   ```

2. **Directional Sprites**: Always provide north variants for proper appearance
   ```
   Sprite:walls_exterior_wooden_01_44,      // South/East
   NorthSprite:walls_exterior_wooden_01_45, // North/West
   ```

### Audio Design

1. **Appropriate Sounds**: Match sounds to construction type
   ```
   CraftingSound:Hammering,     // Wood construction
   CraftingSound:BlowTorch,     // Metal welding
   CraftingSound:Sawing,        // Wood cutting
   ```

2. **Completion Feedback**: Provide satisfying completion sounds
   ```
   CompletionSound:BuildWoodStructureMedium,   // Wood projects
   CompletionSound:BuildMetalStructureMedium,  // Metal projects
   ```

### Common Issues and Solutions

1. **Missing Prerequisites**: Ensure all referenced stages exist
   ```
   PreviousStage:WoodenWallFrame,  // Must exist as multistagebuild or default
   ```

2. **Invalid Sprites**: Verify all sprite references are valid
   ```
   Sprite:walls_exterior_wooden_01_44,  // Must exist in sprite sheets
   ```

3. **Skill Balance**: Test skill requirements for gameplay flow
   ```
   SkillRequired:Woodwork=2,  // Not too easy, not impossibly hard
   ```

4. **Material Costs**: Balance resource consumption with benefit gained
   ```
   ItemsRequired:Base.Plank=2;Base.Nails=4,  // Reasonable for benefit
   ```

### Testing Your Constructions

1. **In-Game Testing**: Build structures in-game to verify functionality
2. **Progression Testing**: Test all upgrade paths work correctly
3. **Balance Testing**: Ensure time/material costs feel appropriate
4. **Visual Testing**: Check sprites appear correctly in all orientations
5. **Audio Testing**: Verify sounds play at appropriate times

### Performance Considerations

1. **Reasonable Complexity**: Don't create overly complex prerequisite chains
2. **Efficient Sprites**: Use existing sprite sets when possible
3. **Balanced Construction Times**: Very long construction times can hurt gameplay
4. **Logical Dependencies**: Prerequisites should make logical sense

---

This guide covers the comprehensive Build 41 multistagebuild system in Project Zomboid. The system allows for complex, progressive construction mechanics that enhance base-building gameplay. Proper multistagebuild scripting creates satisfying construction progression that rewards player skill development and resource management while maintaining game balance and immersion.