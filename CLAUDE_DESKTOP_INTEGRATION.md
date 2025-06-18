# Claude Desktop Integration Guide

Complete guide for integrating the Project Zomboid MCP Server with Claude Desktop for intelligent mod development assistance.

## Table of Contents
- [Quick Start](#quick-start)
- [Configuration Examples](#configuration-examples)
- [Available MCP Tools](#available-mcp-tools)
- [Usage Examples](#usage-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites
- ✅ Claude Desktop installed
- ✅ Project Zomboid MCP Server set up (see [WINDOWS_SETUP.md](WINDOWS_SETUP.md))
- ✅ Project Zomboid game data extracted

### Basic Configuration

1. **Open Claude Desktop Settings**
   - Click the gear icon ⚙️
   - Go to "MCP Settings"
   - Click "Edit Config"

2. **Add MCP Server Configuration**

**For WSL (Recommended):**
```json
{
  "mcpServers": {
    "project-zomboid": {
      "command": "C:\\Windows\\System32\\wsl.exe",
      "args": [
        "-d", "Ubuntu",
        "--cd", "/home/username/pzmcp",
        "/home/username/.local/bin/uv", "run", "python", "run_server.py"
      ],
      "env": {
        "PATH": "/home/username/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
      }
    }
  }
}
```

**For Windows Python:**
```json
{
  "mcpServers": {
    "project-zomboid": {
      "command": "python",
      "args": ["run_server.py"],
      "cwd": "C:\\Users\\YourName\\path\\to\\pzmcp",
      "env": {
        "PYTHONPATH": "C:\\Users\\YourName\\path\\to\\pzmcp"
      }
    }
  }
}
```

3. **Save and Restart Claude Desktop**

4. **Test Connection**
   ```
   Use the Project Zomboid MCP to search for a crowbar
   ```

## Configuration Examples

### Advanced WSL Configuration

```json
{
  "mcpServers": {
    "project-zomboid": {
      "command": "C:\\Windows\\System32\\wsl.exe",
      "args": [
        "-d", "Ubuntu",
        "--cd", "/home/username/pzmcp",
        "/home/username/.local/bin/uv", "run", "python", "run_server.py"
      ],
      "env": {
        "PATH": "/home/username/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "PYTHONPATH": "/home/username/pzmcp",
        "PZ_CONFIG_PATH": "/home/username/pzmcp/pz_config.json"
      },
      "timeout": 30000
    }
  }
}
```

### Multiple Environment Configuration

```json
{
  "mcpServers": {
    "project-zomboid-dev": {
      "command": "C:\\Windows\\System32\\wsl.exe",
      "args": [
        "-d", "Ubuntu",
        "--cd", "/home/username/pzmcp-dev",
        "/home/username/.local/bin/uv", "run", "python", "run_server.py"
      ],
      "env": {
        "PATH": "/home/username/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "PZ_ENV": "development"
      }
    },
    "project-zomboid-stable": {
      "command": "C:\\Windows\\System32\\wsl.exe", 
      "args": [
        "-d", "Ubuntu",
        "--cd", "/home/username/pzmcp-stable",
        "/home/username/.local/bin/uv", "run", "python", "run_server.py"
      ],
      "env": {
        "PATH": "/home/username/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "PZ_ENV": "stable"
      }
    }
  }
}
```

### Debug Configuration

```json
{
  "mcpServers": {
    "project-zomboid": {
      "command": "C:\\Windows\\System32\\wsl.exe",
      "args": [
        "-d", "Ubuntu",
        "--cd", "/home/username/pzmcp", 
        "/home/username/.local/bin/uv", "run", "python", "run_server.py", "--debug"
      ],
      "env": {
        "PATH": "/home/username/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "LOG_LEVEL": "DEBUG",
        "PYTHONPATH": "/home/username/pzmcp"
      }
    }
  }
}
```

## Available MCP Tools

The Project Zomboid MCP Server provides these tools to Claude:

### 🔍 Search Tools
- **`search_vanilla`** - Search vanilla game items, recipes, vehicles
- **`search_items`** - Full-text search across all items
- **`search_recipes`** - Find recipes by ingredients or output

### ✅ Validation Tools  
- **`validate_script`** - Validate Project Zomboid script syntax
- **`check_references`** - Verify item/sound/sprite references exist

### 🛠️ Generation Tools
- **`generate_script`** - Generate new scripts from templates
- **`create_item`** - Create new item definitions
- **`create_recipe`** - Create new crafting recipes

### 📊 Analysis Tools
- **`analyze_mod`** - Analyze mod directory structure
- **`get_item_details`** - Get comprehensive item information
- **`find_dependencies`** - Find item dependencies and references

## Usage Examples

### Item Research and Discovery

**Find specific items:**
```
Use the Project Zomboid MCP to find me all baseball bats in the game
```

**Search by properties:**
```
Find all melee weapons with damage over 2.0 using the PZ MCP
```

**Find crafting materials:**
```
What items can I use to craft a spear? Use the Project Zomboid MCP to search
```

### Script Generation

**Create new items:**
```
Use the Project Zomboid MCP to generate a script for a tactical knife with:
- 1.8 damage
- High durability
- Can be attached to spears
- Requires metalworking to craft
```

**Create recipes:**
```
Generate a Project Zomboid recipe that lets me craft a reinforced backpack using:
- 1 school bag
- 2 leather strips  
- 1 needle and thread
- Tailoring skill level 4
```

**Create weapon modifications:**
```
Create a PZ script for a sawed-off shotgun variant that:
- Has shorter range but higher damage
- Can be crafted from a normal shotgun
- Requires a hacksaw
```

### Script Validation and Analysis

**Validate existing scripts:**
```
Use the Project Zomboid MCP to validate this script for errors:

[paste your script here]
```

**Check item references:**
```
Analyze this mod directory and check if all item references are valid using the PZ MCP:
/path/to/my/mod
```

**Find missing dependencies:**
```
Check what vanilla items this custom recipe depends on using the Project Zomboid MCP:

[paste recipe script]
```

### Mod Development Assistance

**Analyze mod structure:**
```
Use the PZ MCP to analyze my mod structure and suggest improvements:
/home/username/my_mod_folder
```

**Balance checking:**
```
Compare the stats of my custom weapon to similar vanilla weapons using the Project Zomboid MCP:

[paste item script]
```

**Recipe optimization:**
```
Suggest alternative ingredients for this recipe that would be more balanced using the PZ MCP:

[paste recipe script]
```

## Best Practices

### 1. **Effective Prompting**

**✅ Good prompts:**
- Be specific about what you want to find or create
- Mention "Project Zomboid MCP" or "PZ MCP" to ensure tool usage
- Provide context for script generation (damage, durability, etc.)

**❌ Avoid:**
- Vague requests without specifics
- Asking for things outside Project Zomboid scope
- Not mentioning the MCP when you want tool usage

### 2. **Script Development Workflow**

1. **Research** existing items first
   ```
   Find similar items to what I want to create using the PZ MCP
   ```

2. **Generate** initial script
   ```
   Create a PZ script based on [specifications]
   ```

3. **Validate** the generated script
   ```
   Validate this Project Zomboid script for syntax errors
   ```

4. **Analyze** for balance and dependencies
   ```
   Check if this item is balanced compared to vanilla items
   ```

### 3. **Search Strategies**

**Broad searches:**
```
Find all weapons in the "Axe" category using the Project Zomboid MCP
```

**Specific searches:**
```
Find the exact item ID for "Baseball Bat" using the PZ MCP
```

**Property-based searches:**
```
Find all items with "RepairWithTape" tag using the Project Zomboid MCP
```

### 4. **Data Organization**

- Use the MCP to understand vanilla item patterns before creating custom content
- Check existing recipes to understand crafting balance
- Validate all scripts before adding to your mod

## Troubleshooting

### Common Issues

#### "MCP server not responding"

**Solution:**
1. Check if the server is running:
   ```bash
   # In WSL/Ubuntu terminal
   cd pzmcp
   uv run python run_server.py
   ```

2. Verify Claude Desktop configuration syntax
3. Restart Claude Desktop completely
4. Check Windows Event Viewer for WSL errors

#### "No Project Zomboid tools available"

**Solution:**
1. Ensure MCP server name matches in config: `"project-zomboid"`
2. Check server logs for initialization errors
3. Verify database has data:
   ```bash
   uv run python -c "
   import sqlite3
   conn = sqlite3.connect('mcp_data.db')
   cursor = conn.cursor()
   cursor.execute('SELECT COUNT(*) FROM items_fts')
   print(f'Items: {cursor.fetchone()[0]}')
   "
   ```

#### "Database errors"

**Solution:**
1. Re-extract game data:
   ```bash
   rm mcp_data.db
   uv run python -c "
   from mcp_server.core.enhanced_data_extractor import extract_with_path_manager
   extract_with_path_manager(comprehensive=True)
   "
   ```

2. Check Project Zomboid installation path:
   ```bash
   uv run python pz_path_manager.py --find
   ```

#### "Script generation issues"

**Solution:**
1. Be more specific in your requests
2. Provide example items or existing scripts for reference
3. Ask for validation after generation
4. Check if the request is within Project Zomboid's modding capabilities

### Debug Mode

Enable debug logging by modifying your Claude Desktop config:

```json
{
  "mcpServers": {
    "project-zomboid": {
      "command": "C:\\Windows\\System32\\wsl.exe",
      "args": [
        "-d", "Ubuntu",
        "--cd", "/home/username/pzmcp",
        "/home/username/.local/bin/uv", "run", "python", "run_server.py", "--debug"
      ],
      "env": {
        "PATH": "/home/username/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

### Performance Optimization

**For better performance:**

1. **Store project in WSL filesystem** (not `/mnt/c/`)
2. **Allocate more memory to WSL** (`.wslconfig`)
3. **Use SSD storage** for better I/O
4. **Close unnecessary applications** during heavy script generation

## Advanced Usage

### Custom Templates

Create custom script templates in `/templates/` directory and reference them:

```
Generate a PZ script using my custom weapon template for a [weapon type]
```

### Batch Operations

```
Analyze all scripts in my mod directory and generate a compatibility report using the Project Zomboid MCP
```

### Integration with Other Tools

The MCP server can work alongside:
- **PZ Mod Manager** - For mod installation
- **Zomboid Visual Studio** - For map editing  
- **Git** - For version control of your mods

---

**Pro Tip:** Start each session by testing the MCP connection with a simple search to ensure everything is working properly!