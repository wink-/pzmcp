#!/bin/bash
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
