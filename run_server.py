#!/usr/bin/env python3
"""
Direct launcher for the Project Zomboid MCP Server

This script runs the MCP server without Poetry, making it easier to integrate
with Claude Desktop and other MCP clients.
"""

import sys
import os
import asyncio

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

async def main():
    """Run the MCP server directly."""
    try:
        from mcp_server.mcp_server import main as server_main
        await server_main()
    except ImportError as e:
        print(f"Error: Could not import MCP server: {e}", file=sys.stderr)
        print("Make sure all dependencies are installed:", file=sys.stderr)
        print("pip install mcp pydantic sqlalchemy rich", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error running MCP server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())