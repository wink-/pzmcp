#!/usr/bin/env python3
"""
Standalone Project Zomboid MCP Server

This version attempts to run without requiring all dependencies,
providing fallback functionality when packages are missing.
"""

import sys
import os
import json
import asyncio

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_dependencies():
    """Check which dependencies are available."""
    deps = {}
    
    try:
        import mcp
        deps['mcp'] = True
        print("✓ MCP library found", file=sys.stderr)
    except ImportError:
        deps['mcp'] = False
        print("✗ MCP library not found", file=sys.stderr)
    
    try:
        import pydantic
        deps['pydantic'] = True
        print("✓ Pydantic found", file=sys.stderr)
    except ImportError:
        deps['pydantic'] = False
        print("✗ Pydantic not found", file=sys.stderr)
    
    try:
        import sqlalchemy
        deps['sqlalchemy'] = True
        print("✓ SQLAlchemy found", file=sys.stderr)
    except ImportError:
        deps['sqlalchemy'] = False
        print("✗ SQLAlchemy not found", file=sys.stderr)
    
    return deps

def simple_mcp_server():
    """Run a simple MCP server simulation for testing."""
    print("Starting simple MCP server simulation...", file=sys.stderr)
    
    # Simple JSON-RPC message handling
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                print("No more input, shutting down", file=sys.stderr)
                break
                
            line = line.strip()
            if not line:
                continue
                
            # Parse JSON-RPC message
            try:
                message = json.loads(line)
                method = message.get('method', 'unknown')
                msg_id = message.get('id')
                print(f"Received message: {method} (id: {msg_id})", file=sys.stderr)
                
                # Handle initialize
                if method == 'initialize':
                    response = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "protocolVersion": "1.0.0",
                            "capabilities": {
                                "tools": {
                                    "listChanged": False
                                },
                                "resources": {
                                    "subscribe": False,
                                    "listChanged": False
                                }
                            },
                            "serverInfo": {
                                "name": "project-zomboid-fallback",
                                "version": "0.1.0"
                            }
                        }
                    }
                    print(json.dumps(response), flush=True)
                    
                # Handle initialized notification
                elif method == 'initialized':
                    print("Server initialized successfully", file=sys.stderr)
                    print("Waiting for tool and resource requests...", file=sys.stderr)
                    # No response needed for notifications
                    
                # Handle list tools
                elif method == 'tools/list':
                    response = {
                        "jsonrpc": "2.0", 
                        "id": msg_id,
                        "result": {
                            "tools": [
                                {
                                    "name": "validate_script",
                                    "description": "Validate Project Zomboid script syntax (fallback mode)",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "content": {"type": "string", "description": "Script content"},
                                            "script_type": {"type": "string", "description": "Type of script"}
                                        },
                                        "required": ["content", "script_type"]
                                    }
                                },
                                {
                                    "name": "install_dependencies",
                                    "description": "Get instructions for installing full MCP server dependencies",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {},
                                        "required": []
                                    }
                                }
                            ]
                        }
                    }
                    print(json.dumps(response), flush=True)
                    
                # Handle list resources
                elif method == 'resources/list':
                    response = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "resources": [
                                {
                                    "uri": "resource://setup_instructions",
                                    "name": "Setup Instructions",
                                    "description": "Instructions for installing full MCP server",
                                    "mimeType": "text/plain"
                                }
                            ]
                        }
                    }
                    print(json.dumps(response), flush=True)
                    
                # Handle tool calls
                elif method == 'tools/call':
                    tool_name = message.get('params', {}).get('name')
                    if tool_name == 'validate_script':
                        response = {
                            "jsonrpc": "2.0",
                            "id": msg_id,
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Fallback mode: Basic validation only. Install full dependencies for advanced validation.\nTo install: python install_windows_deps.py"
                                    }
                                ]
                            }
                        }
                        print(json.dumps(response), flush=True)
                    elif tool_name == 'install_dependencies':
                        response = {
                            "jsonrpc": "2.0",
                            "id": msg_id,
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"To install full MCP server dependencies:\n\n1. Run this command:\n   {sys.executable} install_windows_deps.py\n\n2. Or install manually:\n   {sys.executable} -m pip install mcp pydantic sqlalchemy rich\n\n3. Update Claude Desktop config to use run_server.py instead of run_server_standalone.py\n\n4. Restart Claude Desktop"
                                    }
                                ]
                            }
                        }
                        print(json.dumps(response), flush=True)
                    else:
                        response = {
                            "jsonrpc": "2.0",
                            "id": msg_id,
                            "error": {
                                "code": -32601,
                                "message": f"Unknown tool: {tool_name}"
                            }
                        }
                        print(json.dumps(response), flush=True)
                        
                # Handle ping
                elif method == 'ping':
                    response = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {}
                    }
                    print(json.dumps(response), flush=True)
                    
                # Handle other methods
                else:
                    if msg_id is not None:  # Only respond to requests, not notifications
                        response = {
                            "jsonrpc": "2.0",
                            "id": msg_id,
                            "error": {
                                "code": -32601,
                                "message": f"Method not found: {method}"
                            }
                        }
                        print(json.dumps(response), flush=True)
                    
            except json.JSONDecodeError as e:
                print(f"Invalid JSON received: {line} - Error: {e}", file=sys.stderr)
                if msg_id is not None:
                    response = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    print(json.dumps(response), flush=True)
                continue
                
        except EOFError:
            print("EOF received, shutting down", file=sys.stderr)
            break
        except KeyboardInterrupt:
            print("Interrupted, shutting down", file=sys.stderr)
            break
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            continue

async def run_full_server():
    """Run the full MCP server if dependencies are available."""
    try:
        from mcp_server.mcp_server import main as server_main
        print("Starting full MCP server...", file=sys.stderr)
        await server_main()
    except Exception as e:
        print(f"Error running full MCP server: {e}", file=sys.stderr)
        raise

def main():
    """Main entry point."""
    print(f"Python executable: {sys.executable}", file=sys.stderr)
    print(f"Script location: {__file__}", file=sys.stderr)
    
    deps = check_dependencies()
    
    # Check if we have minimum requirements for full server
    if deps.get('mcp') and deps.get('pydantic'):
        print("All dependencies found, starting full MCP server...", file=sys.stderr)
        try:
            asyncio.run(run_full_server())
        except Exception as e:
            print(f"Full server failed: {e}", file=sys.stderr)
            print("Falling back to simple server...", file=sys.stderr)
            simple_mcp_server()
    else:
        print("Missing dependencies, running in fallback mode...", file=sys.stderr)
        print("To install dependencies, run:", file=sys.stderr)
        print(f"  {sys.executable} install_windows_deps.py", file=sys.stderr)
        print(f"  {sys.executable} -m pip install mcp pydantic sqlalchemy rich", file=sys.stderr)
        print("Starting fallback MCP server...", file=sys.stderr)
        simple_mcp_server()

if __name__ == "__main__":
    main()