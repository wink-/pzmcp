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
2. **Multiplayer**: Verify range and 3D positioning
3. **Audio Options**: Check sounds appear in settings menu
4. **Performance**: Test with multiple sounds playing
5. **Variation**: Test pitch and volume variation ranges

---

This guide covers the complete sound script system in Project Zomboid. Sound scripts are essential for proper audio integration, especially in multiplayer environments, and provide players with granular control over their audio experience through the options menu.