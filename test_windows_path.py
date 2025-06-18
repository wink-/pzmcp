#!/usr/bin/env python3
"""
Test script to verify Windows paths and Python installation
"""

import sys
import os
import subprocess

def main():
    print("=== Windows Path Test ===")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Script location: {os.path.abspath(__file__)}")
    
    # Check if run_server.py exists
    script_path = os.path.join(os.path.dirname(__file__), "run_server.py")
    print(f"run_server.py path: {script_path}")
    print(f"run_server.py exists: {os.path.exists(script_path)}")
    
    # Test running the server script
    if os.path.exists(script_path):
        print("\n=== Testing run_server.py ===")
        try:
            # Don't actually run it, just check if it can be imported
            import run_server
            print("✓ run_server.py can be imported")
        except Exception as e:
            print(f"✗ Error importing run_server.py: {e}")
    
    # Print the exact configuration for Claude Desktop
    python_exe = sys.executable.replace('\\', '\\\\')
    script_path_escaped = script_path.replace('\\', '\\\\')
    cwd_escaped = os.path.dirname(script_path).replace('\\', '\\\\')
    
    print(f"\n=== Claude Desktop Configuration ===")
    print("Copy this to %APPDATA%\\Claude\\claude_desktop_config.json:")
    print(f"""{{
  "mcpServers": {{
    "project-zomboid": {{
      "command": "{python_exe}",
      "args": ["{script_path_escaped}"],
      "cwd": "{cwd_escaped}"
    }}
  }}
}}""")

if __name__ == "__main__":
    main()