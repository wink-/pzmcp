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
    AddIngredientIfCooked:true,
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