# Project Zomboid Recipe Scripts Guide (Build 41)

*Compiled from Project Zomboid Wiki and community documentation*

**Note**: This guide covers Build 41 recipe system. For Build 42, see CraftRecipe system.

---

## Table of Contents

1. [Introduction to Recipe Scripts](#introduction-to-recipe-scripts)
2. [Basic Recipe Structure](#basic-recipe-structure)
3. [Parameters Reference](#parameters-reference)
4. [Input Items and Modifiers](#input-items-and-modifiers)
5. [Output Items and Quantities](#output-items-and-quantities)
6. [Skills and Learning](#skills-and-learning)
7. [Lua Callbacks](#lua-callbacks)
8. [Examples](#examples)
9. [Advanced Features](#advanced-features)
10. [Tips and Best Practices](#tips-and-best-practices)

---

## Introduction to Recipe Scripts

Recipe scripts in Project Zomboid Build 41 define how items can be crafted. They specify input ingredients, output items, crafting time, required skills, and other crafting mechanics. Recipes take input 'ingredients' (food, tools, items, etc.) and produce an output item.

### Key Concepts:
- **Input Items**: Items consumed or used in crafting (listed at the top)
- **Result**: The item(s) produced by the recipe
- **Time**: How long the crafting takes
- **Skills**: Required skills and XP rewards
- **Callbacks**: Lua functions for custom behavior

### Important Syntax Notes:
- Recipes use `property:value` syntax (different from items which use `property = value`)
- Use `=` only for item counts
- Input items are destroyed unless marked with `keep`
- Module blocks are required for organization

---

## Basic Recipe Structure

### Standard Syntax
```
module ModuleName {
    recipe Recipe Name {
        InputItem1,
        keep InputItem2,
        InputItem3/AlternativeItem,
        
        Result:OutputItem=quantity,
        Sound:SoundName,
        Time:duration,
        Category:CategoryName,
    }
}
```

### Essential Elements:
1. **Input Items**: Listed first, one per line
2. **Blank Line**: Separates inputs from parameters
3. **Result**: Output item and quantity
4. **Time**: Crafting duration in game time units
5. **Sound**: Audio played during crafting

---

## Parameters Reference

### Core Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **Result** | String | Output item and quantity | `Result:Nails=20` |
| **Time** | Float | Crafting time (10 = 1 second) | `Time:50.0` |
| **Sound** | String | Sound effect during crafting | `Sound:PutItemInBag` |
| **Category** | String | Crafting menu category | `Category:Cooking` |

### Skill Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **SkillRequired** | String | Required skill and level | `SkillRequired:Woodwork=2` |
| **OnGiveXP** | String | Lua function for XP rewards | `OnGiveXP:Give10CookingXP` |

### Learning Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **NeedToBeLearn** | Boolean | Must be learned from recipe/book | `NeedToBeLearn:true` |
| **CanBeLearned** | Boolean | Can be learned by crafting | `CanBeLearned:true` |

### Callback Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **OnTest** | String | Lua function to test recipe validity | `OnTest:CutFish_TestIsValid` |
| **OnCreate** | String | Lua function called when recipe completes | `OnCreate:CutFish_OnCreate` |
| **OnGiveXP** | String | Custom XP reward function | `OnGiveXP:CustomXPFunction` |

### Advanced Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **RemoveResultItem** | Boolean | Don't give result item to player | `RemoveResultItem:true` |
| **DontShowResultItem** | Boolean | Hide result in crafting menu | `DontShowResultItem:true` |
| **AnimNode** | String | Animation to play | `AnimNode:Bandage` |
| **Prop1** | String | First prop for animation | `Prop1:BandageDirty` |
| **Prop2** | String | Second prop for animation | `Prop2:AlcoholRippedSheets` |

### Environmental Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **NearItem** | String | Required nearby item | `NearItem:WaterSource` |
| **IsHidden** | Boolean | Hidden from crafting menu | `IsHidden:true` |
| **CanBeDoneFromFloor** | Boolean | Can craft from floor items | `CanBeDoneFromFloor:true` |

---

## Input Items and Modifiers

### Basic Input Items
```
recipe Simple Craft {
    InputItem1,
    InputItem2,
    
    Result:OutputItem=1,
    Time:30.0,
}
```

### Keep Modifier
Prevents the item from being consumed:
```
recipe Cut Fish {
    keep KitchenKnife,        // Knife is not consumed
    Bass,                     // Fish is consumed
    
    Result:FishFillet=2,
    Time:50.0,
}
```

### Alternative Items (OR Logic)
Use `/` to separate alternative items:
```
recipe Slice Meat {
    keep KitchenKnife/HuntingKnife/Cleaver,  // Any of these knives
    Steak,
    
    Result:SteakSlices=3,
    Time:40.0,
}
```

### Item Quantities
Specify quantities after the item name:
```
recipe Craft Arrow {
    Branch=3,               // Requires 3 branches
    keep KitchenKnife,
    
    Result:WoodenStick=6,   // Produces 6 sticks
    Time:80.0,
}
```

### Complex Input Examples
```
recipe Advanced Craft {
    keep Hammer/Screwdriver,                    // Tool (kept)
    Nails=5,                                   // 5 nails (consumed)
    WoodenPlank=2/MetalBar=1,                  // 2 planks OR 1 metal bar
    keep WeldingTorch=1,                       // Welding torch (kept)
    
    Result:MetalWall=1,
    Time:300.0,
}
```

---

## Output Items and Quantities

### Basic Output
```
Result:ItemName=quantity,
```

### Quantity Calculations
The final quantity = Recipe quantity × Item's count property:
```
// If Nails have count = 5 in item definition:
Result:Nails=20,    // Player receives 20 × 5 = 100 nails
```

### Multiple Results
Some recipes can produce multiple different items (handled via Lua callbacks):
```
recipe Disassemble Radio {
    Radio,
    
    Result:Electronics=1,        // Primary result
    // Additional results handled in OnCreate callback
    OnCreate:DisassembleRadio_OnCreate,
    Time:120.0,
}
```

---

## Skills and Learning

### Skill Requirements
```
recipe Advanced Carpentry {
    WoodenPlank=4,
    keep Saw,
    
    Result:WindowFrame=1,
    SkillRequired:Woodwork=4,    // Requires Woodwork level 4
    Time:200.0,
}
```

### Multiple Skill Requirements
```
recipe Electrical Work {
    Electronics=2,
    Wire=3,
    
    Result:CircuitBoard=1,
    SkillRequired:Electricity=3,    // Could also be multiple skills
    Time:180.0,
}
```

### Learning System
```
recipe Read Recipe {
    Magazine,
    
    Result:EmptyJar=1,
    NeedToBeLearn:true,         // Must learn from magazine first
    CanBeLearned:false,         // Cannot learn by trial
    Time:10.0,
}
```

### XP Rewards
```
recipe Cooking Recipe {
    RawMeat,
    
    Result:CookedMeat=1,
    OnGiveXP:Give10CookingXP,   // Custom XP function
    Time:100.0,
}

// Or use predefined XP functions:
// Give5CookingXP, Give10CookingXP, Give25CookingXP
// Give5WoodworkXP, Give10WoodworkXP, etc.
```

---

## Lua Callbacks

### OnTest Callback
Tests if the recipe should be available:
```lua
function CutFish_TestIsValid(sourceItem, recipe)
    -- Return true if recipe should be available
    return sourceItem and sourceItem:getType() == "Bass"
end
```

### OnCreate Callback
Called when recipe is completed:
```lua
function CutFish_OnCreate(items, result, player)
    -- items: ArrayList of source items
    -- result: the result item
    -- player: the player who crafted
    
    -- Add random chance for extra fillet
    if ZombRand(100) < 25 then
        player:getInventory():AddItem("Base.FishFillet")
    end
end
```

### OnGiveXP Callback
Custom XP rewards:
```lua
function CustomCarpentryXP(recipe, ingredients, result, player)
    local woodworkLevel = player:getPerkLevel(Perks.Woodwork)
    local xpAmount = 5 + (woodworkLevel * 2)
    player:getXp():AddXP(Perks.Woodwork, xpAmount)
end
```

---

## Examples

### Basic Item Creation
```
module Base {
    recipe Open Box of Nails {
        NailsBox,
        
        Result:Nails=20,
        Sound:PutItemInBag,
        Time:5.0,
    }
}
```

### Tool-Based Crafting
```
module Base {
    recipe Cut Branches {
        keep Axe/Machete,
        TreeBranch,
        
        Result:WoodenStick=4,
        Sound:ChopTree,
        Time:75.0,
        Category:Carpentry,
        SkillRequired:Woodwork=1,
        OnGiveXP:Give5WoodworkXP,
    }
}
```

### Cooking Recipe
```
module Base {
    recipe Cook Steak {
        RawSteak,
        
        Result:Steak=1,
        Sound:Sizzling,
        Time:150.0,
        Category:Cooking,
        SkillRequired:Cooking=2,
        NearItem:Stove/Campfire,
        OnGiveXP:Give10CookingXP,
    }
}
```

### Complex Multi-Material Recipe
```
module Base {
    recipe Craft Spear {
        keep KitchenKnife/HuntingKnife,
        WoodenStick=1,
        DuctTape=2/Rope=1,
        
        Result:Spear=1,
        Sound:Hammering,
        Time:120.0,
        Category:Weapon,
        SkillRequired:Woodwork=2,
        OnGiveXP:Give15WoodworkXP,
    }
}
```

### Recipe with Lua Callbacks
```
module Base {
    recipe Slice Fish {
        keep KitchenKnife/HuntingKnife,
        Bass/Catfish/Perch/Crappie/Panfish/Pike/Trout,
        
        Result:FishFillet=2,
        Sound:SliceMeat,
        Time:50.0,
        Category:Cooking,
        OnTest:CutFish_TestIsValid,
        OnCreate:CutFish_OnCreate,
        OnGiveXP:Give10CookingXP,
    }
}
```

### Hidden/Automatic Recipe
```
module Base {
    recipe Auto Dismantle {
        BrokenRadio,
        
        Result:Electronics=1,
        Time:30.0,
        IsHidden:true,              // Not shown in crafting menu
        CanBeDoneFromFloor:true,    // Can use items from floor
        OnCreate:DisassembleRadio,  // Handles additional loot
    }
}
```

### Learning-Required Recipe
```
module Base {
    recipe Advanced Electronics {
        CircuitBoard=2,
        Wire=5,
        Battery=1,
        
        Result:RadioReceiver=1,
        Sound:ElectronicBeeps,
        Time:300.0,
        Category:Electronics,
        SkillRequired:Electricity=4,
        NeedToBeLearn:true,         // Must learn from book/magazine
        OnGiveXP:Give25ElectricityXP,
    }
}
```

---

## Advanced Features

### Categories
Organize recipes in the crafting menu:
```
Category:Cooking        // Food preparation
Category:Carpentry      // Wood working
Category:Metalworking   // Metal crafting
Category:Electronics    // Electronic items
Category:Tailoring      // Clothing and fabric
Category:Medical        // First aid items
Category:Weapon         // Weapon crafting
Category:Survival       // Survival gear
```

### Custom Categories
```
Category:MyMod Tools    // Creates custom category
```

### Animation Integration
```
recipe Apply Bandage {
    Bandage,
    
    Result:BandageDirty=1,
    AnimNode:Bandage,           // Animation type
    Prop1:BandageDirty,         // First prop
    Prop2:AlcoholRippedSheets,  // Second prop
    Time:40.0,
}
```

### Environmental Requirements
```
recipe Wash Clothes {
    DirtyClothing,
    
    Result:CleanClothing=1,
    NearItem:WaterSource,       // Must be near water
    Time:200.0,
    Sound:WashingClothes,
}
```

### Floor Crafting
```
recipe Dismantle Car Part {
    CarDoor,
    
    Result:MetalBar=2,
    CanBeDoneFromFloor:true,    // Can work with items on ground
    Time:180.0,
    SkillRequired:Mechanics=3,
}
```

---

## Tips and Best Practices

### Design Guidelines

1. **Logical Ingredients**: Use materials that make sense for the result
2. **Balanced Time**: Don't make recipes too fast or too slow
3. **Progressive Difficulty**: Start simple, add complexity with skill requirements
4. **Resource Economy**: Consider the game's resource balance

### Performance Considerations

1. **Minimize Callbacks**: Only use OnTest/OnCreate when necessary
2. **Efficient OnTest**: Keep OnTest functions fast and simple
3. **Sound Management**: Use existing sounds when possible
4. **Category Organization**: Use appropriate categories for UI performance

### Common Patterns

#### Tool + Material Pattern
```
recipe Basic Craft {
    keep Tool,                  // Keep the tool
    RawMaterial=quantity,       // Consume materials
    
    Result:Product=1,
    Time:reasonable_time,
}
```

#### Multi-Tool Pattern
```
recipe Flexible Craft {
    keep Hammer/Screwdriver/Wrench,    // Multiple tool options
    Material,
    
    Result:Product=1,
}
```

#### Skill Progression Pattern
```
recipe Beginner Level {
    BasicMaterial,
    Result:BasicProduct=1,
    SkillRequired:Skill=1,
}

recipe Advanced Level {
    AdvancedMaterial=3,
    keep ProfessionalTool,
    Result:AdvancedProduct=1,
    SkillRequired:Skill=5,
    NeedToBeLearn:true,
}
```

### Testing Your Recipes

1. **Ingredient Availability**: Ensure all required items can be found
2. **Time Balance**: Test crafting times feel appropriate
3. **Skill Requirements**: Verify skill checks work correctly
4. **Sound Effects**: Test that sounds play properly
5. **Lua Callbacks**: Debug any custom callback functions
6. **Category Placement**: Check recipes appear in correct categories

### Common Mistakes to Avoid

1. **Wrong Syntax**: Remember `:` for properties, `=` only for quantities
2. **Missing Blank Line**: Always separate inputs from parameters
3. **Invalid Items**: Ensure all referenced items exist
4. **Broken Callbacks**: Test Lua functions thoroughly
5. **Time Units**: Remember time is in game time (10 = 1 second)
6. **Keep Keyword**: Don't forget `keep` for tools you want to preserve

### Debugging Recipes

1. **Console Output**: Check for error messages
2. **Recipe Visibility**: Verify recipes appear in crafting menu
3. **Ingredient Recognition**: Test that all input items are recognized
4. **Result Production**: Confirm correct items and quantities are produced
5. **Callback Execution**: Use debug prints in Lua callbacks

---

This guide covers the comprehensive Build 41 recipe system in Project Zomboid. The system is flexible and powerful, allowing for complex crafting mechanics while remaining relatively simple to implement. Always test your recipes thoroughly and consider their impact on game balance and the player experience.