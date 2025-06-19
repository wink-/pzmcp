#!/usr/bin/env python3
"""Test modern server import and basic functionality."""

try:
    from mcp_server.modern_server import mcp
    print("✅ Modern server imports successfully")
    print(f"Server name: {mcp.name}")
    print(f"Dependencies: {len(mcp.dependencies)} packages")
    print("✅ Modern server is ready!")
except Exception as e:
    print(f"❌ Error importing modern server: {e}")
    import traceback
    traceback.print_exc()
