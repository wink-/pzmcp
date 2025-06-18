#!/usr/bin/env python3
"""
Debug version of MCP server that logs everything
"""

import sys
import os
import json
import time

def debug_server():
    """Run a debug MCP server that logs all communication."""
    print("=== DEBUG MCP SERVER ===", file=sys.stderr)
    print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}", file=sys.stderr)
    print(f"Python: {sys.executable}", file=sys.stderr)
    print(f"Working dir: {os.getcwd()}", file=sys.stderr)
    print("Waiting for messages...", file=sys.stderr)
    
    message_count = 0
    
    while True:
        try:
            # Read input
            line = sys.stdin.readline()
            message_count += 1
            
            print(f"\n--- Message #{message_count} ---", file=sys.stderr)
            
            if not line:
                print("EOF received - client disconnected", file=sys.stderr)
                break
                
            line = line.strip()
            print(f"Raw input: {line}", file=sys.stderr)
            
            if not line:
                print("Empty line, ignoring", file=sys.stderr)
                continue
            
            # Parse message
            try:
                message = json.loads(line)
                method = message.get('method', 'unknown')
                msg_id = message.get('id')
                print(f"Parsed method: {method}, id: {msg_id}", file=sys.stderr)
                
                # Always respond with success
                if msg_id is not None:  # Request needs response
                    if method == 'initialize':
                        response = {
                            "jsonrpc": "2.0",
                            "id": msg_id,
                            "result": {
                                "protocolVersion": "1.0.0",
                                "capabilities": {
                                    "tools": {"listChanged": False},
                                    "resources": {"subscribe": False, "listChanged": False}
                                },
                                "serverInfo": {
                                    "name": "debug-server",
                                    "version": "1.0.0"
                                }
                            }
                        }
                    elif method == 'tools/list':
                        response = {
                            "jsonrpc": "2.0",
                            "id": msg_id,
                            "result": {
                                "tools": [
                                    {
                                        "name": "debug_tool",
                                        "description": "A debug tool",
                                        "inputSchema": {
                                            "type": "object",
                                            "properties": {},
                                            "required": []
                                        }
                                    }
                                ]
                            }
                        }
                    else:
                        response = {
                            "jsonrpc": "2.0",
                            "id": msg_id,
                            "result": {"message": f"Received {method}"}
                        }
                    
                    response_json = json.dumps(response)
                    print(f"Sending response: {response_json}", file=sys.stderr)
                    print(response_json, flush=True)
                    
                else:  # Notification
                    print(f"Notification received: {method}", file=sys.stderr)
                    if method == 'initialized':
                        print("Server is now ready!", file=sys.stderr)
                
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}", file=sys.stderr)
                if msg_id is not None:
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "error": {"code": -32700, "message": "Parse error"}
                    }
                    print(json.dumps(error_response), flush=True)
            
        except EOFError:
            print("EOF in readline", file=sys.stderr)
            break
        except KeyboardInterrupt:
            print("Keyboard interrupt", file=sys.stderr)
            break
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            print(f"Exception type: {type(e)}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
    
    print(f"\n=== SERVER SHUTDOWN ===", file=sys.stderr)
    print(f"Processed {message_count} messages", file=sys.stderr)
    print(f"Ended at: {time.strftime('%Y-%m-%d %H:%M:%S')}", file=sys.stderr)

if __name__ == "__main__":
    debug_server()