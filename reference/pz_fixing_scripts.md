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