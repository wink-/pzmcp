#!/usr/bin/env python3
"""
Install dependencies for Windows Python installation
"""

import subprocess
import sys
import os

def run_command(cmd):
    """Run a command and return success status."""
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Success")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ Failed with return code {result.returncode}")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False

def main():
    """Install dependencies."""
    print("Installing Project Zomboid MCP Server dependencies for Windows...")
    print("=" * 60)
    
    python_exe = sys.executable
    print(f"Using Python: {python_exe}")
    print(f"Python version: {sys.version}")
    
    # List of packages to install
    packages = [
        "mcp>=1.0.0",
        "pydantic>=2.0.0",
        "sqlalchemy>=2.0.0", 
        "rich>=13.0.0"
    ]
    
    success_count = 0
    for package in packages:
        print(f"\nInstalling {package}...")
        if run_command([python_exe, "-m", "pip", "install", package]):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"Installation complete: {success_count}/{len(packages)} packages installed")
    
    if success_count == len(packages):
        print("✓ All dependencies installed successfully!")
        
        # Test imports
        print("\nTesting imports...")
        try:
            import mcp
            print("✓ mcp imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import mcp: {e}")
            
        try:
            import pydantic
            print("✓ pydantic imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import pydantic: {e}")
            
        try:
            import sqlalchemy
            print("✓ sqlalchemy imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import sqlalchemy: {e}")
            
        try:
            import rich
            print("✓ rich imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import rich: {e}")
        
        print("\nYou can now test the MCP server with:")
        print(f"  {python_exe} run_server.py")
        
    else:
        print("✗ Some dependencies failed to install")
        print("You may need to:")
        print("1. Run as administrator")
        print("2. Upgrade pip: python -m pip install --upgrade pip")
        print("3. Use a virtual environment")
        
    return 0 if success_count == len(packages) else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        input("\nPress Enter to continue...")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nInstallation cancelled by user")
        sys.exit(1)