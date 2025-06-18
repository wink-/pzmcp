# Quick Fix for Claude Desktop Integration

## The Problem
Your Windows Python installation is missing the MCP dependencies.

## The Solution

### Option 1: Install Dependencies (Recommended)

**Step 1:** Open Command Prompt as Administrator and run:
```cmd
cd C:\Users\winkk\code\pzmcp
C:\Users\winkk\AppData\Local\Programs\Python\Python313\python.exe install_windows_deps.py
```

**Step 2:** Update Claude Desktop config (`%APPDATA%\Claude\claude_desktop_config.json`):
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

### Option 2: Use Standalone Server (Works without dependencies)

**Step 1:** Update Claude Desktop config to use the standalone version:
```json
{
  "mcpServers": {
    "project-zomboid": {
      "command": "C:\\Users\\winkk\\AppData\\Local\\Programs\\Python\\Python313\\python.exe",
      "args": ["C:\\Users\\winkk\\code\\pzmcp\\run_server_standalone.py"],
      "cwd": "C:\\Users\\winkk\\code\\pzmcp"
    }
  }
}
```

**Step 2:** Restart Claude Desktop

The standalone server will:
- ✅ Work without MCP dependencies
- ✅ Show helpful error messages  
- ✅ Provide fallback functionality
- ✅ Guide you to install full dependencies

## Test Locally First

Before configuring Claude Desktop, test the server:

```cmd
# Test standalone version
C:\Users\winkk\AppData\Local\Programs\Python\Python313\python.exe C:\Users\winkk\code\pzmcp\run_server_standalone.py

# Or test with dependencies installed
C:\Users\winkk\AppData\Local\Programs\Python\Python313\python.exe C:\Users\winkk\code\pzmcp\run_server.py
```

## Files Created

- **`install_windows_deps.py`** - Installs MCP dependencies for Windows Python
- **`run_server_standalone.py`** - Fallback server that works without dependencies
- **`install_for_windows.bat`** - One-click installer and tester

## Next Steps

1. Try Option 2 (standalone) first - it should work immediately
2. If you want full functionality, install dependencies with Option 1
3. Test locally before updating Claude Desktop config
4. Restart Claude Desktop after config changes