# Windows Setup Guide for Claude Desktop Integration

## Quick Setup Steps

### 1. Install Dependencies
Run this from Windows Command Prompt:
```cmd
cd C:\Users\winkk\code\pzmcp
install_for_windows.bat
```

Or manually:
```cmd
C:\Users\winkk\AppData\Local\Programs\Python\Python313\python.exe -m pip install mcp pydantic sqlalchemy rich
```

### 2. Test the Server
```cmd
C:\Users\winkk\AppData\Local\Programs\Python\Python313\python.exe C:\Users\winkk\code\pzmcp\run_server.py
```

### 3. Configure Claude Desktop
Add this to `%APPDATA%\Claude\claude_desktop_config.json`:

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

### 4. Restart Claude Desktop

### 5. Test in Claude Desktop
Ask: "What MCP tools are available for Project Zomboid?"

## Troubleshooting

### Error: "can't open file"
- Check that `run_server.py` exists at `C:\Users\winkk\code\pzmcp\run_server.py`
- Verify the paths in the configuration match your actual file locations

### Error: "spawn python ENOENT"
- Use the full path to python.exe in the configuration
- Check your Python installation path

### Error: "No module named 'mcp'"
- Run the installation script: `install_for_windows.bat`
- Or install manually: `python -m pip install mcp pydantic sqlalchemy rich`

### Server disconnects immediately
- Test the server manually first
- Check Claude Desktop logs for specific error messages
- Make sure all dependencies are installed for the same Python installation

## File Locations

- **Config file**: `%APPDATA%\Claude\claude_desktop_config.json`
  - Full path: `C:\Users\winkk\AppData\Roaming\Claude\claude_desktop_config.json`
- **Server script**: `C:\Users\winkk\code\pzmcp\run_server.py`
- **Python**: `C:\Users\winkk\AppData\Local\Programs\Python\Python313\python.exe`

## Alternative Python Locations
If your Python is installed elsewhere, common paths include:
- `C:\Python313\python.exe`
- `C:\Program Files\Python313\python.exe`
- `C:\Users\[username]\AppData\Local\Microsoft\WindowsApps\python.exe`

Use `where python` in Command Prompt to find your Python installation.