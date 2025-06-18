# 🔍 Diagnostic Steps

## Issue Summary
You're still seeing only 2 Project Zomboid tools instead of 5, which suggests the upgrade didn't complete properly.

## Step 1: Run Comprehensive Diagnostic

Open **Command Prompt** and run:

```cmd
cd C:\Users\winkk\code\pzmcp
C:\Users\winkk\AppData\Local\Programs\Python\Python313\python.exe diagnose_windows.py
```

This will tell us:
- ✅ Which dependencies are installed
- ✅ Whether the full server can start
- ✅ How many tools are available
- ✅ Correct configuration to use

## Step 2: Possible Outcomes

### Outcome A: All Dependencies OK
```
Dependencies: 4/4 installed
✅ MCP server imports successfully
🎉 FULL MCP SERVER IS READY!
✅ All 5 tools should be available
```
**Action:** Update Claude Desktop config to use `run_server.py`

### Outcome B: Missing Dependencies
```
Dependencies: 2/4 installed
❌ mcp - MCP Python SDK (ERROR: No module named 'mcp')
⚠️ RECOMMENDED: Use fallback server
```
**Action:** Reinstall dependencies or use fallback server

### Outcome C: Import Errors
```
Dependencies: 4/4 installed
❌ Cannot import MCP server: [error details]
```
**Action:** Fix import issues

## Step 3: Based on Diagnostic Results

The diagnostic will provide:
1. **Exact dependency status**
2. **Recommended configuration**
3. **Copy-paste Claude Desktop config**

## Expected Tool Counts

### Full Server (5 tools):
- validate_script
- generate_script  
- search_vanilla
- check_references
- analyze_mod

### Fallback Server (2 tools):
- validate_script
- get_help

## Quick Test Alternative

If you want a quick test, try this command:

```cmd
C:\Users\winkk\AppData\Local\Programs\Python\Python313\python.exe -c "import mcp; import pydantic; print('SUCCESS: All dependencies installed')"
```

If this works, the issue is likely:
- Config not updated in Claude Desktop
- Claude Desktop needs complete restart
- Cache issue

Please run the diagnostic and share the results!