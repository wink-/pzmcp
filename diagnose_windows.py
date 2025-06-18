#!/usr/bin/env python3
"""
Comprehensive diagnostic for Windows MCP server setup
"""

import sys
import os

def main():
    print("=== Project Zomboid MCP Server Diagnostic ===")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print()
    
    # Test imports
    print("=== Testing Dependencies ===")
    
    deps = {
        'mcp': 'MCP Python SDK',
        'pydantic': 'Data validation library', 
        'sqlalchemy': 'Database ORM',
        'rich': 'Terminal formatting'
    }
    
    success_count = 0
    for module, description in deps.items():
        try:
            __import__(module)
            print(f"✅ {module:12} - {description}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {module:12} - {description} (ERROR: {e})")
    
    print(f"\nDependencies: {success_count}/{len(deps)} installed")
    
    # Test MCP server import
    print("\n=== Testing MCP Server Import ===")
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from mcp_server.mcp_server import server, list_tools, list_resources
        print("✅ MCP server imports successfully")
        
        # Test server components
        print("\n=== Testing Server Components ===")
        try:
            import asyncio
            
            async def test_components():
                try:
                    tools = await list_tools()
                    print(f"✅ Tools available: {len(tools)}")
                    for tool in tools:
                        print(f"   - {tool.name}")
                    
                    resources = await list_resources()
                    print(f"✅ Resources available: {len(resources)}")
                    for resource in resources:
                        print(f"   - {resource.name}")
                    
                    return True
                except Exception as e:
                    print(f"❌ Component test failed: {e}")
                    return False
            
            result = asyncio.run(test_components())
            if result:
                print("\n🎉 FULL MCP SERVER IS READY!")
                print("✅ All 5 tools should be available")
                print("✅ All 4 resources should be available")
            else:
                print("\n⚠️  MCP server has issues")
                
        except Exception as e:
            print(f"❌ Component test error: {e}")
            
    except ImportError as e:
        print(f"❌ Cannot import MCP server: {e}")
        print("⚠️  Will fall back to basic server")
    
    # File existence check
    print("\n=== File System Check ===")
    files_to_check = [
        'run_server.py',
        'run_server_v2.py', 
        'mcp_server/mcp_server.py',
        'mcp_server/core/database.py'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
    
    # Configuration recommendation
    print("\n=== Configuration Recommendation ===")
    
    if success_count == len(deps):
        print("🚀 RECOMMENDED: Use full server")
        print("Config should use: run_server.py")
        print("Expected tools: 5 (validate_script, generate_script, search_vanilla, check_references, analyze_mod)")
    else:
        print("⚠️  RECOMMENDED: Use fallback server")
        print("Config should use: run_server_v2.py")
        print("Expected tools: 2 (validate_script, get_help)")
        print("\nTo upgrade, install missing dependencies:")
        print(f"  {sys.executable} -m pip install mcp pydantic sqlalchemy rich")
    
    print(f"\n=== Claude Desktop Config ===")
    config = f'''{{
  "mcpServers": {{
    "project-zomboid": {{
      "command": "{sys.executable.replace(chr(92), chr(92)*2)}",
      "args": ["C:\\\\Users\\\\winkk\\\\code\\\\pzmcp\\\\{'run_server.py' if success_count == len(deps) else 'run_server_v2.py'}"],
      "cwd": "C:\\\\Users\\\\winkk\\\\code\\\\pzmcp"
    }}
  }}
}}'''
    print(config)

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")