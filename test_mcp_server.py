#!/usr/bin/env python3
"""
Test script for the Project Zomboid MCP Server

This script demonstrates how to test the MCP server functionality
both programmatically and interactively.
"""

import asyncio
import json
import logging
from mcp.client import ClientSession
from mcp.client.stdio import stdio_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_mcp_server():
    """Test the MCP server by connecting as a client."""
    
    logger.info("Starting MCP server test...")
    
    # Start the MCP server as a subprocess
    import subprocess
    import sys
    
    server_process = subprocess.Popen([
        sys.executable, "-m", "mcp_server.mcp_server"
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        # Connect to the server
        async with stdio_client(server_process) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                
                logger.info("✓ Successfully connected to MCP server")
                
                # Test 1: List available resources
                logger.info("\n=== Testing Resources ===")
                resources = await session.list_resources()
                logger.info(f"Available resources: {len(resources)}")
                for resource in resources:
                    logger.info(f"  - {resource.name}: {resource.description}")
                
                # Test 2: Read a resource
                if resources:
                    resource_uri = resources[0].uri
                    logger.info(f"\nReading resource: {resource_uri}")
                    try:
                        content = await session.read_resource(resource_uri)
                        logger.info(f"✓ Resource content retrieved (length: {len(str(content))})")
                    except Exception as e:
                        logger.error(f"✗ Failed to read resource: {e}")
                
                # Test 3: List available tools
                logger.info("\n=== Testing Tools ===")
                tools = await session.list_tools()
                logger.info(f"Available tools: {len(tools)}")
                for tool in tools:
                    logger.info(f"  - {tool.name}: {tool.description}")
                
                # Test 4: Test script validation tool
                logger.info("\n=== Testing validate_script tool ===")
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
                
                try:
                    result = await session.call_tool("validate_script", {
                        "content": test_script,
                        "script_type": "item"
                    })
                    logger.info(f"✓ Script validation result: {result}")
                except Exception as e:
                    logger.error(f"✗ Script validation failed: {e}")
                
                # Test 5: Test search tool
                logger.info("\n=== Testing search_vanilla tool ===")
                try:
                    result = await session.call_tool("search_vanilla", {
                        "query": "apple",
                        "script_type": "item"
                    })
                    logger.info(f"✓ Search result: {result}")
                except Exception as e:
                    logger.error(f"✗ Search failed: {e}")
                
                # Test 6: Test reference checking
                logger.info("\n=== Testing check_references tool ===")
                try:
                    result = await session.call_tool("check_references", {
                        "references": ["Base.Apple", "Base.Hammer", "InvalidReference"],
                        "reference_type": "item"
                    })
                    logger.info(f"✓ Reference check result: {result}")
                except Exception as e:
                    logger.error(f"✗ Reference check failed: {e}")
                
                logger.info("\n✓ All MCP server tests completed!")
                
    except Exception as e:
        logger.error(f"✗ MCP server test failed: {e}")
    finally:
        # Clean up the server process
        server_process.terminate()
        server_process.wait()

async def test_individual_tools():
    """Test individual MCP tools without full client setup."""
    
    logger.info("\n=== Testing Individual Tools ===")
    
    # Import the MCP server tools directly for unit testing
    try:
        from mcp_server.mcp_server import (
            validate_script_tool,
            search_vanilla_tool, 
            check_references_tool,
            analyze_mod_tool
        )
        
        # Test script validation
        result = await validate_script_tool(
            "item Apple { Type = Food, Weight = 0.1 }",
            "item"
        )
        logger.info(f"Direct validation test: {result}")
        
        # Test reference checking
        result = await check_references_tool(
            ["Base.Apple", "Invalid.Reference"],
            "item"
        )
        logger.info(f"Direct reference check: {result}")
        
        # Test mod analysis on current directory
        result = await analyze_mod_tool(".")
        logger.info(f"Direct mod analysis: {result}")
        
    except ImportError as e:
        logger.error(f"Could not import MCP server tools: {e}")

def print_usage_examples():
    """Print usage examples for testing the MCP server."""
    
    print("""
=== MCP Server Testing Guide ===

1. **Run the MCP Server Directly:**
   poetry run python -m mcp_server.mcp_server

2. **Test with this script:**
   poetry run python test_mcp_server.py

3. **Manual Testing with MCP Inspector:**
   # Install MCP Inspector (if available)
   npm install -g @modelcontextprotocol/inspector
   
   # Run inspector pointing to our server
   mcp-inspector python -m mcp_server.mcp_server

4. **Test Individual Components:**
   # Test database initialization
   poetry run python -c "from mcp_server.core.database import create_db_and_tables; create_db_and_tables()"
   
   # Test CLI tools
   poetry run python mcp_server_cli.py ./media/scripts listitems

5. **Integration with Claude Desktop:**
   Add to Claude Desktop config:
   {
     "mcpServers": {
       "project-zomboid": {
         "command": "poetry",
         "args": ["run", "python", "-m", "mcp_server.mcp_server"],
         "cwd": "/path/to/pzmcp"
       }
     }
   }

6. **Available MCP Tools to test:**
   - validate_script: Validate Project Zomboid script syntax
   - generate_script: Generate scripts from templates  
   - search_vanilla: Search vanilla game data
   - check_references: Validate item/sound/sprite references
   - analyze_mod: Analyze mod directory structure

7. **Available MCP Resources:**
   - resource://vanilla_database: Parsed vanilla game data
   - resource://property_reference: Valid properties per script type
   - resource://modding_templates: Pre-built templates
   - resource://best_practices: Modding guidelines
""")

async def main():
    """Main test function."""
    print_usage_examples()
    
    # Test individual tools first
    await test_individual_tools()
    
    # Then test full MCP server (this requires the MCP client libraries)
    try:
        await test_mcp_server()
    except Exception as e:
        logger.error(f"Full MCP server test failed: {e}")
        logger.info("This is expected if MCP client libraries are not installed")
        logger.info("The individual tool tests above should work fine")

if __name__ == "__main__":
    asyncio.run(main())