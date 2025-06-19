#!/usr/bin/env python3
"""
Modern launcher for the Project Zomboid MCP Server using FastMCP
"""

import asyncio
import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import the FastMCP server object for MCP tools
try:
    from mcp_server.modern_server import mcp
except ImportError as e:
    print(f"Error: Could not import modern MCP server: {e}", file=sys.stderr)
    print("Make sure all dependencies are installed:", file=sys.stderr)
    print("uv sync", file=sys.stderr)
    sys.exit(1)

def main():
    """Run the modern MCP server."""
    try:
        # Import and run the FastMCP server directly
        from mcp_server.modern_server import mcp
        import sys
        
        # Check for HTTP mode
        if len(sys.argv) > 1 and sys.argv[1] == "--http":
            mcp.run(transport="sse", host="0.0.0.0", port=8000)
        else:
            # Run stdio server (default for MCP clients like Claude Desktop)
            mcp.run()
            
    except Exception as e:
        print(f"Error running modern MCP server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
