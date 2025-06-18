#!/usr/bin/env python3
"""
Test the standalone MCP server locally
"""

import subprocess
import json
import sys
import time

def test_mcp_server():
    """Test the standalone MCP server."""
    print("Testing standalone MCP server...")
    
    # Start the server
    server_process = subprocess.Popen(
        [sys.executable, "run_server_standalone.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    def send_message(message):
        """Send a JSON-RPC message and get response."""
        json_msg = json.dumps(message) + "\n"
        server_process.stdin.write(json_msg)
        server_process.stdin.flush()
        
        # Read response
        response_line = server_process.stdout.readline()
        if response_line:
            return json.loads(response_line.strip())
        return None
    
    try:
        # Test 1: Initialize
        print("1. Testing initialize...")
        init_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "1.0.0",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        response = send_message(init_msg)
        if response and response.get("result"):
            print("✓ Initialize successful")
            print(f"  Server: {response['result']['serverInfo']['name']}")
        else:
            print("✗ Initialize failed")
            return False
        
        # Test 2: Send initialized notification
        print("2. Sending initialized notification...")
        initialized_msg = {
            "jsonrpc": "2.0",
            "method": "initialized"
        }
        send_message(initialized_msg)
        
        # Test 3: List tools
        print("3. Testing tools/list...")
        tools_msg = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        response = send_message(tools_msg)
        if response and response.get("result"):
            tools = response["result"]["tools"]
            print(f"✓ Found {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
        else:
            print("✗ Tools list failed")
            return False
        
        # Test 4: Call a tool
        print("4. Testing tool call...")
        tool_call_msg = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "validate_script",
                "arguments": {
                    "content": "item Apple { Type = Food }",
                    "script_type": "item"
                }
            }
        }
        
        response = send_message(tool_call_msg)
        if response and response.get("result"):
            content = response["result"]["content"][0]["text"]
            print("✓ Tool call successful")
            print(f"  Response: {content[:100]}...")
        else:
            print("✗ Tool call failed")
            return False
        
        print("\n✓ All tests passed! The standalone server is working.")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False
        
    finally:
        # Clean up
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    success = test_mcp_server()
    if success:
        print("\n🎉 The standalone server is ready for Claude Desktop!")
        print("\nNext steps:")
        print("1. Make sure your Claude Desktop config uses run_server_standalone.py")
        print("2. Restart Claude Desktop")
        print("3. Ask Claude: 'What MCP tools are available?'")
    else:
        print("\n❌ Tests failed. Check the errors above.")
    
    input("\nPress Enter to exit...")