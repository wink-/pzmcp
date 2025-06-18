# Windows Setup Guide for Project Zomboid MCP Server

This guide covers setting up the Project Zomboid MCP Server on Windows using WSL (Windows Subsystem for Linux) and integrating it with Claude Desktop.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Step 1: Install WSL](#step-1-install-wsl)
- [Step 2: Install Dependencies](#step-2-install-dependencies)
- [Step 3: Clone and Setup Project](#step-3-clone-and-setup-project)
- [Step 4: Configure Project Zomboid Paths](#step-4-configure-project-zomboid-paths)
- [Step 5: Extract Game Data](#step-5-extract-game-data)
- [Step 6: Configure Claude Desktop](#step-6-configure-claude-desktop)
- [Step 7: Test the Integration](#step-7-test-the-integration)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- **Windows 10/11** with admin privileges
- **Project Zomboid** installed (Steam, Epic, or GOG)
- **Claude Desktop** application installed

## Step 1: Install WSL

### Option A: Quick Install (Windows 11 or Windows 10 version 2004+)

1. **Open PowerShell as Administrator**
   ```powershell
   wsl --install
   ```

2. **Restart your computer** when prompted

3. **Set up Ubuntu user account** on first launch

### Option B: Manual Install (Older Windows versions)

1. **Enable WSL feature**
   ```powershell
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```

2. **Download and install WSL2 Linux kernel update**
   - Visit: https://aka.ms/wsl2kernel
   - Install the downloaded package

3. **Set WSL2 as default**
   ```powershell
   wsl --set-default-version 2
   ```

4. **Install Ubuntu from Microsoft Store**
   - Search for "Ubuntu" in Microsoft Store
   - Install Ubuntu 22.04 LTS (recommended)

## Step 2: Install Dependencies

Open **Ubuntu terminal** (search "Ubuntu" in Start menu):

### Install Python and uv

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python 3.11+
sudo apt install python3.11 python3.11-venv python3-pip curl git -y

# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify installation
uv --version
```

## Step 3: Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/your-username/pzmcp.git
cd pzmcp

# Install dependencies with uv
uv sync

# Verify installation
uv run python -c "print('✓ Setup successful!')"
```

## Step 4: Configure Project Zomboid Paths

The MCP server automatically detects Project Zomboid installations. Let's verify your setup:

```bash
# Check available paths
uv run python pz_path_manager.py --list
```

**Expected output:**
```
✓ [ 1] steam_common_x86
    Path: C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid\media\scripts
    WSL:  /mnt/c/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media/scripts ✓
    Desc: Steam installation (Program Files x86)
```

### If Project Zomboid isn't detected:

1. **Find your PZ installation:**
   - **Steam**: Right-click Project Zomboid → Properties → Installed Files → Browse
   - **Epic**: Usually `C:\Program Files\Epic Games\ProjectZomboid`
   - **GOG**: Usually `C:\GOG Games\Project Zomboid`

2. **Add custom path:**
   ```bash
   uv run python pz_path_manager.py --add "my_pz" "C:\Your\ProjectZomboid\Path\media\scripts" 1
   ```

3. **Verify detection:**
   ```bash
   uv run python pz_path_manager.py --find
   ```

## Step 5: Extract Game Data

Extract Project Zomboid script data into the MCP database:

```bash
# Extract data using enhanced extractor
uv run python -c "
from mcp_server.core.enhanced_data_extractor import extract_with_path_manager
print('Starting comprehensive data extraction...')
extract_with_path_manager(comprehensive=True)
print('✓ Data extraction complete!')
"
```

**Expected output:**
```
Starting comprehensive data extraction...
✓ Inserted 2705 items from Project Zomboid scripts
✓ Inserted 500+ recipes from Project Zomboid scripts
✓ Data extraction complete!
```

### Verify database population:

```bash
# Check item count
uv run python -c "
import sqlite3
conn = sqlite3.connect('mcp_data.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM items_fts')
count = cursor.fetchone()[0]
print(f'✓ Database contains {count} items')
conn.close()
"
```

## Step 6: Configure Claude Desktop

### Find WSL project path:

In Ubuntu terminal:
```bash
# Get the full Windows path to your project
wslpath -w $(pwd)
```

**Example output:** `C:\Users\YourName\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu_79rhkp1fndgsc\LocalState\rootfs\home\username\pzmcp`

### Configure Claude Desktop:

1. **Open Claude Desktop**

2. **Go to Settings** (gear icon)

3. **Open MCP Settings** → **Edit Config**

4. **Add this configuration** (replace the path with your WSL path):

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

**Important:** Replace `/home/username/` with your actual username!

### Alternative: Direct Windows Python approach

If you prefer not to use WSL for the MCP server:

```json
{
  "mcpServers": {
    "project-zomboid": {
      "command": "python",
      "args": ["C:\\Users\\YourName\\path\\to\\pzmcp\\run_server.py"],
      "cwd": "C:\\Users\\YourName\\path\\to\\pzmcp"
    }
  }
}
```

## Step 7: Test the Integration

1. **Restart Claude Desktop** completely

2. **Open a new conversation**

3. **Test basic functionality:**
   ```
   Use the Project Zomboid MCP to find me a baseball bat
   ```

4. **Test script generation:**
   ```
   Create a Project Zomboid script for a steel katana with high damage
   ```

5. **Test search capabilities:**
   ```
   Search for all items that contain "apple" in their name
   ```

**Expected responses:**
- ✅ Claude should find items from the PZ database
- ✅ Claude should generate properly formatted PZ scripts
- ✅ Claude should perform intelligent searches

## Troubleshooting

### MCP Server Won't Start

**Check WSL connection:**
```bash
# In Ubuntu terminal
uv run python run_server.py
```

**Common issues:**
- **Path errors**: Verify paths in config don't have spaces or special characters
- **Permission errors**: Ensure WSL can access Windows files
- **Python errors**: Make sure all dependencies are installed with `uv sync`

### Claude Desktop Can't Connect

1. **Check MCP config syntax** - JSON must be valid
2. **Verify paths** - Use forward slashes in WSL paths
3. **Check logs** - Claude Desktop → Help → Show Logs
4. **Restart Claude** - Complete restart required after config changes

### Database Issues

**Re-extract data:**
```bash
# Clear and re-populate database
rm mcp_data.db
uv run python -c "
from mcp_server.core.enhanced_data_extractor import extract_with_path_manager
extract_with_path_manager(comprehensive=True)
"
```

**Check Project Zomboid path:**
```bash
# Manually verify PZ installation
ls "/mnt/c/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media/scripts/"
```

### Performance Issues

**WSL performance tips:**
- Store project files in WSL filesystem (`/home/username/`) not Windows filesystem (`/mnt/c/`)
- Use WSL 2 (not WSL 1)
- Allocate more memory to WSL if needed

**Windows .wslconfig example** (`C:\Users\YourName\.wslconfig`):
```ini
[wsl2]
memory=8GB
processors=4
```

## Advanced Configuration

### Auto-start MCP Server

Create a startup script in WSL:

```bash
# Create startup script
cat > ~/start-pzmcp.sh << 'EOF'
#!/bin/bash
cd ~/pzmcp
/home/$(whoami)/.local/bin/uv run python run_server.py
EOF

chmod +x ~/start-pzmcp.sh
```

Update Claude Desktop config:
```json
{
  "mcpServers": {
    "project-zomboid": {
      "command": "C:\\Windows\\System32\\wsl.exe",
      "args": ["-d", "Ubuntu", "/home/username/start-pzmcp.sh"]
    }
  }
}
```

### Multiple Project Zomboid Versions

Add multiple paths for different PZ versions:

```bash
# Add paths for different versions
uv run python pz_path_manager.py --add "pz_stable" "C:\Steam\steamapps\common\ProjectZomboid\media\scripts" 1
uv run python pz_path_manager.py --add "pz_beta" "C:\Steam\steamapps\common\ProjectZomboidBeta\media\scripts" 2
```

## Getting Help

- **GitHub Issues**: Report bugs and feature requests
- **Discord**: Join the Project Zomboid modding community  
- **Documentation**: Check README.md for additional information

---

**Need help?** The MCP server includes comprehensive logging. Check the terminal output for detailed error messages and troubleshooting information.