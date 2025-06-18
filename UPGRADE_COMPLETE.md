# 🚀 Upgrade to Full MCP Server

## Step 1: Dependencies Installed ✅

You've successfully installed the full MCP dependencies!

## Step 2: Update Claude Desktop Configuration

**Replace your Claude Desktop config** (`%APPDATA%\Claude\claude_desktop_config.json`) with:

```json
{
  "mcpServers": {
    "project-zomboid": {
      "command": "C:\\Users\\winkk\\AppData\\Local\\Programs\\Python\\Python313\\python.exe",
      "args": ["C:\\Users\\winkk\\code\\pzmcp\\run_server.py"],
      "cwd": "C:\\Users\\winkk\\code\\pzmcp"
    }
  }
}
```

**Key Change:** Using `run_server.py` instead of `run_server_v2.py`

## Step 3: Restart Claude Desktop

Close and restart Claude Desktop completely.

## Step 4: Test the Full Server

Ask Claude: *"What MCP tools are available for Project Zomboid?"*

You should now see **5 advanced tools**:

### 🔧 Full Tool Suite:
1. **`validate_script`** - Advanced script validation with syntax checking
2. **`generate_script`** - Generate scripts from templates
3. **`search_vanilla`** - Search vanilla Project Zomboid game data
4. **`check_references`** - Validate item/sound/sprite references
5. **`analyze_mod`** - Comprehensive mod directory analysis

### 📚 Enhanced Resources:
1. **`vanilla_database`** - Full vanilla game data
2. **`property_reference`** - Complete property documentation
3. **`modding_templates`** - Professional templates
4. **`best_practices`** - Advanced modding guidelines

## What You Get Now

### Advanced Capabilities:
- ✅ **Script Generation** - Create items, recipes, vehicles from templates
- ✅ **Vanilla Search** - Find any vanilla item, recipe, or vehicle
- ✅ **Reference Validation** - Check if sprites, sounds, items exist
- ✅ **Mod Analysis** - Analyze entire mod projects
- ✅ **Database Access** - Query 35 script files worth of vanilla data

### Example Advanced Queries:
- *"Generate a custom sword script for Project Zomboid"*
- *"Search for all vanilla melee weapons"*
- *"Analyze my mod directory for errors"*
- *"Check if these item references are valid: Base.Hammer, Base.Apple"*

## Verification

After restart, the server should initialize the database and you'll have access to the full feature set. You've now upgraded from the basic 2-tool fallback to the complete 5-tool professional MCP server!

🎉 **Welcome to the full Project Zomboid MCP experience!**