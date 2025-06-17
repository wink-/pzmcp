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