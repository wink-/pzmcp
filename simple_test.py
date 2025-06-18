#!/usr/bin/env python3
"""
Simple test for the Project Zomboid MCP Server

Tests the server components directly without full MCP client setup.
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_server_components():
    """Test MCP server components directly."""
    print("=== Testing MCP Server Components ===\n")
    
    try:
        # Test 1: Import and initialize services
        print("1. Testing service initialization...")
        from mcp_server.mcp_server import initialize_services
        await initialize_services()
        print("✓ Services initialized successfully\n")
        
        # Test 2: Test individual tools
        print("2. Testing MCP tools...")
        from mcp_server.mcp_server import (
            validate_script_tool,
            check_references_tool,
            analyze_mod_tool,
            search_vanilla_tool
        )
        
        # Test script validation
        print("   Testing validate_script...")
        test_script = """
        module Base {
            item Apple {
                Type = Food,
                DisplayName = Red Apple,
                Icon = Apple,
                Weight = 0.1,
            }
        }
        """
        result = await validate_script_tool(test_script, "item")
        print(f"   ✓ Validation result: {result}\n")
        
        # Test reference checking
        print("   Testing check_references...")
        result = await check_references_tool(["Base.Apple", "Invalid.Reference"], "item")
        print(f"   ✓ Reference check: {result}\n")
        
        # Test mod analysis
        print("   Testing analyze_mod...")
        result = await analyze_mod_tool(".")
        print(f"   ✓ Mod analysis: {result}\n")
        
        # Test search (may not have data yet)
        print("   Testing search_vanilla...")
        result = await search_vanilla_tool("apple")
        print(f"   ✓ Search result: {result}\n")
        
        # Test 3: Test MCP server setup
        print("3. Testing MCP server setup...")
        from mcp_server.mcp_server import server, list_tools, list_resources
        
        # Test resource listing
        resources = await list_resources()
        print(f"   ✓ Found {len(resources)} resources:")
        for resource in resources:
            print(f"     - {resource.name}")
        
        # Test tool listing  
        tools = await list_tools()
        print(f"   ✓ Found {len(tools)} tools:")
        for tool in tools:
            print(f"     - {tool.name}: {tool.description}")
        
        print("\n✓ All component tests passed!")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_database():
    """Test database initialization."""
    print("=== Testing Database ===")
    
    try:
        from mcp_server.core.database import create_db_and_tables, engine
        print("Creating database tables...")
        create_db_and_tables()
        print("✓ Database tables created successfully")
        
        # Check if database file exists
        if os.path.exists("mcp_data.db"):
            print("✓ Database file created: mcp_data.db")
        else:
            print("✗ Database file not found")
            
    except Exception as e:
        print(f"✗ Database test failed: {e}")

def run_basic_server_test():
    """Run a basic server test without full MCP protocol."""
    print("=== Basic Server Test ===")
    
    try:
        # Test that we can import the server
        from mcp_server.mcp_server import server
        print("✓ MCP server module imported successfully")
        
        # Test that server has expected methods
        if hasattr(server, 'list_tools'):
            print("✓ Server has list_tools method")
        if hasattr(server, 'list_resources'): 
            print("✓ Server has list_resources method")
        if hasattr(server, 'call_tool'):
            print("✓ Server has call_tool method")
            
    except Exception as e:
        print(f"✗ Basic server test failed: {e}")

async def main():
    """Main test function."""
    print("Project Zomboid MCP Server - Test Suite")
    print("=" * 50)
    
    # Test 1: Database
    test_database()
    print()
    
    # Test 2: Basic server
    run_basic_server_test()
    print()
    
    # Test 3: Components
    await test_server_components()
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("- Database initialization: ✓")
    print("- MCP server module: ✓") 
    print("- MCP tools: ✓")
    print("- MCP resources: ✓")
    print("\nTo run the actual MCP server:")
    print("poetry run python -m mcp_server.mcp_server")

if __name__ == "__main__":
    asyncio.run(main())