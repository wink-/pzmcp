# Claude Desktop Integration Guide

## Setup Instructions

### Option 1: Using Poetry (Linux/WSL)
If you're in WSL/Linux and have Poetry working:

```json
{
  "mcpServers": {
    "project-zomboid": {
      "command": "poetry",
      "args": ["run", "python", "-m", "mcp_server.mcp_server"],
      "cwd": "/mnt/c/Users/winkk/code/pzmcp"
    }
  }
}
```

### Option 2: Using Python directly (Windows/Recommended)
For Windows Claude Desktop, use this configuration with full paths:

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

**IMPORTANT**: Replace the Python path with your actual Python installation path. Common locations:
- `C:\\Users\\[username]\\AppData\\Local\\Programs\\Python\\Python313\\python.exe`
- `C:\\Python313\\python.exe`
- `C:\\Program Files\\Python313\\python.exe`

### Option 3: Using full Python path (if Python not in PATH)
If Python isn't in your PATH:

```json
{
  "mcpServers": {
    "project-zomboid": {
      "command": "C:\\Python311\\python.exe",
      "args": ["run_server.py"],
      "cwd": "C:\\Users\\winkk\\code\\pzmcp"
    }
  }
}
```

## Claude Desktop Configuration File Location

### Windows
Add the configuration to:
```
%APPDATA%\Claude\claude_desktop_config.json
```

### macOS
Add the configuration to:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Linux
Add the configuration to:
```
~/.config/claude/claude_desktop_config.json
```

## Installing Dependencies

### Method 1: Using Poetry (Recommended for development)
```bash
poetry install
poetry run python simple_test.py  # Test the server
```

### Method 2: Using pip directly
```bash
pip install mcp pydantic sqlalchemy rich
python run_server.py  # Test the server
```

### Method 3: Using the installer script
```bash
python install_dependencies.py
python run_server.py
```

## Testing the Integration

1. **Install dependencies** using one of the methods above
2. **Test the server locally:**
   ```bash
   python run_server.py
   ```
3. **Add the configuration** to Claude Desktop config file
4. **Restart Claude Desktop**
5. **Test in Claude Desktop** by asking: "What MCP tools are available?"

## Available MCP Tools

Once integrated, you can use these tools in Claude Desktop:

- **validate_script** - Validate Project Zomboid script syntax
- **generate_script** - Generate scripts from templates
- **search_vanilla** - Search vanilla game data
- **check_references** - Validate item/sound/sprite references
- **analyze_mod** - Analyze mod directory structure

## Available MCP Resources

- **vanilla_database** - Parsed vanilla game data
- **property_reference** - Valid properties per script type
- **modding_templates** - Pre-built templates
- **best_practices** - Modding guidelines

## Troubleshooting

### "python not found"
- Install Python 3.11+ and add to PATH
- Or use full path to python.exe in configuration

### "spawn poetry ENOENT"
- Use Option 2 or 3 above instead of Poetry
- Poetry may not be in Windows PATH

### Server disconnects immediately
- Check that all dependencies are installed
- Run `python run_server.py` manually to see error messages
- Check Claude Desktop logs for specific error details

### Dependencies not found
- Make sure you're using the same Python installation that has the packages
- Consider using a virtual environment
- Run the test script: `python simple_test.py`