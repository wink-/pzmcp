# Debug Steps for Claude Desktop Integration

## The Issue
The server starts, responds to initialize, but then disconnects. Let's debug this step by step.

## Debug Configuration

**Step 1: Use the debug server**

Replace your Claude Desktop config with this debug version:

```json
{
  "mcpServers": {
    "project-zomboid": {
      "command": "C:\\Users\\winkk\\AppData\\Local\\Programs\\Python\\Python313\\python.exe",
      "args": ["C:\\Users\\winkk\\code\\pzmcp\\debug_server.py"],
      "cwd": "C:\\Users\\winkk\\code\\pzmcp"
    }
  }
}
```

**Step 2: Restart Claude Desktop**

**Step 3: Check the logs**

The debug server will log everything to help us understand what's happening.

## What We Know

From your logs:
1. ✅ Server starts correctly
2. ✅ Receives initialize message (id: 0)  
3. ✅ Sends proper response
4. ❌ Connection closes after first message

## Possible Causes

1. **Missing `initialized` notification** - Client may not be sending it
2. **Capability mismatch** - Our capabilities might not match expectations
3. **Protocol version issue** - Version compatibility problem
4. **Buffer flushing** - Output not being flushed properly

## What the Debug Server Will Show

- Every message received
- Every response sent
- Exact timing of disconnection
- Any errors that occur

## Next Steps After Debug

Once we see the debug output, we can:
1. Fix any protocol issues
2. Adjust the capabilities
3. Handle missing messages
4. Update the main server

## Manual Test

You can also test manually:

```cmd
cd C:\Users\winkk\code\pzmcp
C:\Users\winkk\AppData\Local\Programs\Python\Python313\python.exe debug_server.py
```

Then type:
```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"1.0.0","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
```

And see what happens.