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