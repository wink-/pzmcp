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