# Project Zomboid Fixing Scripts Guide

*Compiled from Project Zomboid Wiki and community documentation*

---

## Table of Contents

1. [Introduction to Fixing Scripts](#introduction-to-fixing-scripts)
2. [Basic Fixing Structure](#basic-fixing-structure)
3. [Parameters Reference](#parameters-reference)
4. [Skills System](#skills-system)
5. [Examples](#examples)
6. [Advanced Usage](#advanced-usage)
7. [Tips and Best Practices](#tips-and-best-practices)

---

## Introduction to Fixing Scripts

Fixing blocks are used to define how items can be repaired in Project Zomboid. These scripts specify which items can be used to fix other items, how much material is required, and what skills (if any) are needed for the repair.

### Key Concepts:
- **Require**: The item that needs to be repaired
- **Fixer**: The materials that can be used for repair and their quantities
- **Skills**: Optional skill requirements for specific repair materials
- **Syntax**: Uses `property : value` format (different from item scripts)

---

## Basic Fixing Structure

### Standard Syntax
```
fixing Fix [ItemName] {
    Require : ItemToBeRepaired,
    Fixer : RepairMaterial=Quantity,
    Fixer : RepairMaterial=Quantity; SkillRequired=Level,
    Fixer : AnotherMaterial=Quantity,
}
```

### Key Rules:
- **Naming Convention**: Use descriptive names starting with "Fix"
- **Require Parameter**: Must specify exactly one item type to be repaired
- **Multiple Fixers**: Can have multiple repair material options
- **Skill Requirements**: Optional second parameter after semicolon
- **No Module Required**: Fixing blocks don't need to be in a module block

---

## Parameters Reference

### Core Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **Require** | String | Item that can be repaired | `WoodAxe` |
| **Fixer** | String | Repair material and quantity | `Woodglue=2` |
| **Fixer (with skill)** | String | Material, quantity, and skill requirement | `Woodglue=2; Woodwork=2` |

### Fixer Parameter Format

The `Fixer` parameter can be specified in two formats:

**Basic Format:**
```
Fixer : MaterialName=Quantity,
```

**With Skill Requirement:**
```
Fixer : MaterialName=Quantity; SkillName=Level,
```

### Important Notes:
- **First Parameter**: Always the material name and quantity
- **Second Parameter**: Optional skill requirement
- **Quantity**: Number of items consumed in repair
- **Skill Level**: Minimum skill level required (0-10)

---

## Skills System

### Available Skills for Repair Requirements

| Skill Name | Description | Common Uses |
|------------|-------------|-------------|
| **Axe** | Axe weapon skill | Axe repairs |
| **Blunt** | Blunt weapon skill | Club, bat repairs |
| **SmallBlunt** | Small blunt weapon skill | Small tools |
| **LongBlade** | Long blade weapon skill | Sword, machete repairs |
| **SmallBlade** | Small blade weapon skill | Knife repairs |
| **Spear** | Spear weapon skill | Spear repairs |
| **Maintenance** | General maintenance skill | Tool repairs |
| **Aiming** | Firearms skill | Gun part repairs |
| **Reloading** | Reload skill | Magazine repairs |
| **Woodwork** | Carpentry skill | Wood item repairs |
| **Cooking** | Cooking skill | Kitchen item repairs |
| **Farming** | Farming skill | Farm tool repairs |
| **Doctor** | Medical skill | Medical item repairs |
| **Electricity** | Electrical skill | Electronic repairs |
| **MetalWelding** | Metalworking skill | Metal item repairs |
| **Mechanics** | Automotive skill | Vehicle part repairs |
| **Tailoring** | Tailoring skill | Clothing repairs |
| **Fishing** | Fishing skill | Fishing gear repairs |
| **Trapping** | Trapping skill | Trap repairs |
| **PlantScavenging** | Foraging skill | Natural item repairs |
| **Fitness** | Fitness skill | Rarely used |
| **Strength** | Strength skill | Heavy item repairs |
| **Sprinting** | Sprint skill | Rarely used |
| **Lightfoot** | Lightfoot skill | Rarely used |
| **Nimble** | Nimble skill | Rarely used |
| **Sneak** | Sneak skill | Rarely used |

---

## Examples

### Basic Weapon Repair
```
fixing Fix Wood Axe {
    Require : WoodAxe,
    Fixer : Woodglue=2,
    Fixer : DuctTape=2,
    Fixer : Glue=2,
    Fixer : Scotchtape=4,
}
```

### Repair with Skill Requirements
```
fixing Fix Baseball Bat {
    Require : BaseballBat,
    Fixer : Woodglue=2; Woodwork=2,
    Fixer : DuctTape=2,
    Fixer : Glue=2,
    Fixer : Scotchtape=4,
}
```

### Tool Repair
```
fixing Fix Hammer {
    Require : Hammer,
    Fixer : DuctTape=1,
    Fixer : Woodglue=1; Maintenance=1,
    Fixer : MetalPipe=1; MetalWelding=3,
    Fixer : Nails=2; Woodwork=1,
}
```

### Clothing Repair
```
fixing Fix Jeans {
    Require : Jeans,
    Fixer : Thread=2; Tailoring=1,
    Fixer : DuctTape=1,
    Fixer : Needle=1; Tailoring=2,
}
```

### Kitchen Item Repair
```
fixing Fix Cooking Pot {
    Require : Pot,
    Fixer : MetalBar=1; MetalWelding=2,
    Fixer : DuctTape=2,
    Fixer : Glue=3,
}
```

### Complex Repair with Multiple Materials
```
fixing Fix Chainsaw {
    Require : Chainsaw,
    Fixer : ScrewsBox=5; Mechanics=4,
    Fixer : MetalBar=2; MetalWelding=5,
    Fixer : DuctTape=3,
    Fixer : WeldingRods=2; MetalWelding=3,
    Fixer : SmallEngine=1; Mechanics=6,
}
```

### Vehicle Part Repair
```
fixing Fix Car Door {
    Require : NormalCarSeat,
    Fixer : MetalBar=3; MetalWelding=4,
    Fixer : ScrewsBox=10; Mechanics=3,
    Fixer : DuctTape=5,
    Fixer : WeldingRods=3; MetalWelding=2,
}
```

### Medical Item Repair
```
fixing Fix Stethoscope {
    Require : Stethoscope,
    Fixer : DuctTape=1,
    Fixer : Glue=2; Doctor=2,
    Fixer : Electronics=1; Electricity=3,
}
```

---

## Advanced Usage

### Multiple Item Types
You can create separate fixing blocks for variants of the same item:

```
fixing Fix Normal Crowbar {
    Require : Crowbar,
    Fixer : MetalBar=1; MetalWelding=2,
    Fixer : DuctTape=2,
}

fixing Fix Red Crowbar {
    Require : CrowbarRed,
    Fixer : MetalBar=1; MetalWelding=2,
    Fixer : DuctTape=2,
}
```

### Tiered Repair Materials
Organize repair options from basic to advanced:

```
fixing Fix Kitchen Knife {
    Require : KitchenKnife,
    Fixer : DuctTape=1,                    // Emergency repair
    Fixer : Glue=2,                        // Basic repair
    Fixer : Whetstone=1; Maintenance=2,    // Proper repair
    Fixer : MetalBar=1; MetalWelding=4,    // Professional repair
}
```

### Skill-Gated Premium Repairs
```
fixing Fix Watch {
    Require : DigitalWatch,
    Fixer : DuctTape=1,                    // Anyone can tape it
    Fixer : Electronics=1; Electricity=3,  // Need skill for proper fix
    Fixer : Battery=1; Electricity=1,      // Battery replacement
}
```

---

## Tips and Best Practices

### Design Guidelines

1. **Progressive Difficulty**: Start with easy/common materials, add skill-required options
2. **Material Balance**: Don't make repairs too cheap or too expensive
3. **Realistic Materials**: Use materials that logically would work for repair
4. **Skill Appropriateness**: Match skill requirements to the item type

### Common Material Hierarchy
```
// From easiest/cheapest to hardest/most expensive:
DuctTape=1-3           // Universal emergency repair
Scotchtape=2-5         // Weaker alternative
Glue=1-3              // Basic adhesive
Woodglue=1-2          // Better for wood items
Thread=1-2            // For fabric items
Nails=2-5             // For wood construction
ScrewsBox=3-10        // For mechanical items
MetalBar=1-3          // For metal welding
WeldingRods=1-5       // Professional metal repair
```

### Skill Level Guidelines
```
Level 0-1: Basic repairs anyone can do
Level 2-3: Require some training/experience
Level 4-6: Intermediate skill level
Level 7-8: Advanced/professional level
Level 9-10: Master craftsman level
```

### Performance Considerations

1. **Don't Over-Specify**: Only add fixing blocks for items that should be repairable
2. **Reasonable Options**: 3-6 fixer options is usually sufficient
3. **Balance Testing**: Test repair costs vs. finding new items
4. **Mod Compatibility**: Consider how your repairs interact with other mods

### Common Mistakes to Avoid

1. **Wrong Syntax**: Remember `property : value` not `property = value`
2. **Missing Commas**: Each parameter line needs a trailing comma
3. **Invalid Items**: Ensure Require and Fixer items actually exist
4. **Invalid Skills**: Use exact skill names from the reference list
5. **Unrealistic Repairs**: Don't let duct tape fix everything perfectly

### Testing Your Repairs

1. **In-Game Testing**: Spawn items and test repair options
2. **Skill Requirements**: Test with different skill levels
3. **Material Consumption**: Verify correct quantities are consumed
4. **Success/Failure**: Check that skill requirements work properly
5. **Balance Testing**: Ensure repairs aren't overpowered or useless

### Integration with Mods

When creating fixing scripts for modded items:

```
fixing Fix Custom Weapon {
    Require : MyMod.CustomSword,
    Fixer : DuctTape=2,
    Fixer : Woodglue=1; Maintenance=2,
    Fixer : MetalBar=1; MetalWelding=3,
}
```

Remember to use the full item type including module name for modded items.

---

This guide covers the essential aspects of Project Zomboid fixing scripts. The system is straightforward but powerful, allowing you to create realistic repair mechanics that enhance gameplay by giving players meaningful choices about item maintenance and resource management.
# Project Zomboid Evolved Recipe Scripts Guide

*Compiled from Project Zomboid Wiki and community documentation*

---

## Table of Contents

1. [Introduction to Evolved Recipes](#introduction-to-evolved-recipes)
2. [Basic Structure](#basic-structure)
3. [Parameters Reference](#parameters-reference)
4. [Template System](#template-system)
5. [Item Integration](#item-integration)
6. [Examples](#examples)
7. [Advanced Features](#advanced-features)
8. [Tips and Best Practices](#tips-and-best-practices)

---

## Introduction to Evolved Recipes

Evolved recipes in Project Zomboid are a special type of recipe system designed primarily for food preparation. Unlike regular recipes, evolved recipes allow players to continuously add ingredients to a base item, creating complex dishes with multiple components. They are perfect for sandwiches, salads, stews, and other multi-ingredient foods.

### Key Concepts:
- **Base Item**: The starting item (e.g., bread for sandwiches)
- **Ingredients**: Items that can be added to the base item
- **Result Item**: The final dish when ingredients are added
- **Template System**: Allows multiple recipes to share the same ingredient pool
- **Dynamic Building**: Players can add ingredients one by one

### How It Works:
1. Player starts with a base item (like bread slices)
2. Right-clicks to see available ingredients to add
3. Each ingredient added transforms the item closer to the final result
4. Maximum number of ingredients can be set
5. Final result can be cooked or used as-is

---

## Basic Structure

### Standard Syntax
```
module ModuleName {
    evolvedrecipe Recipe Name {
        BaseItem:StartingItem,
        MaxItems:number,
        ResultItem:FinalItem,
        Name:Display Name,
    }
}
```

### Essential Elements:
- **BaseItem**: The item to start building on
- **MaxItems**: Maximum number of ingredients that can be added
- **ResultItem**: What the item becomes when ingredients are added
- **Name**: Display name shown to players

### Simple Example:
```
module Base {
    evolvedrecipe Sandwich {
        BaseItem:BreadSlices,
        MaxItems:4,
        ResultItem:Sandwich,
        Name:Make Sandwich,
    }
}
```

---

## Parameters Reference

### Core Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **BaseItem** | String | Starting item for the recipe | `BaseItem:BreadSlices` |
| **ResultItem** | String | Final item when ingredients are added | `ResultItem:Sandwich` |
| **MaxItems** | Integer | Maximum ingredients that can be added | `MaxItems:4` |
| **Name** | String | Display name in crafting menu | `Name:Make Sandwich` |

### Behavior Parameters

| Parameter | Type | Description | Default | Example |
|-----------|------|-------------|---------|---------|
| **Cookable** | Boolean | Can the result item be cooked | `false` | `Cookable:true` |
| **AddIngredientIfCooked** | Boolean | Can add ingredients to cooked items | `false` | `AddIngredientIfCooked:true` |
| **CanAddSpicesEmpty** | Boolean | Can add spices without other ingredients | `false` | `CanAddSpicesEmpty:true` |

### Organization Parameters

| Parameter | Type | Description | Default | Example |
|-----------|------|-------------|---------|---------|
| **Template** | String | Template name for shared ingredients | `""` | `Template:Sandwich` |
| **Hidden** | Boolean | Hide from recipe menu | `false` | `Hidden:true` |

### Audio Parameters

| Parameter | Type | Description | Default | Example |
|-----------|------|-------------|---------|---------|
| **AddIngredientSound** | String | Sound when adding ingredients | `AddItemInRecipe` | `AddIngredientSound:ChopFood` |

### Advanced Parameters

| Parameter | Type | Description | Default | Example |
|-----------|------|-------------|---------|---------|
| **AllowFrozenIngredient** | Boolean | Allow frozen ingredients | `false` | `AllowFrozenIngredient:true` |

---

## Template System

The template system allows multiple evolved recipes to share the same pool of ingredients. This is efficient for creating variations of similar foods.

### Defining a Template
```
evolvedrecipe Sandwich {
    BaseItem:BreadSlices,
    MaxItems:4,
    ResultItem:Sandwich,
    Name:Make Sandwich,
    Template:Sandwich,
}

evolvedrecipe Burger {
    BaseItem:BreadSlices,
    MaxItems:6,
    ResultItem:Burger,
    Name:Make Burger,
    Template:Sandwich,    // Uses same ingredient pool as Sandwich
}
```

### Using Templates in Items
Items specify which evolved recipes they can be used in via the `EvolvedRecipe` parameter:

```
item Tomato {
    Type = Food,
    DisplayName = Tomato,
    // Other parameters...
    EvolvedRecipe = Sandwich:6;Burger:6,  // Can be used in both recipes
}

item Ham {
    Type = Food,
    DisplayName = Ham,
    // Other parameters...
    EvolvedRecipe = Sandwich:3;Burger:3,  // Different nutrition values per recipe
}
```

### Template Benefits:
- **Shared Ingredients**: Multiple recipes can use the same ingredient pool
- **Consistency**: Same ingredients work across similar recipes
- **Efficiency**: Less duplication in item definitions
- **Flexibility**: Easy to add new recipe variations

---

## Item Integration

### EvolvedRecipe Parameter in Items
Items that can be used as ingredients must specify this in their item definition:

```
item IngredientItem {
    Type = Food,
    DisplayName = My Ingredient,
    // Other food parameters...
    EvolvedRecipe = TemplateName:NutritionValue,
}
```

### Nutrition Value System
The number after the colon represents how much this ingredient contributes to the recipe:
```
EvolvedRecipe = Sandwich:6;Burger:4;Salad:8,
```
- Higher numbers = more nutritious/filling ingredients
- Used to calculate final food values
- Can be different for each recipe type

### Multiple Recipe Support
Items can be used in multiple evolved recipes:
```
item Cheese {
    Type = Food,
    DisplayName = Cheese,
    EvolvedRecipe = Sandwich:4;Burger:4;Pizza:5;Salad:3,
}
```

---

## Examples

### Basic Sandwich Recipe
```
module Base {
    evolvedrecipe Sandwich {
        BaseItem:BreadSlices,
        MaxItems:4,
        ResultItem:Sandwich,
        Name:Make Sandwich,
        Template:Sandwich,
    }
}
```

### Advanced Burger Recipe
```
module Base {
    evolvedrecipe Burger {
        BaseItem:BurgerBun,
        MaxItems:6,
        ResultItem:Burger,
        Name:Make Burger,
        Cookable:true,
        AddIngredientIfCooked:true,
        CanAddSpicesEmpty:true,
        Template:Burger,
        AddIngredientSound:ChopFood,
    }
}
```

### Soup Recipe
```
module Base {
    evolvedrecipe Soup {
        BaseItem:Pot,
        MaxItems:8,
        ResultItem:Soup,
        Name:Make Soup,
        Cookable:true,
        AddIngredientIfCooked:false,      // Must add ingredients before cooking
        CanAddSpicesEmpty:true,           // Can start with just spices
        Template:Soup,
        AddIngredientSound:AddFoodInPot,
    }
}
```

### Salad Recipe
```
module Base {
    evolvedrecipe Salad {
        BaseItem:Bowl,
        MaxItems:10,
        ResultItem:Salad,
        Name:Make Salad,
        Cookable:false,                   // Salads aren't cooked
        AddIngredientIfCooked:true,       // Can add cooked ingredients
        CanAddSpicesEmpty:false,          // Need actual ingredients first
        Template:Salad,
        AllowFrozenIngredient:false,      // Fresh ingredients only
    }
}
```

### Pizza Recipe
```
module Base {
    evolvedrecipe Pizza {
        BaseItem:PizzaDough,
        MaxItems:12,
        ResultItem:Pizza,
        Name:Make Pizza,
        Cookable:true,
        AddIngredientIfCooked:false,      // Add toppings before baking
        CanAddSpicesEmpty:true,           // Can start with sauce/spices
        Template:Pizza,
        AddIngredientSound:AddToppings,
    }
}
```

### Stew Recipe
```
module Base {
    evolvedrecipe Stew {
        BaseItem:Pot,
        MaxItems:15,
        ResultItem:Stew,
        Name:Make Stew,
        Cookable:true,
        AddIngredientIfCooked:true,       // Can add ingredients while cooking
        CanAddSpicesEmpty:true,
        Template:Stew,
        AllowFrozenIngredient:true,       // Frozen ingredients OK for stew
    }
}
}
```

---

## Advanced Features

### Complex Template Sharing
Multiple recipes can share templates for ingredient compatibility:

```
// All use the same "MeatDish" template
evolvedrecipe MeatStew {
    BaseItem:Pot,
    MaxItems:10,
    ResultItem:Stew,
    Template:MeatDish,
}

evolvedrecipe MeatPie {
    BaseItem:PieCrust,
    MaxItems:8,
    ResultItem:MeatPie,
    Template:MeatDish,
}

evolvedrecipe MeatSoup {
    BaseItem:Pot,
    MaxItems:12,
    ResultItem:Soup,
    Template:MeatDish,
}
```

### Ingredient Categories
Items can belong to multiple evolved recipe categories:
```
item Chicken {
    Type = Food,
    DisplayName = Chicken,
    EvolvedRecipe = MeatDish:8;Sandwich:4;Soup:6;Salad:5,
}
```

### Cooking Integration
Evolved recipes work with the cooking system:
```
evolvedrecipe CookableDish {
    BaseItem:RawBase,
    ResultItem:CookedDish,
    Cookable:true,                      // Can be cooked
    AddIngredientIfCooked:false,        // Add ingredients before cooking
    MaxItems:6,
}
```

### Spice System
Special handling for spices and seasonings:
```
evolvedrecipe FlavoredDish {
    BaseItem:BlandFood,
    ResultItem:FlavoredFood,
    CanAddSpicesEmpty:true,             // Can start with just spices
    MaxItems:8,
}
```

---

## Tips and Best Practices

### Design Guidelines

1. **Logical Base Items**: Choose appropriate starting items (bread for sandwiches, bowls for salads)
2. **Reasonable Limits**: Set MaxItems based on what makes sense for the dish
3. **Template Consistency**: Group similar recipes under shared templates
4. **Nutrition Balance**: Set appropriate nutrition values in item EvolvedRecipe parameters

### Template Strategy

1. **Group Similar Foods**: Sandwiches, burgers, wraps can share templates
2. **Separate by Type**: Keep meat dishes, vegetarian dishes, desserts separate
3. **Consider Cooking**: Hot and cold dishes might need different ingredients
4. **Spice Compatibility**: Consider which spices work with which dish types

### MaxItems Guidelines
```
Sandwiches/Burgers: 4-6 items
Salads: 6-10 items
Soups/Stews: 8-15 items
Pizza: 8-12 items
Simple dishes: 3-5 items
Complex dishes: 10+ items
```

### Ingredient Balance

1. **Main Ingredients**: High nutrition values (6-10)
2. **Secondary Ingredients**: Medium values (3-5)
3. **Seasonings/Spices**: Low values (1-2)
4. **Garnishes**: Very low values (0-1)

### Performance Considerations

1. **Template Reuse**: Use templates to reduce duplicate ingredient lists
2. **Reasonable MaxItems**: Don't make recipes with excessive ingredient slots
3. **Sound Management**: Use appropriate, existing sounds when possible

### Common Patterns

#### Basic Food Assembly
```
evolvedrecipe SimpleFood {
    BaseItem:Base,
    MaxItems:4,
    ResultItem:CompleteFood,
    Name:Make Food,
    Template:FoodType,
}
```

#### Cookable Dish
```
evolvedrecipe CookableDish {
    BaseItem:RawBase,
    MaxItems:8,
    ResultItem:CookedDish,
    Cookable:true,
    AddIngredientIfCooked:false,
    Template:CookableFood,
}
```

#### Flexible Seasoning
```
evolvedrecipe FlexibleDish {
    BaseItem:PlainFood,
    MaxItems:6,
    ResultItem:SeasonedFood,
    CanAddSpicesEmpty:true,
    AddIngredientIfCookable:true,
}
```

### Testing Your Evolved Recipes

1. **Base Item Recognition**: Verify base items show the recipe option
2. **Ingredient Addition**: Test that appropriate ingredients can be added
3. **MaxItems Limit**: Confirm the limit works correctly
4. **Template Sharing**: Test that multiple recipes can use shared ingredients
5. **Cooking Integration**: If cookable, test the cooking process
6. **Nutrition Calculation**: Verify final food values make sense

### Common Mistakes to Avoid

1. **Missing EvolvedRecipe Parameter**: Ingredients won't work without this in item definitions
2. **Inconsistent Templates**: Using wrong template names
3. **Unrealistic MaxItems**: Too many or too few ingredient slots
4. **Missing Base Items**: Base item must exist and be obtainable
5. **Template Conflicts**: Different templates with same ingredients can cause confusion

### Integration with Other Systems

Evolved recipes work with:
- **Regular Recipes**: Can create base items or ingredients via regular recipes
- **Cooking System**: Final results can be cooked if Cookable:true
- **Nutrition System**: Ingredient nutrition values are calculated into final food
- **Spoilage System**: Final foods spoil based on ingredient spoilage rates

---

This guide covers the complete evolved recipe system in Project Zomboid. Evolved recipes provide a flexible way to create complex, multi-ingredient foods that feel realistic and allow for player creativity in food preparation. They're particularly effective for foods where the combination of ingredients matters more than the specific crafting process.
# Project Zomboid Item Scripting Guide

*Compiled from Project Zomboid Wiki and community documentation*

---

## Table of Contents

1. [Introduction to Item Scripts](#introduction-to-item-scripts)
2. [Basic Item Structure](#basic-item-structure)
3. [Essential Parameters](#essential-parameters)
4. [Item Types](#item-types)
5. [Core Parameters Reference](#core-parameters-reference)
6. [Weapon Parameters](#weapon-parameters)
7. [Food Parameters](#food-parameters)
8. [Container Parameters](#container-parameters)
9. [Clothing Parameters](#clothing-parameters)
10. [Advanced Parameters](#advanced-parameters)
11. [Callbacks and Events](#callbacks-and-events)
12. [Examples](#examples)
13. [Tips and Best Practices](#tips-and-best-practices)

---

## Introduction to Item Scripts

Item scripts in Project Zomboid define the properties and behavior of all items in the game. They use a simple text-based syntax that can be edited in any text editor. Each item has its own set of parameters, and depending on the item "Type", different parameters may be required.

**Important Notes:**
- When writing scripts, be guided by similar items from the vanilla game or other mods
- Not all parameters are required - only use what you need
- Parameters not in the standard list will be written as key-value pairs in the item's ModData
- Any custom parameters can be accessed via `item:getModData().MyCustomOption`

---

## Basic Item Structure

### Module Declaration
Every item script must be contained within a module block:

```
module MyModName {
    imports {
        Base
    }
    
    item MyItem {
        Type = Normal,
        DisplayName = My Custom Item,
        Icon = MyIcon,
        Weight = 0.1,
    }
}
```

### Key Structure Rules:
- **Module Name**: Used as prefix for item's full type (e.g., `MyModName.MyItem`)
- **Imports**: Import other modules if needed (most vanilla items use `Base`)
- **Syntax**: Uses `property = value,` format
- **Comments**: Use `/** comment **/` for multi-line comments

---

## Essential Parameters

These parameters are fundamental to most items:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **Type** | String | Item category/type | `Normal`, `Weapon`, `Food`, `Container` |
| **DisplayName** | String | Name shown in game | `Baseball Bat` |
| **Icon** | String | Icon filename (without extension) | `BaseballBat` |
| **Weight** | Float | Item weight in pounds | `0.8` |
| **DisplayCategory** | String | Category in inventory | `Weapon`, `Food`, `Tools` |

---

## Item Types

The `Type` parameter determines how the item behaves in game:

### Common Types:
- **`Normal`** - Standard items (tools, materials, etc.)
- **`Weapon`** - Melee and ranged weapons
- **`Food`** - Edible items
- **`Container`** - Bags, boxes, storage items
- **`Clothing`** - Wearable items
- **`Literature`** - Books, magazines, maps
- **`Drainable`** - Items with liquid content
- **`Key`** - Keys for doors/vehicles
- **`KeyRing`** - Key storage items
- **`AlarmClock`** - Time-based items
- **`AlarmClockClothing`** - Wearable time items

---

## Core Parameters Reference

### Basic Properties
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `Type` | String | Item type/category | Required |
| `DisplayName` | String | Display name in UI | Required |
| `Icon` | String | Icon image name | Required |
| `Weight` | Float | Weight in pounds | `1.0` |
| `DisplayCategory` | String | Inventory category | `""` |
| `Count` | Integer | Stack size multiplier | `1` |
| `Tooltip` | String | Custom tooltip text | `""` |

### Durability and Condition
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `ConditionMax` | Integer | Maximum condition | `10` |
| `ConditionLowerChanceOneIn` | Integer | Condition loss chance (1 in X) | `0` |
| `Wet` | Boolean | Can get wet | `TRUE` |
| `Obsolete` | Boolean | Item is obsolete | `FALSE` |
| `IsCookable` | Boolean | Can be cooked | `FALSE` |

### World Interaction
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `WorldStaticModel` | String | 3D model for world placement | `""` |
| `StaticModel` | String | Alternative static model | `""` |
| `CanStoreWater` | Boolean | Can hold water | `FALSE` |
| `ReplaceOnUse` | String | Item to replace when used | `""` |
| `UseWhileEquipped` | Boolean | Can use while equipped | `TRUE` |

### Tags and Categories
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `Tags` | String | Semicolon-separated tags | `""` |
| `Categories` | String | Semicolon-separated categories | `""` |
| `SubCategory` | String | Weapon subcategory | `""` |

---

## Weapon Parameters

Weapons require additional parameters for combat mechanics:

### Basic Combat Stats
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `MinDamage` | Float | Minimum damage | `0.1` |
| `MaxDamage` | Float | Maximum damage | `1.0` |
| `BaseSpeed` | Float | Attack speed multiplier | `1.0` |
| `CriticalChance` | Integer | Critical hit chance (0-100) | `0` |
| `CritDmgMultiplier` | Float | Critical damage multiplier | `2.0` |

### Range and Targeting
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `MinRange` | Float | Minimum attack range | `0.61` |
| `MaxRange` | Float | Maximum attack range | `1.55` |
| `MaxHitCount` | Integer | Max targets per swing | `1` |
| `MinAngle` | Float | Minimum hit angle | `0.8` |

### Weapon Behavior
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `SwingTime` | Float | Swing duration | `2.0` |
| `SwingAnim` | String | Swing animation | `Bat` |
| `TwoHandWeapon` | Boolean | Requires two hands | `FALSE` |
| `WeaponSprite` | String | Weapon sprite when equipped | `""` |
| `AttachmentType` | String | Where weapon attaches | `""` |

### Audio
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `SwingSound` | String | Sound when swinging | `""` |
| `HitSound` | String | Sound when hitting target | `""` |
| `BreakSound` | String | Sound when weapon breaks | `""` |
| `DoorHitSound` | String | Sound when hitting door | `""` |
| `HitFloorSound` | String | Sound when hitting floor | `""` |

### Knockback and Effects
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `KnockBackOnNoDeath` | Boolean | Knockback non-fatal hits | `TRUE` |
| `KnockdownMod` | Float | Knockdown chance modifier | `1.0` |
| `PushBackMod` | Float | Pushback force modifier | `1.0` |
| `SplatBloodOnNoDeath` | Boolean | Blood splatter on non-fatal | `TRUE` |
| `SplatNumber` | Integer | Number of blood splatters | `1` |

### Special Damage
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `DoorDamage` | Integer | Damage to doors | `1` |
| `TreeDamage` | Integer | Damage to trees | `0` |
| `MetalValue` | Integer | Metal salvage value | `0` |
| `FirePower` | Integer | Fire damage | `0` |

---

## Food Parameters

Food items require nutrition and freshness parameters:

### Nutrition
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `HungerChange` | Integer | Hunger restoration (-100 to 100) | `0` |
| `ThirstChange` | Integer | Thirst restoration (-100 to 100) | `0` |
| `Calories` | Integer | Caloric value | `0` |
| `Carbohydrates` | Float | Carbohydrate content | `0` |
| `Lipids` | Float | Fat content | `0` |
| `Proteins` | Float | Protein content | `0` |

### Freshness and Spoilage
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `DaysFresh` | Integer | Days until spoiled | `0` |
| `DaysTotallyRotten` | Integer | Days until completely rotten | `0` |
| `HoursFresh` | Integer | Hours until spoiled | `0` |
| `HoursTotallyRotten` | Integer | Hours until completely rotten | `0` |

### Cooking
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `IsCookable` | Boolean | Can be cooked | `FALSE` |
| `MinutesToCook` | Integer | Cooking time in minutes | `0` |
| `MinutesToBurn` | Integer | Time to burn after cooking | `0` |
| `ReplaceOnCooked` | String | Item when cooked | `""` |

### Effects
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `Alcoholic` | Boolean | Contains alcohol | `FALSE` |
| `Poison` | Boolean | Is poisonous | `FALSE` |
| `PoisonDetectionLevel` | Integer | Cooking skill to detect poison | `0` |
| `BoredomChange` | Integer | Boredom change when eaten | `0` |
| `UnhappyChange` | Integer | Unhappiness change when eaten | `0` |

---

## Container Parameters

Containers store other items:

### Storage
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `Capacity` | Integer | Number of slots | `10` |
| `WeightReduction` | Integer | Weight reduction percentage | `0` |
| `CanBeEquipped` | String | Where it can be equipped | `""` |
| `AttachmentType` | String | Attachment type | `""` |

### Access Control
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `OnlyAcceptCategory` | String | Only accept items of category | `""` |
| `AcceptItemFunction` | String | Lua function for item acceptance | `""` |

---

## Clothing Parameters

Clothing items have protection and temperature properties:

### Equipment
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `BodyLocation` | String | Where worn on body | Required |
| `CanBeEquipped` | String | Equipment slot | Required |
| `ClothingItem` | String | Clothing item type | `""` |

### Protection
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `ScratchDefense` | Integer | Scratch protection (0-100) | `0` |
| `BiteDefense` | Integer | Bite protection (0-100) | `0` |
| `BulletDefense` | Integer | Bullet protection (0-100) | `0` |
| `BluntDefense` | Integer | Blunt protection (0-100) | `0` |

### Temperature
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `Insulation` | Float | Heat insulation | `0` |
| `WindResistance` | Float | Wind protection | `0` |
| `WaterResistance` | Integer | Water protection (0-100) | `0` |

---

## Advanced Parameters

### Animations
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `IdleAnim` | String | Idle animation | `""` |
| `RunAnim` | String | Running animation | `""` |
| `SwingAnim` | String | Swing animation | `""` |

### Special Properties
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `SurvivalGear` | Boolean | Counts as survival gear | `FALSE` |
| `Ranged` | Boolean | Is ranged weapon | `FALSE` |
| `RequiresEquippedBothHands` | Boolean | Needs both hands equipped | `FALSE` |
| `FabricType` | String | Type of fabric (for clothing) | `""` |
| `RemoveNegativeEffectOnCreate` | Boolean | Remove negative effects | `FALSE` |

### Medical Items
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `Medical` | Boolean | Is medical item | `FALSE` |
| `Bandage` | Boolean | Is bandage | `FALSE` |
| `AlcoholPower` | Float | Alcohol strength for disinfection | `0` |

---

## Callbacks and Events

Items can have Lua callbacks for custom behavior:

### Common Callbacks
| Callback | Description | Parameters |
|----------|-------------|------------|
| `OnCreate` | Called when item is created | `item` |
| `OnEat` | Called when item is eaten | `item, character, amount` |
| `OnCooked` | Called when item is cooked | `item` |

### Example:
```
item MyCustomFood {
    Type = Food,
    DisplayName = Custom Food,
    OnEat = MyMod.OnEatCustomFood,
    OnCreate = MyMod.OnCreateCustomFood,
}
```

---

## Examples

### Basic Item
```
module MyMod {
    item Screwdriver {
        Type = Normal,
        DisplayName = Screwdriver,
        DisplayCategory = Tools,
        Icon = Screwdriver,
        Weight = 0.2,
        MetalValue = 10,
        Tags = CraftingTool,
    }
}
```

### Weapon
```
module MyMod {
    item CustomSword {
        Type = Weapon,
        DisplayName = Custom Sword,
        DisplayCategory = Weapon,
        Icon = CustomSword,
        Weight = 1.5,
        SubCategory = LongBlade,
        Categories = Blade,
        MinDamage = 1.2,
        MaxDamage = 2.8,
        BaseSpeed = 0.9,
        CriticalChance = 10,
        CritDmgMultiplier = 3.0,
        MinRange = 0.61,
        MaxRange = 1.8,
        SwingAnim = Stab,
        WeaponSprite = CustomSword,
        TwoHandWeapon = TRUE,
        SwingSound = BladeSlash,
        HitSound = BladeHit,
        ConditionMax = 10,
        ConditionLowerChanceOneIn = 5,
    }
}
```

### Food Item
```
module MyMod {
    item CustomApple {
        Type = Food,
        DisplayName = Custom Apple,
        DisplayCategory = Food,
        Icon = CustomApple,
        Weight = 0.1,
        HungerChange = -15,
        ThirstChange = 5,
        Calories = 80,
        Carbohydrates = 20,
        DaysFresh = 5,
        DaysTotallyRotten = 10,
        IsCookable = TRUE,
        MinutesToCook = 20,
        ReplaceOnCooked = Base.BakedApple,
    }
}
```

### Container
```
module MyMod {
    item BigBackpack {
        Type = Container,
        DisplayName = Big Backpack,
        DisplayCategory = Container,
        Icon = BigBackpack,
        Weight = 2.0,
        Capacity = 30,
        WeightReduction = 80,
        CanBeEquipped = Back,
        AttachmentType = Bag,
    }
}
```

### Clothing
```
module MyMod {
    item ArmoredJacket {
        Type = Clothing,
        DisplayName = Armored Jacket,
        DisplayCategory = Clothing,
        Icon = ArmoredJacket,
        Weight = 3.0,
        BodyLocation = Torso_Upper,
        CanBeEquipped = Torso1_Upper,
        ClothingItem = Jacket,
        ScratchDefense = 80,
        BiteDefense = 60,
        BulletDefense = 40,
        BluntDefense = 70,
        Insulation = 0.8,
        WindResistance = 0.9,
        WaterResistance = 50,
        FabricType = Leather,
    }
}
```

---

## Tips and Best Practices

### Development Tips
1. **Start Simple**: Begin with basic items and add complexity gradually
2. **Study Vanilla Items**: Examine existing item scripts for guidance
3. **Use Comments**: Document your scripts for future reference
4. **Test Thoroughly**: Always test items in-game before release

### Parameter Guidelines
1. **Required Parameters**: Always include Type, DisplayName, and Icon
2. **Realistic Values**: Keep weights and stats realistic for game balance
3. **Consistent Naming**: Use clear, descriptive names for items
4. **Icon Files**: Ensure icon files exist in your mod's media/ui folder

### Performance Considerations
1. **Minimal Callbacks**: Only use callbacks when necessary
2. **Efficient Tags**: Use tags sparingly and meaningfully
3. **Sound Files**: Ensure referenced sound files exist

### Modding Etiquette
1. **Unique Names**: Use your mod name as prefix to avoid conflicts
2. **Clear Documentation**: Document any special requirements
3. **Version Compatibility**: Test with current game versions

### Common Mistakes to Avoid
1. **Missing Icons**: Forgetting to include icon files
2. **Invalid Types**: Using non-existent item types
3. **Syntax Errors**: Missing commas or incorrect formatting
4. **Unrealistic Stats**: Values that break game balance

### Testing Your Items
1. **Spawn in Debug**: Use debug mode to spawn and test items
2. **Check Tooltips**: Verify all information displays correctly
3. **Test Interactions**: Ensure items work with recipes and mechanics
4. **Multiplayer Testing**: Test in multiplayer environments if applicable

---

This comprehensive guide covers the essential aspects of Project Zomboid item scripting. For the most up-to-date parameter list and examples, always refer to the vanilla game files and the Project Zomboid wiki.
# Project Zomboid Lua Modding Documentation

*Generated from: https://demiurgequantified.github.io/ProjectZomboidLuaDocs/*
*This is unofficial documentation based on the javadocs extracted from the game*

---

## Table of Contents

1. [Introduction](#introduction)
2. [Events System](#events-system)
3. [Hooks System](#hooks-system)
4. [Callbacks System](#callbacks-system)
5. [Essential Event Reference](#essential-event-reference)
6. [Essential Hook Reference](#essential-hook-reference)
7. [Essential Callback Reference](#essential-callback-reference)

---

## Introduction

Welcome to the Project Zomboid Lua modding documentation! This guide covers the essential systems for building mods with Lua and the game's scripting language.

**Important Notes:**
- This documentation is based on javadocs generated directly from the game code
- Lua is dynamically typed, so type inference may sometimes be incorrect
- These docs are community-maintained and may have gaps
- Always test your implementations against the actual game behavior

---

## Events System

Events are triggered automatically by the game at specific times. You register event handlers using `Events.EventName.Add(yourFunction)`.

### Event Registration Pattern
```lua
local function onPlayerDeath(player)
    print("Player died: " .. player:getDisplayName())
end

Events.OnPlayerDeath.Add(onPlayerDeath)
```

### Key Timing Events

**EveryDays**: Fires at 0:00 every in-game day
- No parameters

**EveryHours**: Fires at the start of every in-game hour  
- No parameters

**EveryOneMinute**: Fires every in-game minute
- No parameters

**EveryTenMinutes**: Fires every ten in-game minutes
- No parameters

**OnTick**: Fires every game tick
- `tick` (number): The number of ticks since the game started

**OnTickEvenPaused**: Fires every game tick, even if the game is paused
- `tick` (number): The number of ticks since the game started. Always zero while paused

### Character & Player Events

**OnCreatePlayer** (Client): Fires every time a local player loads into the world
- `playerNum` (integer): The player number of the newly-spawned character
- `player` (IsoPlayer): The new player object

**OnPlayerDeath** (Client): Fires when a local player dies
- `player` (IsoPlayer): The player who died

**OnCharacterDeath**: Fires when any character dies, including zombies, players and animals
- `character` (IsoGameCharacter): The character who died

**OnPlayerUpdate** (Client): Fires during each local player's update (every tick)
- `player` (IsoPlayer): The player being updated

**OnPlayerMove** (Client): Fires during each local player's update if they are walking
- `character` (IsoPlayer): The moving character

**AddXP** (Client): Fires after a local character gains perk XP, except when the XP source specifically requested not to
- `character` (IsoGameCharacter): The character who gained the XP
- `perk` (PerkFactory.Perk): The perk XP was gained in
- `amount` (number): The amount of XP gained. This is the final value after all modifiers

**LevelPerk** (Client): Fires after a local character gains or loses a perk level
- `character` (IsoGameCharacter): The character whose perk level changed
- `perk` (PerkFactory.Perk): The perk that changed level
- `level` (integer): The new level of the perk
- `increased` (boolean): True if the level increased, false if it decreased

### Game State Events

**OnGameBoot**: Fires after the game finishes starting up
- No parameters
- Note: For clients, lua files in lua/server/ will not have loaded by the time this event is fired

**OnGameStart** (Client): Fires upon finishing loading and entering the game
- No parameters

**OnLoad** (Client): Fires upon finishing loading and entering the game
- No parameters

**OnInitGlobalModData**: Fires when GlobalModData is initialised. This is the earliest event after Sandbox Options are loaded
- `newGame` (boolean): True if this is the first time the save has started

**OnSave**: Fires while saving the world, after characters and sandbox options have been saved, but before global mod data and the world have been saved
- No parameters

**OnPostSave**: Fires after saving and exiting the game
- No parameters

### World & Object Events

**LoadGridsquare**: Fires after a new square is loaded
- `square` (IsoGridSquare): The square that was loaded

**OnObjectAdded**: Fires when an object is added to the world
- `object` (IsoObject): The object that was added

**OnObjectAboutToBeRemoved**: Fires before a tile object is destroyed or picked up
- `object` (IsoObject): The object about to be removed

**OnTileRemoved**: Fires when a tile object is removed
- `object` (IsoObject): The object being removed

**OnNewFire**: Fires when a new fire is started
- `fire` (IsoFire): The fire that was created

### Combat Events

**OnHitZombie**: Fires whenever a zombie is hit by a character
- `zombie` (IsoZombie): The zombie that was hit
- `attacker` (IsoGameCharacter): The character that hit the zombie
- `bodyPart` (BodyPartType): The type of the body part that was hit
- `weapon` (HandWeapon): The weapon the zombie was hit with

**OnWeaponSwing**: Fires when a player begins swinging a weapon
- `attacker` (IsoPlayer): The character attacking
- `weapon` (HandWeapon): The weapon being attacked with

**OnPlayerAttackFinished** (Client): Fires when a local player finishes attacking
- `player` (IsoPlayer): The player who attacked
- `weapon` (HandWeapon): The weapon the player attacked with

### Vehicle Events

**OnEnterVehicle** (Client): Fires when a character enters a vehicle
- `character` (IsoGameCharacter): The character that entered the vehicle

**OnExitVehicle** (Client): Fires when a character exits a vehicle
- `character` (IsoGameCharacter): The character that exited the vehicle

**OnSwitchVehicleSeat** (Client): Fires when a local character moves seats in a vehicle
- `character` (IsoGameCharacter): The character who moved seats

### Multiplayer Events

**OnServerCommand** (Client): Fires when a server command sent through sendServerCommand is received by the client
- `module` (string): The module the command was sent with
- `command` (string): The command the command was sent with  
- `args` (table or nil): The arguments table the command was sent with

**OnClientCommand** (Server): Fires when a client command sent through sendClientCommand is received by the server
- `module` (string): The module the command was sent with
- `command` (string): The command the command was sent with
- `player` (IsoPlayer): The player who sent the command
- `args` (table or nil): The arguments table the command was sent with

### Container & Loot Events

**OnFillContainer** (Server): Fires whenever a container is first filled with loot, or when loot respawns
- `roomType` (string): Distribution type of the room the container is in, or the type of the vehicle
- `containerType` (string): The type of the container that was filled
- `container` (ItemContainer): The container that was filled

**OnDistributionMerge**: Fires when the distribution tables merge
- No parameters

**OnPostDistributionMerge**: Fires after the distribution tables have been merged
- No parameters

### Input Events

**OnKeyPressed** (Client): Fires when a key is released
- `key` (integer): Key code of the key that was released

**OnKeyStartPressed** (Client): Fires when a key starts being pressed
- `key` (integer): Key code of the key that was pressed

**OnKeyKeepPressed** (Client): Fires every frame while a key is held down
- `key` (integer): Key code of the key that was held

**OnMouseDown** (Client): Fires when the player left clicks, as long as the input isn't eaten by UI
- `x` (number): Screen X co-ordinate of the click
- `y` (number): Screen Y co-ordinate of the click

**OnRightMouseDown** (Client): Fires when the player right clicks, as long as the input isn't eaten by UI
- `x` (number): Screen X co-ordinate of the click
- `y` (number): Screen Y co-ordinate of the click

### Context Menu Events

**OnFillWorldObjectContextMenu** (Client): Fires after a world context menu is filled
- `playerNum` (integer): The number of the player whose context menu has been filled
- `context` (ISContextMenu): The context menu that was filled
- `worldObjects` (IsoObject[]): The objects that were right clicked on
- `test` (boolean): Whether the context menu was filled to test for interactive objects

**OnFillInventoryObjectContextMenu** (Client): Fires after the context menu for an inventory item is filled
- `playerNum` (integer): The number of the player whose context menu has been filled
- `context` (ISContextMenu): The context menu that was filled
- `items` (InventoryItem[] or ContextMenuItemStack[]): The items that were selected

---

## Hooks System

Hooks are called during specific game calculations and allow you to modify the behavior. Register with `LuaEventManager.AddEvent("HookName")`.

### Hook Registration Pattern
```lua
local function modifyAttack(attacker, chargeDelta, weapon)
    -- Modify attack behavior
    print("Character attacking with: " .. weapon:getDisplayName())
end

LuaEventManager.AddEvent("Attack")
Events.Attack.Add(modifyAttack)
```

### Combat Hooks

**Attack** (Client): Called every tick while a local character is pressing their attack button and is able to attack
- `attacker` (IsoLivingCharacter): The character attempting to attack
- `chargeDelta` (number): Charge delta value
- `weapon` (HandWeapon): The weapon being used

**WeaponSwing**: Called when a weapon is swung to find targets
- `character` (IsoGameCharacter): The character swinging
- `weapon` (HandWeapon): The weapon being swung

**WeaponHitCharacter**: Called when the effects of an attack are being calculated
- `attacker` (IsoGameCharacter): The attacking character
- `target` (IsoGameCharacter): The target character
- `weapon` (HandWeapon): The weapon used
- `damageSplit` (number): Damage split value

### Character State Hooks

**CalculateStats** (Client): Called when a character's stats are being updated (health not included)
- `character` (IsoGameCharacter): The character whose stats are being calculated

**AutoDrink** (Client): Called whenever a character automatically drinks while auto-drink is turned on
- `character` (IsoGameCharacter): The character auto-drinking

### General Action Hook

**ContextualAction**: Called for various contextual actions
- `actionType` (string): Type of action
- `character` (IsoGameCharacter): Character performing action
- `object` (any): Object involved
- `arg1` (any): Additional argument
- `arg2` (any): Additional argument
- `arg3` (any): Additional argument

---

## Callbacks System

Callbacks are specific functions that can be assigned to items, recipes, and other game objects in their definitions.

### Item Callbacks

**Item_OnCreate**: Called when the item is first created, before it is placed into its container
- `item` (InventoryItem): The item being created

**Item_OnEat**: Called when a player eats the item (client eating only)
- `item` (InventoryItem): The item being eaten
- `character` (IsoGameCharacter): The character eating the item
- `amount` (number): The fraction of the item that was eaten

**Item_OnCooked**: Called when the item is cooked (doesn't fire if item has ReplaceOnCooked)
- `item` (InventoryItem): The item being cooked

**Item_AcceptItemFunction**: Called when checking if an item is allowed inside a container
- `container` (ItemContainer): The container the item is being added to
- `item` (InventoryItem): The item being added to the container
- Returns: `acceptItem` (boolean): Whether to allow the item in the container

### Recipe Callbacks

**Recipe_OnCreate**: Called after crafting the recipe
- `sources` (ArrayList<InventoryItem>): The items used to craft the recipe
- `result` (InventoryItem): The item crafted by the recipe
- `character` (IsoGameCharacter): The character who crafted the recipe
- `item` (InventoryItem): The item used in the crafting action
- `isPrimaryHandItem` (boolean): True if item is equipped in primary hand
- `isSecondaryHandItem` (boolean): True if item is equipped in secondary hand

**Recipe_OnCanPerform**: Called when checking if a character is able to perform the recipe
- `recipe` (Recipe): The recipe being checked
- `character` (IsoGameCharacter): The character the recipe is being checked for
- `item` (InventoryItem or nil): The item the player right clicked
- Returns: `canPerform` (boolean): Whether to allow the character to craft the recipe

**Recipe_OnTest**: Called when checking if an item is allowed to be used in a recipe
- `item` (InventoryItem): The item being checked
- `result` (Recipe.Result): The result of the recipe
- Returns: `test` (boolean): Whether to allow the item into the recipe

**Recipe_OnGiveXP**: Called after crafting the recipe
- `recipe` (Recipe): The recipe that was crafted
- `sources` (ArrayList<InventoryItem>): The items used to craft the recipe
- `result` (InventoryItem): The item crafted by the recipe
- `character` (IsoGameCharacter): The character who crafted the recipe

**Recipe_GetItemTypes**: Called by the recipe manager for every recipe source after lua/server/ loads
- `outItems` (ArrayList<Item>): An empty ArrayList to be filled with items

### Craft Recipe Callbacks (Build 42)

**CraftRecipe_OnCreate**: Called when successfully crafting the recipe
- `recipeData` (CraftRecipeData): Recipe data
- `character` (IsoGameCharacter or nil): The character who crafted the recipe

**CraftRecipe_OnStart**: Called at the start of crafting the recipe
- `recipeData` (CraftRecipeData): Recipe data
- `character` (IsoGameCharacter or nil): The character crafting the recipe

**CraftRecipe_OnUpdate**: Called every tick while crafting the recipe
- `recipeData` (CraftRecipeData): Recipe data

**CraftRecipe_OnFailed**: Called when failing to craft the recipe
- `recipeData` (CraftRecipeData): Recipe data

**CraftRecipe_OnTest**: Called when checking if an item can be used in the recipe
- `item` (InventoryItem): The item being tested
- Returns: `test` (boolean): Whether to allow the item in the recipe

### Vehicle Part Callbacks

**VehiclePart_Install_test**: Called when testing if the part can be installed
- `vehicle` (BaseVehicle): The vehicle the part belongs to
- `part` (VehiclePart): The part being tested
- `character` (IsoGameCharacter): The character using the part
- Returns: `test` (boolean): Whether the part can be installed

**VehiclePart_Install_complete**: Called after the part is successfully installed
- `vehicle` (BaseVehicle): The vehicle the part belongs to
- `part` (VehiclePart): The part that was installed

**VehiclePart_Uninstall_test**: Called when testing if the part can be uninstalled
- `vehicle` (BaseVehicle): The vehicle the part belongs to
- `part` (VehiclePart): The part being tested
- `character` (IsoGameCharacter): The character using the part
- Returns: `test` (boolean): Whether the part can be uninstalled

**VehiclePart_Uninstall_complete**: Called after the part is successfully uninstalled
- `vehicle` (BaseVehicle): The vehicle the part belongs to
- `part` (VehiclePart): The part that was uninstalled
- `item` (InventoryItem): The item that was removed

**VehiclePart_create**: Called when the part is spawned for the first time
- `vehicle` (BaseVehicle): The vehicle the part belongs to
- `part` (VehiclePart): The part being created

**VehiclePart_init**: Called every time the part loads in or is reset
- `vehicle` (BaseVehicle): The vehicle the part belongs to
- `part` (VehiclePart): The part being initialised

**VehiclePart_update**: Called regularly to update the part (targeting every half in-game minute)
- `vehicle` (BaseVehicle): The vehicle the part belongs to
- `part` (VehiclePart): The part being updated
- `deltaMinutes` (number): The number of minutes since the last update

**VehiclePart_use**: Called when a character interacts with the vehicle while in the part's area
- `vehicle` (BaseVehicle): The vehicle the part belongs to
- `part` (VehiclePart): The part being used
- `character` (IsoGameCharacter): The character using the part

**VehiclePart_checkEngine**: Called every tick while the engine is running
- `vehicle` (BaseVehicle): The vehicle the part belongs to
- `part` (VehiclePart): The part being checked
- Returns: `working` (boolean): Whether the engine should be working

**VehiclePart_checkOperate**: Called every tick while a player is in the driver's seat
- `vehicle` (BaseVehicle): The vehicle the part belongs to
- `part` (VehiclePart): The part being checked
- Returns: `operable` (boolean): Whether the vehicle is operable

### Container Callbacks

**ItemContainer_Predicate**: Used by -Eval methods in ItemContainer to filter items
- `item` (InventoryItem): The item being tested
- Returns: `allowItem` (boolean): Whether the item is a valid match

**ItemContainer_Comparator**: Used by getBest methods in ItemContainer to sort matches
- `a` (InventoryItem): The first item being tested
- `b` (InventoryItem): The second item being tested
- Returns: (number): Positive if a should be prioritised over b, negative if b should be prioritised

---

## Essential Event Reference

### Most Commonly Used Events for Modding

1. **OnGameBoot** - Initialize your mod
2. **OnCreatePlayer** - Set up player-specific data
3. **OnTick** - Continuous updates
4. **OnFillWorldObjectContextMenu** - Add context menu options
5. **OnPlayerDeath** - Handle player death
6. **OnHitZombie** - Modify combat
7. **OnFillContainer** - Modify loot spawning
8. **AddXP** - Modify experience gains
9. **OnKeyPressed** - Handle custom keybinds
10. **OnServerCommand/OnClientCommand** - Multiplayer communication

### Event Timing Guidelines
- Use **OnGameBoot** for one-time initialization
- Use **OnTick** sparingly (performance impact)
- Use **EveryOneMinute** or **EveryTenMinutes** for periodic checks
- Use **OnLoad** for player-specific setup

---

## Essential Hook Reference

### Most Commonly Used Hooks for Modding

1. **CalculateStats** - Modify character stats
2. **Attack** - Modify attack behavior
3. **WeaponHitCharacter** - Modify damage calculation
4. **AutoDrink** - Modify auto-drink behavior

### Hook Performance Notes
- Hooks are called frequently - keep them optimized
- Return values affect game behavior
- Test thoroughly as hooks can break game balance

---

## Essential Callback Reference

### Most Commonly Used Callbacks for Modding

1. **Item_OnCreate** - Initialize custom items
2. **Recipe_OnCreate** - Handle recipe crafting
3. **Recipe_OnCanPerform** - Control recipe availability
4. **Item_OnEat** - Handle food effects
5. **VehiclePart_update** - Vehicle part behavior

### Callback Implementation Notes
- Callbacks are assigned in item/recipe definitions
- OnCooked functions cannot be inside tables
- Always handle nil parameters appropriately

---

This documentation provides the essential foundation for Project Zomboid Lua modding. For complete class and method references, refer to the full documentation site.
# Project Zomboid Fluid Scripts Guide (Build 42)

*Compiled from Project Zomboid Wiki and community documentation*

**Note**: This guide covers Build 42 fluid system. Fluid scripts define liquids that can be stored, mixed, and consumed in the new fluid transfer system introduced in Build 42.

---

## Table of Contents

1. [Introduction to Fluid Scripts](#introduction-to-fluid-scripts)
2. [Basic Structure](#basic-structure)
3. [Core Parameters Reference](#core-parameters-reference)
4. [Color System](#color-system)
5. [Categories](#categories)
6. [Blending System](#blending-system)
7. [Properties](#properties)
8. [Poison System](#poison-system)
9. [Examples](#examples)
10. [Tips and Best Practices](#tips-and-best-practices)

---

## Introduction to Fluid Scripts

Fluid scripts in Project Zomboid Build 42 define liquids that can be stored in containers, mixed together, and consumed by players. The fluid system is part of the major crafting overhaul in Build 42, allowing for complex liquid interactions including cocktails, fuel mixtures, medicines, poisons, and industrial chemicals.

### Key Concepts:
- **Global Registry**: All fluids are stored in a global registry for easy modding
- **Categories**: Fluids belong to categories like Beverage, Fuel, Medical, etc.
- **Properties**: Each fluid has nutritional, medical, and effect properties
- **Blending**: Fluids can be mixed with rules for compatibility
- **Visual Identity**: Each fluid has color and display properties
- **Poison System**: Hazardous fluids can have toxic effects

### Important Notes:
- Fluid scripts use `property = value` syntax with some special formatting
- Colors use RGB01 format (0.0 to 1.0 decimal values)
- Blending rules determine which fluids can be mixed
- Properties are calculated per liter of fluid

---

## Basic Structure

### Standard Syntax
```
module ModuleName {
    fluid FluidName {
        Color = red : green : blue,
        ColorReference = ColorName,
        DisplayName = TRANSLATION_KEY,
        
        Categories {
            Category1,
            Category2,
        }
        
        Properties {
            /* Nutritional and effect properties */
        }
        
        Poison {
            /* Toxicity properties */
        }
        
        BlendWhiteList {
            /* Mixing compatibility rules */
        }
    }
}
```

### Essential Elements:
1. **Color**: Visual appearance of the fluid
2. **DisplayName**: Translation key for the fluid name
3. **Categories**: What type of fluid this is
4. **Properties**: Effects when consumed
5. **Blending Rules**: What this fluid can mix with

---

## Core Parameters Reference

### Identification Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **DisplayName** | String | Translation key for display name | `DisplayName = FLUID_WATER` |

### Visual Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **Color** | RGB01 | Color in decimal format (0.0-1.0) | `Color = 1.000 : 0.894 : 0.769` |
| **ColorReference** | String | Named color reference | `ColorReference = Red` |

### Categorization

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **Categories** | Block | List of fluid categories | See [Categories](#categories) section |

### Interaction Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **BlendWhiteList** | String/Block | Reference to filter or inline rules | See [Blending System](#blending-system) |
| **BlendBlackList** | String/Block | Fluids this cannot mix with | See [Blending System](#blending-system) |

---

## Color System

### RGB01 Format
Colors use decimal values from 0.0 to 1.0:
```
fluid RedLiquid {
    Color = 1.0 : 0.0 : 0.0,  // Pure red
}

fluid BlueLiquid {
    Color = 0.0 : 0.0 : 1.0,  // Pure blue
}

fluid YellowLiquid {
    Color = 1.0 : 1.0 : 0.0,  // Yellow (red + green)
}

fluid PurpleLiquid {
    Color = 0.5 : 0.0 : 0.5,  // Dark purple
}
```

### Color References
Use predefined color names:
```
fluid WaterFluid {
    ColorReference = Blue,
}

fluid BloodFluid {
    ColorReference = Red,
}

fluid GasolineFluid {
    ColorReference = Yellow,
}
```

### Common Color Values
```
// Basic Colors
White:    1.0 : 1.0 : 1.0
Black:    0.0 : 0.0 : 0.0
Red:      1.0 : 0.0 : 0.0
Green:    0.0 : 1.0 : 0.0
Blue:     0.0 : 0.0 : 1.0
Yellow:   1.0 : 1.0 : 0.0
Cyan:     0.0 : 1.0 : 1.0
Magenta:  1.0 : 0.0 : 1.0

// Realistic Fluid Colors
Water:        0.8 : 0.9 : 1.0    // Light blue
Gasoline:     1.0 : 0.9 : 0.7    // Yellowish
Motor Oil:    0.1 : 0.1 : 0.1    // Nearly black
Orange Juice: 1.0 : 0.6 : 0.0    // Orange
Milk:         0.95 : 0.95 : 0.9   // Off-white
Blood:        0.7 : 0.1 : 0.1     // Dark red
```

---

## Categories

### Standard Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| **Beverage** | Drinks for consumption | Water, Soda, Juice |
| **Alcoholic** | Alcoholic beverages | Beer, Wine, Whiskey |
| **Industrial** | Industrial fluids | Oil, Coolant, Lubricant |
| **Medical** | Medical substances | Disinfectant, Medicine |
| **Chemical** | Chemical substances | Bleach, Acid, Solvent |
| **Fuel** | Combustible fluids | Gasoline, Diesel, Kerosene |
| **Flammable** | Fire-related fluids | Alcohol, Fuel, Accelerant |
| **Food** | Liquid food items | Milk, Soup, Sauce |
| **Cleaning** | Cleaning products | Soap, Detergent, Disinfectant |

### Category Usage
```
fluid Gasoline {
    Categories {
        Fuel,
        Flammable,
        Industrial,
    }
}

fluid Beer {
    Categories {
        Beverage,
        Alcoholic,
    }
}

fluid DisinfectantAlcohol {
    Categories {
        Medical,
        Alcoholic,
        Cleaning,
    }
}
```

---

## Blending System

### Whitelist by Reference
Reference an external filter script:
```
fluid MixableFluid {
    BlendWhiteList = MyFluidFilter,
    BlendBlackList = RestrictedFluidFilter,
}
```

### Inline Whitelist Rules
Define mixing rules directly:
```
fluid Alcohol {
    BlendWhiteList {
        whitelist = true,
        fluids {
            Water,
            FruitJuice,
            Soda,
        }
        categories {
            Beverage,
            Medical,
        }
    }
}
```

### Blacklist Rules
Prevent mixing with specific fluids:
```
fluid GasolineFuel {
    BlendBlackList {
        whitelist = false,
        fluids {
            Water,
            Blood,
        }
        categories {
            Beverage,
            Food,
        }
    }
}
```

### Complex Blending Example
```
fluid UniversalSolvent {
    BlendWhiteList {
        whitelist = true,
        fluids {
            Water,
            Alcohol,
            Oil,
        }
        categories {
            Chemical,
            Industrial,
            Cleaning,
        }
    }
    
    BlendBlackList {
        whitelist = false,
        fluids {
            Acid,
            Bleach,
        }
        categories {
            Explosive,
        }
    }
}
```

---

## Properties

### Nutritional Properties

| Property | Type | Description | Range |
|----------|------|-------------|-------|
| **calories** | Float | Calories per liter | 0.0+ |
| **carbohydrates** | Float | Carbohydrate content | 0.0+ |
| **lipids** | Float | Fat content | 0.0+ |
| **proteins** | Float | Protein content | 0.0+ |

### Status Effect Properties

| Property | Type | Description | Range |
|----------|------|-------------|-------|
| **hungerChange** | Float | Hunger level change | Negative = reduces hunger |
| **thirstChange** | Float | Thirst level change | Negative = reduces thirst |
| **fatigueChange** | Float | Fatigue level change | Negative = reduces fatigue |
| **stressChange** | Float | Stress level change | Negative = reduces stress |
| **unhappyChange** | Float | Unhappiness level change | Negative = reduces sadness |

### Medical Properties

| Property | Type | Description | Range |
|----------|------|-------------|-------|
| **alcohol** | Float | Alcohol content percentage | 0.0-1.0 |
| **fluReduction** | Float | Flu symptom reduction | 0.0+ |
| **painReduction** | Float | Pain reduction amount | 0.0+ |
| **enduranceChange** | Float | Endurance modification | Can be positive/negative |
| **foodSicknessReduction** | Float | Food poisoning reduction | 0.0+ |

### Properties Example
```
fluid Beer {
    Properties {
        calories = 150,
        carbohydrates = 12,
        lipids = 0,
        proteins = 1,
        alcohol = 0.05,              // 5% alcohol
        thirstChange = -10,          // Reduces thirst slightly
        unhappyChange = -5,          // Improves mood slightly
        stressChange = -3,           // Reduces stress
        hungerChange = 2,            // Slightly increases hunger
    }
}

fluid EnergyDrink {
    Properties {
        calories = 160,
        carbohydrates = 40,
        caffeine = 80,               // Custom property
        thirstChange = -15,
        fatigueChange = -20,         // Reduces fatigue significantly
        enduranceChange = 10,        // Temporary endurance boost
        stressChange = 5,            // Slightly increases stress
    }
}

fluid Medicine {
    Properties {
        painReduction = 30,
        fluReduction = 25,
        foodSicknessReduction = 40,
        stressChange = -2,
        thirstChange = 1,            // Slightly increases thirst
    }
}
```

---

## Poison System

### Poison Parameters

| Parameter | Type | Description | Values |
|-----------|------|-------------|--------|
| **maxEffect** | String | Maximum poison severity | None, Low, Medium, Extreme, Deadly |
| **minAmount** | Float | Minimum effective dose | 0.0-1.0 |
| **diluteRatio** | Float | Dilution effectiveness | 0.0-1.0 |

### Poison Levels
```
// Non-toxic
maxEffect = None,

// Mild poisoning
maxEffect = Low,          // Mild symptoms
maxEffect = Medium,       // Moderate symptoms  
maxEffect = Extreme,      // Severe symptoms
maxEffect = Deadly,       // Potentially fatal
```

### Poison Examples
```
fluid Bleach {
    Poison {
        maxEffect = Deadly,
        minAmount = 0.1,        // 10% concentration is dangerous
        diluteRatio = 0.8,      // Dilutes well with other fluids
    }
}

fluid SpoiledMilk {
    Poison {
        maxEffect = Medium,
        minAmount = 0.3,        // Need significant amount for effect
        diluteRatio = 0.5,      // Moderate dilution
    }
}

fluid DisinfectantAlcohol {
    Poison {
        maxEffect = Low,
        minAmount = 0.7,        // High threshold for poisoning
        diluteRatio = 0.9,      // Dilutes very effectively
    }
}

fluid IndustrialAcid {
    Poison {
        maxEffect = Deadly,
        minAmount = 0.05,       // Extremely dangerous even in small amounts
        diluteRatio = 0.3,      // Doesn't dilute easily
    }
}
```

---

## Examples

### Basic Beverage
```
module Base {
    fluid Water {
        Color = 0.8 : 0.9 : 1.0,
        DisplayName = FLUID_WATER,
        
        Categories {
            Beverage,
        }
        
        BlendWhiteList {
            whitelist = true,
            categories {
                Beverage,
                Medical,
                Food,
            }
        }
        
        Properties {
            thirstChange = -20,
            calories = 0,
            carbohydrates = 0,
            lipids = 0,
            proteins = 0,
        }
        
        Poison {
            maxEffect = None,
            minAmount = 0,
            diluteRatio = 1.0,
        }
    }
}
```

### Alcoholic Beverage
```
module Base {
    fluid Whiskey {
        Color = 0.8 : 0.6 : 0.3,
        DisplayName = FLUID_WHISKEY,
        
        Categories {
            Beverage,
            Alcoholic,
            Flammable,
        }
        
        BlendWhiteList {
            whitelist = true,
            fluids {
                Water,
                Soda,
                FruitJuice,
            }
            categories {
                Beverage,
            }
        }
        
        Properties {
            calories = 250,
            carbohydrates = 0,
            alcohol = 0.40,          // 40% alcohol
            thirstChange = 5,        // Actually increases thirst
            stressChange = -10,      // Reduces stress
            unhappyChange = -5,      // Improves mood
            fatigueChange = 5,       // Increases fatigue over time
        }
        
        Poison {
            maxEffect = Extreme,     // High alcohol content is dangerous
            minAmount = 0.3,
            diluteRatio = 0.7,
        }
    }
}
```

### Industrial Fuel
```
module Base {
    fluid Gasoline {
        Color = 1.0 : 0.9 : 0.7,
        DisplayName = FLUID_GASOLINE,
        
        Categories {
            Fuel,
            Flammable,
            Industrial,
        }
        
        BlendWhiteList {
            whitelist = true,
            fluids {
                Diesel,
                Kerosene,
            }
            categories {
                Fuel,
                Industrial,
            }
        }
        
        BlendBlackList {
            whitelist = false,
            categories {
                Beverage,
                Food,
                Medical,
            }
        }
        
        Properties {
            // No nutritional value
            calories = 0,
            carbohydrates = 0,
            lipids = 0,
            proteins = 0,
        }
        
        Poison {
            maxEffect = Deadly,
            minAmount = 0.05,        // Very toxic
            diluteRatio = 0.2,       // Doesn't dilute well
        }
    }
}
```

### Medical Fluid
```
module Base {
    fluid Disinfectant {
        Color = 0.9 : 0.9 : 1.0,
        DisplayName = FLUID_DISINFECTANT,
        
        Categories {
            Medical,
            Chemical,
            Cleaning,
        }
        
        BlendWhiteList {
            whitelist = true,
            fluids {
                Water,
                Alcohol,
            }
            categories {
                Medical,
                Cleaning,
            }
        }
        
        Properties {
            painReduction = 5,
            fluReduction = 10,
            foodSicknessReduction = 15,
            stressChange = 2,        // Stings, causes stress
        }
        
        Poison {
            maxEffect = Medium,
            minAmount = 0.2,
            diluteRatio = 0.8,
        }
    }
}
```

### Complex Mixture Fluid
```
module CustomMod {
    fluid EnergyBooster {
        Color = 0.0 : 1.0 : 0.0,
        DisplayName = FLUID_ENERGY_BOOSTER,
        
        Categories {
            Beverage,
            Medical,
        }
        
        BlendWhiteList {
            whitelist = true,
            fluids {
                Water,
                FruitJuice,
                Coffee,
            }
            categories {
                Beverage,
            }
        }
        
        Properties {
            calories = 200,
            carbohydrates = 30,
            thirstChange = -15,
            fatigueChange = -30,     // Significant fatigue reduction
            enduranceChange = 15,    // Endurance boost
            stressChange = -5,
            hungerChange = 5,        // Slightly increases hunger
        }
        
        Poison {
            maxEffect = Low,         // Mild side effects from overconsumption
            minAmount = 0.8,         // Only toxic in large amounts
            diluteRatio = 0.9,
        }
    }
}
```

### Dangerous Chemical
```
module Base {
    fluid IndustrialBleach {
        Color = 1.0 : 1.0 : 0.9,
        DisplayName = FLUID_BLEACH,
        
        Categories {
            Chemical,
            Cleaning,
            Industrial,
        }
        
        BlendWhiteList {
            whitelist = true,
            fluids {
                Water,
            }
            categories {
                Cleaning,
            }
        }
        
        BlendBlackList {
            whitelist = false,
            fluids {
                Alcohol,
                Acid,
            }
            categories {
                Beverage,
                Food,
                Fuel,
            }
        }
        
        Properties {
            // No nutritional value, only harmful
            stressChange = 20,       // Causes significant stress
            painReduction = -10,     // Actually causes pain
        }
        
        Poison {
            maxEffect = Deadly,
            minAmount = 0.02,        // Extremely dangerous
            diluteRatio = 0.6,       // Moderate dilution
        }
    }
}
```

---

## Tips and Best Practices

### Design Guidelines

1. **Realistic Properties**: Base fluid properties on real-world counterparts
   ```
   Water: No calories, reduces thirst
   Alcohol: Calories, alcohol content, affects mood
   Gasoline: Toxic, flammable, no nutrition
   ```

2. **Logical Categories**: Choose categories that make sense for the fluid's use
   ```
   Soda: Beverage
   Gasoline: Fuel, Flammable, Industrial
   Medicine: Medical, sometimes Chemical
   ```

3. **Balanced Effects**: Ensure effects are proportional to realism and gameplay
   ```
   Mild effects: ±1 to ±5
   Moderate effects: ±5 to ±15
   Strong effects: ±15 to ±30
   ```

### Color Guidelines

1. **Recognizable Colors**: Use colors that players will recognize
   ```
   Water: Light blue
   Blood: Dark red
   Gasoline: Yellow/amber
   Milk: Off-white
   ```

2. **Consistent Color Logic**: Similar fluids should have similar colors
   ```
   All alcoholic beverages in amber/brown range
   All cleaning products in white/blue range
   All fuels in yellow/brown range
   ```

### Blending Best Practices

1. **Logical Compatibility**: Only allow realistic combinations
   ```
   Water + Alcohol = OK
   Gasoline + Water = Dangerous
   Bleach + Alcohol = Extremely dangerous
   ```

2. **Category-Based Rules**: Use categories for broad compatibility
   ```
   Beverages generally mix with other beverages
   Fuels mix with other fuels
   Chemicals should be restricted
   ```

### Poison System Guidelines

1. **Realistic Toxicity**: Match poison levels to real-world danger
   ```
   Household cleaners: Low to Medium
   Industrial chemicals: Medium to Extreme
   Pure toxins: Extreme to Deadly
   ```

2. **Appropriate Thresholds**: Set minAmount based on real toxicity
   ```
   Very toxic substances: 0.01-0.05
   Moderately toxic: 0.1-0.3
   Mildly toxic: 0.5-0.8
   ```

### Performance Considerations

1. **Efficient Color Values**: Use simple color values when possible
2. **Reasonable Property Ranges**: Avoid extreme values that could break gameplay
3. **Logical Category Assignment**: Don't over-categorize fluids

### Common Issues and Solutions

1. **Invalid Color Format**: Ensure RGB values are 0.0-1.0
   ```
   // Wrong
   Color = 255 : 128 : 64,
   
   // Correct
   Color = 1.0 : 0.5 : 0.25,
   ```

2. **Conflicting Blend Rules**: Ensure whitelist and blacklist don't contradict
3. **Missing Translation Keys**: Ensure DisplayName keys exist in translation files
4. **Unrealistic Properties**: Test that property values feel appropriate in-game

### Testing Your Fluids

1. **Visual Testing**: Check colors appear correctly in containers
2. **Mixing Testing**: Verify blending rules work as expected
3. **Effect Testing**: Confirm properties have appropriate gameplay impact
4. **Toxicity Testing**: Ensure poison effects trigger correctly
5. **Integration Testing**: Test with existing vanilla fluids

### Modding Integration

1. **Namespace**: Use consistent naming for your mod's fluids
2. **Compatibility**: Consider compatibility with other fluid mods
3. **Balance**: Ensure your fluids don't break game balance
4. **Documentation**: Document your fluid effects for players

---

This guide covers the comprehensive Build 42 fluid system in Project Zomboid. The fluid system allows for complex liquid interactions that enhance crafting, survival mechanics, and player creativity. Proper fluid scripting creates immersive and balanced liquid mechanics that integrate seamlessly with the game's survival systems while opening new possibilities for modding and gameplay experimentation.
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
# Project Zomboid Model Scripts Guide (Build 41)

*Compiled from Project Zomboid community documentation and modding resources*

**Note**: This guide covers Build 41 model system. Model scripts define 3D models and their properties for use in Project Zomboid.

---

## Table of Contents

1. [Introduction to Model Scripts](#introduction-to-model-scripts)
2. [Basic Model Structure](#basic-model-structure)
3. [Parameters Reference](#parameters-reference)
4. [Model Types](#model-types)
5. [Textures and Materials](#textures-and-materials)
6. [Animations and Attachments](#animations-and-attachments)
7. [Examples](#examples)
8. [Advanced Features](#advanced-features)
9. [Integration with Items](#integration-with-items)
10. [Tips and Best Practices](#tips-and-best-practices)

---

## Introduction to Model Scripts

Model scripts in Project Zomboid Build 41 define 3D models that can be used by items, characters, and world objects. They specify mesh files, textures, scaling, and other visual properties that determine how objects appear in the game world.

### Key Concepts:
- **Mesh**: The 3D geometry of the model (.X or .fbx format in Build 41)
- **Texture**: The surface appearance applied to the mesh
- **Scale**: Size adjustment for the model in-game
- **Attachments**: How models connect to characters or other objects
- **Shaders**: Rendering properties and effects

### Important Notes:
- Build 41 supports .X and .fbx model formats
- Model scripts use `property = value` syntax (similar to item scripts)
- Models must be referenced in item scripts to be used
- Texture files should be in .png format

---

## Basic Model Structure

### Standard Syntax
```
module ModuleName {
    model ModelName {
        MeshName = meshfile,
        TextureName = texturefile,
        Scale = 1.0,
        Shader = shadertype,
    }
}
```

### Essential Elements:
1. **Module Declaration**: Groups related models together
2. **Model Block**: Defines a single 3D model
3. **MeshName**: Path to the 3D mesh file
4. **TextureName**: Path to the texture image
5. **Scale**: Size multiplier for the model

---

## Parameters Reference

### Core Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **MeshName** | String | Path to mesh file | `MeshName = models_X/MyModel` |
| **TextureName** | String | Path to texture file | `TextureName = textures/MyTexture` |
| **Scale** | Float | Size multiplier | `Scale = 1.5` |
| **Shader** | String | Rendering shader type | `Shader = basicEffect` |

### Advanced Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **LoadTexture** | String | Alternative texture loading | `LoadTexture = MyTexture.png` |
| **Attachment** | String | Attachment point definition | `Attachment = Bip01_R_Hand` |
| **BoneName** | String | Bone for attachment | `BoneName = Bip01_Spine2` |
| **Offset** | Vector3 | Position offset | `Offset = 0.1 0.0 -0.05` |
| **Rotate** | Vector3 | Rotation values | `Rotate = 0.0 90.0 0.0` |

### Visual Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **Alpha** | Float | Transparency level | `Alpha = 0.8` |
| **Ambient** | Float | Ambient lighting | `Ambient = 0.5` |
| **Diffuse** | Float | Diffuse lighting | `Diffuse = 1.0` |
| **Specular** | Float | Specular lighting | `Specular = 0.3` |

---

## Model Types

### Static Models
Used for non-animated objects like weapons, tools, and world items:
```
model SimpleWeapon {
    MeshName = models_X/weapons/Knife,
    TextureName = textures/weapons/KnifeTexture,
    Scale = 1.0,
    Shader = basicEffect,
}
```

### Character Attachments
Models that attach to character bones:
```
model BackpackModel {
    MeshName = models_X/clothing/Backpack,
    TextureName = textures/clothing/BackpackTexture,
    Scale = 1.0,
    Attachment = Bip01_Spine2,
    Offset = 0.0 0.1 -0.15,
    Rotate = 0.0 0.0 0.0,
}
```

### World Static Models
For objects placed in the game world:
```
model ChairModel {
    MeshName = models_X/furniture/Chair,
    TextureName = textures/furniture/ChairTexture,
    Scale = 1.0,
    Shader = basicEffect,
}
```

---

## Textures and Materials

### Texture Specification
```
model TexturedItem {
    MeshName = models_X/items/MyItem,
    TextureName = textures/items/MyItemTexture,
    LoadTexture = MyItemTexture.png,    // Alternative method
    Scale = 1.0,
}
```

### Material Properties
```
model ReflectiveItem {
    MeshName = models_X/items/MetalItem,
    TextureName = textures/items/MetalTexture,
    Scale = 1.0,
    Shader = basicEffect,
    Ambient = 0.4,
    Diffuse = 1.0,
    Specular = 0.8,
}
```

### Transparency
```
model GlassItem {
    MeshName = models_X/items/GlassBottle,
    TextureName = textures/items/GlassTexture,
    Scale = 1.0,
    Alpha = 0.7,               // Semi-transparent
    Shader = basicEffect,
}
```

---

## Animations and Attachments

### Weapon Attachments
```
model RifleModel {
    MeshName = models_X/weapons/Rifle,
    TextureName = textures/weapons/RifleTexture,
    Scale = 1.0,
    Attachment = Bip01_R_Hand,
    Offset = 0.05 0.0 0.0,
    Rotate = 0.0 0.0 -15.0,
}
```

### Clothing Attachments
```
model HelmetModel {
    MeshName = models_X/clothing/Helmet,
    TextureName = textures/clothing/HelmetTexture,
    Scale = 1.0,
    Attachment = Bip01_Head,
    Offset = 0.0 0.0 0.0,
    BoneName = Bip01_Head,
}
```

### Multiple Attachment Points
```
model DualWieldWeapon {
    MeshName = models_X/weapons/Pistol,
    TextureName = textures/weapons/PistolTexture,
    Scale = 1.0,
    Attachment = Bip01_R_Hand,
    Offset = 0.02 0.0 0.0,
    
    // Alternative attachment for left hand
    // (requires additional Lua code)
}
```

---

## Examples

### Basic Weapon Model
```
module Base {
    model CrowbarModel {
        MeshName = models_X/weapons/Crowbar,
        TextureName = textures/weapons/CrowbarTexture,
        Scale = 1.0,
        Shader = basicEffect,
    }
}
```

### Scaled Tool Model
```
module MyMod {
    model OversizedHammer {
        MeshName = models_X/tools/Hammer,
        TextureName = textures/tools/HammerTexture,
        Scale = 2.0,              // Double size
        Shader = basicEffect,
        Attachment = Bip01_R_Hand,
        Offset = 0.0 0.0 -0.1,
    }
}
```

### Complex Clothing Model
```
module Clothing {
    model TacticalVest {
        MeshName = models_X/clothing/TacticalVest,
        TextureName = textures/clothing/TacticalVestTexture,
        Scale = 1.0,
        Shader = basicEffect,
        Attachment = Bip01_Spine1,
        Offset = 0.0 0.0 0.05,
        Rotate = 0.0 0.0 0.0,
        Ambient = 0.5,
        Diffuse = 1.0,
        Specular = 0.2,
    }
}
```

### Transparent Object Model
```
module Glass {
    model WindowPane {
        MeshName = models_X/building/WindowPane,
        TextureName = textures/building/GlassTexture,
        Scale = 1.0,
        Shader = basicEffect,
        Alpha = 0.3,              // Mostly transparent
        Ambient = 0.8,
        Diffuse = 0.6,
        Specular = 1.0,           // Highly reflective
    }
}
```

### Food Item Model
```
module Food {
    model AppleModel {
        MeshName = models_X/food/Apple,
        TextureName = textures/food/AppleTexture,
        Scale = 0.8,
        Shader = basicEffect,
        Ambient = 0.6,
        Diffuse = 1.0,
    }
}
```

---

## Advanced Features

### Shader Types
Different rendering effects for models:
```
// Common shader types:
Shader = basicEffect,         // Standard rendering
Shader = character,           // Character-specific shading
Shader = vehicle,             // Vehicle rendering
Shader = terrain,             // Terrain-specific
```

### Lighting Properties
```
model LitItem {
    MeshName = models_X/items/Lantern,
    TextureName = textures/items/LanternTexture,
    Scale = 1.0,
    Shader = basicEffect,
    Ambient = 0.3,            // How much ambient light affects it
    Diffuse = 1.2,            // Response to direct light
    Specular = 0.9,           // Shininess/reflection
}
```

### Conditional Loading
```
model ConditionalModel {
    MeshName = models_X/items/SpecialItem,
    TextureName = textures/items/SpecialTexture,
    Scale = 1.0,
    // Additional properties can be set via Lua
}
```

---

## Integration with Items

### Linking Models to Items
In item scripts, reference models using specific properties:

```
// In item script:
item MyWeapon {
    Type = Weapon,
    DisplayName = My Custom Weapon,
    Icon = MyWeaponIcon,
    WeaponSprite = MyWeaponModel,     // References model name
    WorldStaticModel = MyWeaponModel, // Model when dropped
    AttachmentType = Shovel,
}
```

### Static World Models
```
item Food {
    Type = Food,
    DisplayName = Custom Food,
    Icon = FoodIcon,
    StaticModel = FoodModel,          // Model in inventory/world
    WorldStaticModel = FoodModel,     // Model when on ground
}
```

### Character Equipment Models
```
item Clothing {
    Type = Clothing,
    DisplayName = Custom Shirt,
    Icon = ShirtIcon,
    BodyLocation = Torso,
    AttachmentType = Torso,
    // Model applied automatically based on AttachmentType
}
```

---

## Tips and Best Practices

### Model Creation Guidelines

1. **File Organization**: Keep models in logical folder structures
   ```
   models_X/
   ├── weapons/
   ├── clothing/
   ├── tools/
   ├── food/
   └── furniture/
   ```

2. **Naming Conventions**: Use descriptive, consistent names
   ```
   model KitchenKnifeModel     // Clear and specific
   model Knife01Model          // Avoid generic numbers
   ```

3. **Scale Considerations**: Test scale values in-game
   ```
   Scale = 1.0,    // Normal size
   Scale = 0.5,    // Half size
   Scale = 2.0,    // Double size
   ```

### Performance Optimization

1. **Efficient Textures**: Use appropriate texture sizes
   - Icons: 64x64 or 128x128
   - World models: 256x256 or 512x512
   - Character models: 512x512 or 1024x1024

2. **Polygon Count**: Keep models reasonably low-poly
   - Weapons: 500-2000 triangles
   - Clothing: 1000-5000 triangles
   - Furniture: 200-1000 triangles

3. **Texture Compression**: Use compressed formats when possible

### Common Issues and Solutions

1. **Model Not Appearing**:
   - Check file paths are correct
   - Verify mesh file exists
   - Ensure proper module structure

2. **Incorrect Scaling**:
   - Test different scale values
   - Check if model was created at wrong size
   - Verify Scale parameter syntax

3. **Texture Problems**:
   - Confirm texture file format (.png recommended)
   - Check TextureName path
   - Verify texture dimensions are power of 2

4. **Attachment Issues**:
   - Use correct bone names (Bip01_R_Hand, etc.)
   - Adjust Offset and Rotate values
   - Test with different attachment points

### Testing Your Models

1. **In-Game Preview**: Use debug mode to see models
2. **Attachment Testing**: Equip items to test positioning
3. **Animation Testing**: Check how models move with character
4. **Lighting Testing**: Verify models look good in different lighting
5. **Performance Testing**: Monitor FPS with multiple models loaded

### Debugging Models

1. **Console Output**: Check for error messages
2. **Missing Files**: Verify all referenced files exist
3. **Syntax Errors**: Double-check script syntax
4. **Path Issues**: Ensure file paths are correct
5. **Case Sensitivity**: File names are case-sensitive on some systems

### Model Formats

**Supported Formats (Build 41)**:
- `.X` - DirectX mesh format
- `.fbx` - Autodesk FBX format

**Conversion Tips**:
- Export from Blender using appropriate exporters
- Maintain proper UV mapping
- Include vertex normals for lighting
- Keep bone hierarchy simple for attachments

---

This guide covers the comprehensive Build 41 model system in Project Zomboid. Model scripts provide the visual representation for items and objects in the game world. Proper model creation and scripting are essential for creating immersive and well-integrated mods that enhance the player experience while maintaining good performance.
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
# Project Zomboid Sound Scripts Guide

*Compiled from Project Zomboid Wiki and community documentation*

---

## Table of Contents

1. [Introduction to Sound Scripts](#introduction-to-sound-scripts)
2. [Basic Sound Structure](#basic-sound-structure)
3. [Parameters Reference](#parameters-reference)
4. [Clip Parameters](#clip-parameters)
5. [Sound Categories](#sound-categories)
6. [Audio File Formats](#audio-file-formats)
7. [Examples](#examples)
8. [Multiplayer Considerations](#multiplayer-considerations)
9. [Tips and Best Practices](#tips-and-best-practices)

---

## Introduction to Sound Scripts

Sound scripts in Project Zomboid define audio parameters for sounds that can be used throughout the game. Since Build 40, all sounds must be defined in sound blocks to be heard by players beyond 20 tiles in multiplayer. Sound scripts also integrate sounds into the game's advanced audio options menu.

### Key Concepts:
- **Sound Blocks**: Define audio properties and behavior
- **Categories**: Organize sounds for audio options menu
- **3D Audio**: Positional audio with distance falloff
- **Clip Parameters**: Individual audio file properties
- **Multiplayer Range**: Distance other players can hear sounds

### Why Sound Scripts Are Important:
- **Multiplayer Compatibility**: Proper range and 3D positioning
- **Audio Options Integration**: Sounds appear in settings menu
- **Performance**: Optimized audio loading and playback
- **Customization**: Players can adjust sound categories independently

---

## Basic Sound Structure

### Standard Syntax
```
sound SoundName {
    category = CategoryName,
    loop = true/false,
    is3D = true/false,
    clip {
        file = path/to/audiofile.ogg,
        distanceMax = number,
        volume = 0.0-1.0,
        // Additional clip parameters...
    }
}
```

### Essential Elements:
- **Sound Name**: Unique identifier for the sound
- **Category**: Audio category for options menu
- **Clip Block**: Contains audio file and properties
- **File Path**: Relative path to audio file from mod root

### Simple Example:
```
sound MyCustomSound {
    category = MyMod,
    is3D = true,
    clip {
        file = media/sound/MySound.ogg,
        distanceMax = 100,
        volume = 0.8,
    }
}
```

---

## Parameters Reference

### Core Sound Parameters

| Parameter | Type | Description | Default | Example |
|-----------|------|-------------|---------|---------|
| **category** | String | Audio category for options menu | `""` | `category = Weapons` |
| **loop** | Boolean | Whether sound loops continuously | `false` | `loop = true` |
| **is3D** | Boolean | Enable 3D positional audio | `false` | `is3D = true` |
| **master** | String | Master volume category | `""` | `master = SFX` |

### Audio Behavior
| Parameter | Type | Description | Default | Example |
|-----------|------|-------------|---------|---------|
| **fadeInTime** | Float | Fade in duration (seconds) | `0.0` | `fadeInTime = 2.0` |
| **fadeOutTime** | Float | Fade out duration (seconds) | `0.0` | `fadeOutTime = 1.5` |

---

## Clip Parameters

The `clip` block contains parameters for individual audio files:

### File and Basic Properties
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **file** | String | Path to audio file | `file = media/sound/gunshot.ogg` |
| **event** | String | FMOD event for vanilla sounds | `event = Weapons/Firearm/shotgun2` |
| **volume** | Float | Volume level (0.0-1.0) | `volume = 0.7` |
| **pitch** | Float | Pitch modification | `pitch = 1.2` |

### 3D Audio Properties
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **distanceMax** | Integer | Maximum hearing distance | `distanceMax = 200` |
| **reverbFactor** | Float | Reverb amount (0.0-1.0) | `reverbFactor = 0.1` |

### Advanced Properties
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **pitchVar** | Float | Random pitch variation | `pitchVar = 0.1` |
| **volumeVar** | Float | Random volume variation | `volumeVar = 0.05` |

---

## Sound Categories

### Common Categories
Sound categories organize audio for the options menu:

| Category | Description | Use Cases |
|----------|-------------|-----------|
| **Item** | Item-related sounds | Weapon sounds, tool usage |
| **Ambient** | Environmental audio | Wind, rain, ambient loops |
| **Music** | Musical content | Background music, radio |
| **Voice** | Character voices | Player voices, NPC speech |
| **Vehicle** | Vehicle sounds | Engines, horns, crashes |
| **Zombie** | Zombie audio | Groans, footsteps, attacks |
| **UI** | Interface sounds | Menu clicks, notifications |
| **World** | World interaction | Door opening, breaking objects |

### Custom Categories
You can create custom categories for your mod:
```
sound MyModSound {
    category = MyMod: Weapons,  // Creates subcategory
    // ...
}
```

### Category Hierarchy
Use colons to create subcategories:
```
category = MyMod: Combat: Explosions,
```

---

## Audio File Formats

### Supported Formats
- **OGG Vorbis** (.ogg) - Recommended format
- **WAV** (.wav) - Uncompressed, larger files
- **MP3** (.mp3) - Compressed, not recommended

### File Placement
Audio files should be placed in your mod's media/sound directory:
```
MyMod/
├── media/
│   └── sound/
│       ├── weapons/
│       │   └── gunshot.ogg
│       ├── ambient/
│       │   └── wind.ogg
│       └── music/
│           └── theme.ogg
└── media/
    └── scripts/
        └── sounds.txt
```

### Audio Specifications
- **Sample Rate**: 44.1kHz recommended
- **Bit Depth**: 16-bit minimum, 24-bit preferred
- **Channels**: Mono or stereo
- **Compression**: Use OGG Vorbis quality 5-7

---

## Examples

### Basic Weapon Sound
```
sound CustomGunshot {
    category = Item,
    is3D = true,
    clip {
        file = media/sound/weapons/customgun.ogg,
        distanceMax = 200,
        volume = 0.8,
        reverbFactor = 0.2,
    }
}
```

### Ambient Loop
```
sound ForestAmbient {
    category = Ambient,
    loop = true,
    is3D = true,
    clip {
        file = media/sound/ambient/forest_loop.ogg,
        distanceMax = 50,
        volume = 0.3,
        reverbFactor = 0.5,
    }
}
```

### Vehicle Engine
```
sound CarEngine {
    category = Vehicle,
    loop = true,
    is3D = true,
    clip {
        file = media/sound/vehicles/engine_idle.ogg,
        distanceMax = 150,
        volume = 0.6,
        pitch = 1.0,
        pitchVar = 0.1,
    }
}
```

### Interface Sound
```
sound MenuClick {
    category = UI,
    is3D = false,
    clip {
        file = media/sound/ui/click.ogg,
        volume = 0.5,
    }
}
```

### Music Track
```
sound CustomRadioSong {
    category = Music,
    loop = false,
    is3D = false,
    clip {
        file = media/sound/music/radio_song.ogg,
        volume = 0.4,
        fadeInTime = 2.0,
        fadeOutTime = 3.0,
    }
}
```

### Zombie Sound with Variation
```
sound ZombieGrowl {
    category = Zombie,
    is3D = true,
    clip {
        file = media/sound/zombie/growl1.ogg,
        distanceMax = 80,
        volume = 0.7,
        pitchVar = 0.2,
        volumeVar = 0.1,
        reverbFactor = 0.3,
    }
}
```

### Environmental Effect
```
sound ThunderClap {
    category = Ambient,
    is3D = false,
    clip {
        file = media/sound/weather/thunder.ogg,
        distanceMax = 1000,
        volume = 0.9,
        reverbFactor = 0.8,
    }
}
```

### Tool Usage Sound
```
sound HammerHit {
    category = Item,
    is3D = true,
    clip {
        file = media/sound/tools/hammer_hit.ogg,
        distanceMax = 120,
        volume = 0.6,
        pitchVar = 0.15,
        reverbFactor = 0.1,
    }
}
```

---

## Multiplayer Considerations

### Distance and Range
- **distanceMax**: How far other players can hear the sound
- **Zombie Aggro**: Separate from distanceMax, handled by item properties
- **Performance**: Larger distances impact network performance

### Example Ranges by Sound Type:
```
Gunshots:     distanceMax = 200-400
Melee Combat: distanceMax = 50-100
Tools:        distanceMax = 80-150
Ambient:      distanceMax = 30-80
Explosions:   distanceMax = 500-800
Whispers:     distanceMax = 10-20
Shouts:       distanceMax = 100-200
```

### Network Optimization
```
sound OptimizedSound {
    category = Item,
    is3D = true,
    clip {
        file = media/sound/optimized.ogg,
        distanceMax = 100,        // Reasonable range
        volume = 0.7,
        reverbFactor = 0.1,       // Light reverb for performance
    }
}
```

---

## Tips and Best Practices

### Audio Production Guidelines

1. **File Format**: Use OGG Vorbis for best compression and compatibility
2. **Sample Rate**: 44.1kHz is standard, higher rates waste space
3. **Bit Depth**: 16-bit minimum, 24-bit for high-quality sounds
4. **Normalization**: Normalize audio to prevent clipping
5. **Noise Reduction**: Clean audio files of background noise

### Sound Design Principles

1. **Realistic Distances**: Match distanceMax to logical hearing range
2. **Volume Balance**: Ensure sounds don't overpower each other
3. **Variation**: Use pitchVar and volumeVar for natural variety
4. **Context Appropriate**: Match reverb and tone to environment
5. **Player Feedback**: Provide clear audio feedback for actions

### Performance Optimization

1. **File Size**: Keep audio files reasonably sized
2. **Loop Points**: Ensure loops are seamless for ambient sounds
3. **Distance Limits**: Don't set excessive distanceMax values
4. **Category Organization**: Use meaningful categories for player control

### Integration with Items and Recipes

Sounds defined in sound scripts can be used in:
- **Item Scripts**: `SwingSound`, `HitSound`, `BreakSound`
- **Recipe Scripts**: `Sound` parameter
- **Lua Code**: `getSoundManager():PlaySound()`

### Example Item Integration:
```
// In sound script:
sound CustomAxeSwing {
    category = Item,
    is3D = true,
    clip {
        file = media/sound/weapons/axe_swing.ogg,
        distanceMax = 100,
        volume = 0.6,
    }
}

// In item script:
item CustomAxe {
    Type = Weapon,
    SwingSound = CustomAxeSwing,
    // Other parameters...
}
```

### Troubleshooting Common Issues

1. **Sound Not Playing**: Check file path and format
2. **No Multiplayer Range**: Verify distanceMax is set
3. **Missing from Options**: Ensure category is specified
4. **Performance Issues**: Reduce file sizes and distances
5. **Audio Clipping**: Lower volume levels and normalize audio

### Category Best Practices

1. **Consistency**: Use established categories when possible
2. **Hierarchy**: Create logical subcategories with colons
3. **Player Control**: Allow players to control sound volumes
4. **Mod Identification**: Include mod name in custom categories

### Testing Your Sounds

1. **Single Player**: Test basic playback and volume
2. **Multiplayer**: Test range and 3D positioning
3. **Audio Options**: Check sounds appear in settings menu
4. **Performance**: Test with multiple sounds playing
5. **Variation**: Test pitch and volume variation ranges

---

This guide covers the complete sound script system in Project Zomboid. Sound scripts are essential for proper audio integration, especially in multiplayer environments, and provide players with granular control over their audio experience through the options menu.
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