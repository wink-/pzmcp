#!/usr/bin/env python3
"""
Project Zomboid MCP Server v2 - Robust version for Windows
"""

import sys
import os
import json
import time
import signal
import threading

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

class MCPServer:
    def __init__(self):
        self.running = True
        self.initialized = False
        self.message_count = 0
        
        # Set up signal handlers
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)
    
    def log(self, message):
        """Log to stderr with timestamp."""
        timestamp = time.strftime('%H:%M:%S')
        print(f"[{timestamp}] {message}", file=sys.stderr, flush=True)
    
    def shutdown(self, signum=None, frame=None):
        """Graceful shutdown."""
        self.log(f"Shutdown requested (signal: {signum})")
        self.running = False
    
    def send_response(self, response):
        """Send JSON response to stdout."""
        json_response = json.dumps(response)
        self.log(f"Sending: {json_response}")
        print(json_response, flush=True)
    
    def handle_initialize(self, msg_id, params):
        """Handle initialize request."""
        client_protocol = params.get('protocolVersion', '2024-11-05')
        self.log(f"Handling initialize request with protocol: {client_protocol}")
        
        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": client_protocol,  # Match client protocol version
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {"subscribe": False, "listChanged": False}
                },
                "serverInfo": {
                    "name": "project-zomboid-mcp",
                    "version": "0.1.0"
                }
            }
        }
        self.send_response(response)
        # Small delay to ensure message is processed
        time.sleep(0.1)
        return True
    
    def handle_initialized(self):
        """Handle initialized notification."""
        self.log("Received initialized notification - server is ready!")
        self.initialized = True
        return True
    
    def handle_tools_list(self, msg_id):
        """Handle tools/list request."""
        self.log("Handling tools/list request")
        tools = [
            {
                "name": "validate_script",
                "description": "Validate Project Zomboid script syntax",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "Script content"},
                        "script_type": {"type": "string", "description": "Script type (item, recipe, vehicle)"}
                    },
                    "required": ["content", "script_type"]
                }
            },
            {
                "name": "get_help",
                "description": "Get help with Project Zomboid modding",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string", "description": "Help topic"}
                    },
                    "required": []
                }
            }
        ]
        
        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": tools}
        }
        self.send_response(response)
        return True
    
    def handle_resources_list(self, msg_id):
        """Handle resources/list request."""
        self.log("Handling resources/list request")
        resources = [
            {
                "uri": "pz://setup_guide",
                "name": "Setup Guide",
                "description": "Installation and setup instructions",
                "mimeType": "text/markdown"
            }
        ]
        
        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"resources": resources}
        }
        self.send_response(response)
        return True
    
    def handle_tool_call(self, msg_id, params):
        """Handle tools/call request."""
        tool_name = params.get('name')
        arguments = params.get('arguments', {})
        
        self.log(f"Handling tool call: {tool_name}")
        
        if tool_name == 'validate_script':
            content = arguments.get('content', '')
            script_type = arguments.get('script_type', 'unknown')
            
            # Simple validation
            result_text = f"Validating {script_type} script...\n"
            if content.strip():
                result_text += "✓ Script has content\n"
                if 'item' in content.lower():
                    result_text += "✓ Contains item definition\n"
                result_text += "Basic validation complete."
            else:
                result_text += "✗ Script is empty"
            
            response = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result_text
                        }
                    ]
                }
            }
        
        elif tool_name == 'get_help':
            topic = arguments.get('topic', 'general')
            help_text = f"""# Project Zomboid Modding Help

## Topic: {topic}

### Basic Script Structure:
```
module MyMod {{
    item MyItem {{
        Type = Food,
        DisplayName = My Custom Item,
        Icon = MyIcon,
        Weight = 0.5,
    }}
}}
```

### To install full MCP server:
Run: `{sys.executable} install_windows_deps.py`

This will enable advanced features like script generation and vanilla data search.
"""
            
            response = {
                "jsonrpc": "2.0", 
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": help_text
                        }
                    ]
                }
            }
        
        else:
            response = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32601,
                    "message": f"Unknown tool: {tool_name}"
                }
            }
        
        self.send_response(response)
        return True
    
    def handle_message(self, message):
        """Handle incoming JSON-RPC message."""
        try:
            data = json.loads(message)
            method = data.get('method')
            msg_id = data.get('id')
            params = data.get('params', {})
            
            self.log(f"Message: {method} (id: {msg_id})")
            
            if method == 'initialize':
                return self.handle_initialize(msg_id, params)
            elif method == 'initialized':
                return self.handle_initialized()
            elif method == 'tools/list':
                return self.handle_tools_list(msg_id)
            elif method == 'resources/list':
                return self.handle_resources_list(msg_id)
            elif method == 'tools/call':
                return self.handle_tool_call(msg_id, params)
            elif method == 'ping':
                response = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
                self.send_response(response)
                return True
            else:
                if msg_id is not None:
                    response = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {method}"
                        }
                    }
                    self.send_response(response)
                return True
                
        except json.JSONDecodeError as e:
            self.log(f"JSON decode error: {e}")
            return False
        except Exception as e:
            self.log(f"Error handling message: {e}")
            return False
    
    def run(self):
        """Main server loop."""
        self.log("Starting Project Zomboid MCP Server v2")
        self.log(f"Python: {sys.executable}")
        self.log(f"Working directory: {os.getcwd()}")
        
        # Change to the correct directory if needed
        if not os.path.exists('run_server_v2.py'):
            self.log("Changing to project directory...")
            os.chdir(project_root)
            self.log(f"New working directory: {os.getcwd()}")
        
        # Keep server alive with a watchdog thread
        def watchdog():
            while self.running:
                time.sleep(1)
        
        watchdog_thread = threading.Thread(target=watchdog, daemon=True)
        watchdog_thread.start()
        
        try:
            while self.running:
                try:
                    line = sys.stdin.readline()
                    if not line:
                        self.log("EOF received from client")
                        break
                    
                    line = line.strip()
                    if not line:
                        continue
                    
                    self.message_count += 1
                    self.log(f"Received message #{self.message_count}: {line[:100]}...")
                    
                    if not self.handle_message(line):
                        self.log("Failed to handle message, continuing...")
                    
                    # Send a heartbeat if we haven't received messages in a while
                    if self.initialized and self.message_count > 1:
                        time.sleep(0.01)  # Small delay between messages
                    
                except EOFError:
                    self.log("EOF in readline")
                    break
                except Exception as e:
                    self.log(f"Error in main loop: {e}")
                    continue
        
        except KeyboardInterrupt:
            self.log("Keyboard interrupt received")
        
        finally:
            self.log(f"Server shutting down. Processed {self.message_count} messages.")

def main():
    """Entry point."""
    server = MCPServer()
    server.run()

if __name__ == "__main__":
    main()