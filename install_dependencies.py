#!/usr/bin/env python3
"""
Install dependencies for the Project Zomboid MCP Server

This script installs the required dependencies without Poetry.
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a Python package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package}: {e}")
        return False

def main():
    """Install all required dependencies."""
    print("Installing Project Zomboid MCP Server dependencies...")
    print("=" * 50)
    
    # Required packages
    packages = [
        "mcp>=1.0.0",
        "pydantic>=2.0.0", 
        "sqlalchemy>=2.0.0",
        "rich>=13.0.0"
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"Installation complete: {success_count}/{len(packages)} packages installed")
    
    if success_count == len(packages):
        print("✓ All dependencies installed successfully!")
        print("\nYou can now run the MCP server with:")
        print("  python run_server.py")
    else:
        print("✗ Some dependencies failed to install")
        print("Please check the error messages above")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())