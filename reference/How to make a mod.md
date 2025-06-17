Of course. Here is a comprehensive guide for creating a basic Project Zomboid mod, based on the provided video. This document is structured for clarity and easy reference, making it perfect for a knowledge base or a Gemini gem.

***

## Project Zomboid (B42) Modding Guide: Creating Your First Mod

This guide walks through the fundamental steps of creating a basic Project Zomboid mod, from setting up the required file structure to creating and implementing a new custom item.

### Part 1: Initial Folder and File Structure

The foundation of any mod is its folder structure. Project Zomboid requires a specific hierarchy for the game to recognize and load your mod correctly.

**1. Navigate to the Workshop Folder:**
The primary working directory for your mod is located in your user's Zomboid folder.

`C:\Users\YourUserName\Zomboid\Workshop`

**2. Create the Main Mod Folder:**
Inside the `Workshop` folder, create a new folder for your mod.
*   **Example Name:** `My First Mod`

**3. Create the Core Directory Structure:**
Inside your main mod folder (`My First Mod`), create the following nested folders. The naming must be exact.

```
My First Mod
└───Contents
    └───mods
        └───My First Mod
            ├───42
            │   └───media
            └───common
```

*   In `My First Mod`, create a folder named `Contents`.
*   In `Contents`, create a folder named `mods`.
*   In `mods`, create another folder with the *exact same name as your mod*. In this case, `My First Mod`.
*   In this second `My First Mod` folder, create two new folders: `42` and `common`.
*   Finally, inside the `42` folder, create a folder named `media`.

### Part 2: The `mod.info` File

The `mod.info` file tells Project Zomboid what your mod is, what it's called, and how to load it. You will need **two identical copies** of this file.

**1. Get a Template (Important!):**
You cannot simply create a new text file and rename it to `mod.info`. You must use a valid `.INFO` file as a template.

*   Navigate to your user's Zomboid `mods` folder: `C:\Users\YourUserName\Zomboid\mods`
*   Open the `examplemod` folder.
*   Copy the `mod.info` file from this folder.

**2. Place the `mod.info` Files:**
Paste the copied `mod.info` file into the following two locations within your mod's structure:

*   **Location 1:** `...\Workshop\My First Mod\Contents\mods\My First Mod`
*   **Location 2:** `...\Workshop\My First Mod\Contents\mods\My First Mod\42`

**3. Edit the `mod.info` Content:**
Open the `mod.info` file in a text editor and modify its contents. Both files must be **100% identical**.

Here is a template based on the video:

```
name=My First Mod
id=MyFirstMod
description=This is where you can describe what your mod does.
poster=
icon=
```

*   `name`: The display name of your mod in the game's mod list.
*   `id`: A unique identifier for your mod. It should not contain spaces.
*   `description`: The text that appears when you select the mod in-game.
*   `poster`: The filename of a **256x256 png** image for your mod's workshop page/mod list. It can be left blank for now.
*   `icon`: The filename of a **32x32 png** image that appears next to your mod's name. It can also be left blank.

### Part 3: Creating a Custom Item (Example: Super Katana)

This section covers the creation of a simple new weapon.

**1. Create the Scripts Folder:**
All item, recipe, and script files go into a `scripts` folder inside your mod's `media` folder.

*   Navigate to: `...\42\media`
*   Create a new folder named `scripts`.

**2. Create the Item Script File:**
Inside the `scripts` folder, create a new text document (`.txt`). This file will contain the code for your new item.

*   **Example Name:** `Super Katana.txt`

**3. Find a Vanilla Template:**
The easiest way to create a new item is to copy an existing one from the base game and modify it.

*   Navigate to the Project Zomboid installation directory: `Steam\steamapps\common\ProjectZomboid`
*   Go to the game's script files: `\media\scripts\items`
*   For a Katana, the file is `items_weapons_long_blade.txt`.
*   Open this file and find the code block for `item Katana`.

**4. Write the Item Script:**
Copy the entire `item Katana { ... }` block from the vanilla file and paste it into your `Super Katana.txt` file.

**Crucial Formatting:**
Your script file **must** be structured correctly. It needs a `module Base` wrapper around your item definition. Missing the module name or the curly braces (`{ }`) will break the mod.

```lua
module Base
{
    item SuperKatana
    {
        DisplayName = Super Katana,
        DisplayCategory = Weapon,
        Type = Weapon,
        Weight = 0.01,
        Icon = Katana,
        AttachmentType = Sword,
        BaseSpeed = 1,
        BreakSound = Katanabreak,
        Categories = LongBlade,
        ConditionLowerChanceOneIn = 150,
        ConditionMax = 70,
        CritDmgMultiplier = 8,
        CriticalChance = 80,
        DamageCategory = Slash,
        DamageMakeHole = TRUE,
        DoorDamage = 20,
        HitSound = Katanahit,
        ImpactSound = Katanahit,
        KnockBackOnNoDeath = TRUE,
        KnockdownMod = 8,
        MaxDamage = 8,
        MaxHitCount = 8,
        MinAngle = 0.0,
        MinDamage = 8,
        RunAnim = Run_Weapon2,
        SwingSound = KatanaSwing,
        SwingTime = 1,
        TreeDamage = 1,
        WeaponSprite = Katana,
    }
}
```

**5. Modify the Item:**

*   **Rename the Item:** Change `item Katana` to `item SuperKatana`. This is critical to ensure you are creating a *new* item and not overwriting the vanilla one.
*   **Change the Display Name:** Change `DisplayName = Katana,` to `DisplayName = Super Katana,`.
*   **Adjust Stats:** Modify the values to make the weapon unique. In the video, these stats were changed to make it overpowered:
    *   `Weight = 0.01,`
    *   `ConditionLowerChanceOneIn = 150,`
    *   `ConditionMax = 70,`
    *   `CritDmgMultiplier = 8,`
    *   `CriticalChance = 80,`
    *   `DoorDamage = 20,`
    *   `KnockdownMod = 8,`
    *   `MaxDamage = 8,`
    *   `MinDamage = 8,`
    *   `MaxHitCount = 8,`
    *   `TreeDamage = 1,`
    *   `SwingTime = 1,`

### Part 4: Testing the Mod

1.  Launch Project Zomboid.
2.  From the main menu, select **MODS**. Find "My First Mod" and click **ENABLE**.
3.  Go back and start a **NEW GAME**. Make sure you start in **DEBUG MODE**.
4.  Once in-game, click the mosquito icon on the left to open the **DEBUG MENU**.
5.  Select **Items List**. In the filter box, type the name of your item (`super`) to find it.
6.  Double-click the item to add it to your inventory.
7.  Equip the item and test it out