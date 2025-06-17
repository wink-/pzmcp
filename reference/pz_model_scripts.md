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