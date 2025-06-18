#!/usr/bin/env python3
"""
Setup MCP server integration for Claude Code in WSL
"""

import os
import json
import subprocess
import sys

def create_wsl_launcher():
    """Create a WSL-compatible launcher script."""
    launcher_content = '''#!/bin/bash
# WSL Launcher for Project Zomboid MCP Server

cd "$(dirname "$0")"

# Use Poetry if available, otherwise use direct python
if command -v poetry &> /dev/null; then
    echo "Using Poetry environment..." >&2
    poetry run python -m mcp_server.mcp_server
else
    echo "Using system Python..." >&2
    python3 -m mcp_server.mcp_server
fi
'''
    
    with open('/mnt/c/Users/winkk/code/pzmcp/run_server_wsl.sh', 'w') as f:
        f.write(launcher_content)
    
    # Make executable
    os.chmod('/mnt/c/Users/winkk/code/pzmcp/run_server_wsl.sh', 0o755)
    print("✅ Created WSL launcher script")

def create_claude_code_config():
    """Create Claude Code MCP configuration."""
    
    # Claude Code config locations to try
    config_paths = [
        os.path.expanduser("~/.config/claude-code/mcp_servers.json"),
        os.path.expanduser("~/.claude-code/mcp_servers.json"),
        "/mnt/c/Users/winkk/.config/claude-code/mcp_servers.json",
        "/mnt/c/Users/winkk/AppData/Roaming/claude-code/mcp_servers.json"
    ]
    
    config = {
        "mcpServers": {
            "project-zomboid": {
                "command": "/mnt/c/Users/winkk/code/pzmcp/run_server_wsl.sh",
                "cwd": "/mnt/c/Users/winkk/code/pzmcp",
                "env": {
                    "PYTHONPATH": "/mnt/c/Users/winkk/code/pzmcp"
                }
            }
        }
    }
    
    # Try to find the right config directory
    for config_path in config_paths:
        config_dir = os.path.dirname(config_path)
        if os.path.exists(config_dir) or config_path.startswith('/mnt/c'):
            try:
                os.makedirs(config_dir, exist_ok=True)
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                print(f"✅ Created Claude Code config: {config_path}")
                return config_path
            except Exception as e:
                print(f"❌ Failed to create {config_path}: {e}")
                continue
    
    # Fallback - create in current directory
    fallback_path = "/mnt/c/Users/winkk/code/pzmcp/claude_code_mcp_config.json"
    with open(fallback_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"✅ Created fallback config: {fallback_path}")
    return fallback_path

def test_wsl_server():
    """Test the WSL server setup."""
    print("\n=== Testing WSL Server ===")
    
    try:
        # Test Poetry environment
        result = subprocess.run(['poetry', 'run', 'python', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Poetry Python: {result.stdout.strip()}")
        else:
            print("❌ Poetry not available")
    except Exception as e:
        print(f"❌ Poetry test failed: {e}")
    
    try:
        # Test MCP server imports
        result = subprocess.run(['poetry', 'run', 'python', '-c', 
                               'from mcp_server.mcp_server import server; print("MCP server OK")'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ MCP server imports successfully")
        else:
            print(f"❌ MCP server import failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Import test failed: {e}")

def main():
    print("=== Setting up Project Zomboid MCP for Claude Code (WSL) ===")
    print(f"Working directory: {os.getcwd()}")
    print(f"Python: {sys.executable}")
    
    # Step 1: Create WSL launcher
    create_wsl_launcher()
    
    # Step 2: Create Claude Code config
    config_path = create_claude_code_config()
    
    # Step 3: Test setup
    test_wsl_server()
    
    print("\n=== Setup Complete ===")
    print("✅ WSL launcher created")
    print("✅ Claude Code config created")
    
    print(f"\n=== Next Steps ===")
    print("1. Restart Claude Code")
    print("2. Test MCP integration")
    print("3. If config location is wrong, manually copy the config:")
    print(f"   Source: {config_path}")
    print("   Target: Your Claude Code MCP config directory")
    
    print(f"\n=== Manual Config (if needed) ===")
    print("If automatic config doesn't work, add this to Claude Code:")
    print(json.dumps({
        "mcpServers": {
            "project-zomboid": {
                "command": "/mnt/c/Users/winkk/code/pzmcp/run_server_wsl.sh",
                "cwd": "/mnt/c/Users/winkk/code/pzmcp"
            }
        }
    }, indent=2))

if __name__ == "__main__":
    main()