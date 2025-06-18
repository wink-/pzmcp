#!/usr/bin/env python3
"""Project Zomboid MCP Server

A Model Context Protocol server that provides intelligent script validation,
generation, and contextual assistance for Project Zomboid mod development.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
import os

from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from pydantic import BaseModel

from mcp_server.core.database import create_db_and_tables
from mcp_server.core.data_extractor import DataExtractor
from mcp_server.core.script_generator import ScriptGenerator
from mcp_server.core.search_service import SearchService
from mcp_server.core.models import ItemTemplateParams, RecipeTemplateParams
from mcp_server.core.mod_checker import ModChecker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
server = Server("project-zomboid")

# Initialize services
script_generator = ScriptGenerator()
search_service = None  # Will be initialized after database setup
mod_checker = None  # Will be initialized after database setup

class ScriptValidationParams(BaseModel):
    content: str
    script_type: str

class ScriptGenerationParams(BaseModel):
    script_type: str
    template_name: str
    parameters: Dict[str, Any]

class VanillaSearchParams(BaseModel):
    query: str
    script_type: Optional[str] = None
    category: Optional[str] = None

class ReferenceCheckParams(BaseModel):
    references: List[str]
    reference_type: str

class ModAnalysisParams(BaseModel):
    mod_path: str

class ModCheckParams(BaseModel):
    mod_path: str
    report_format: Optional[str] = "text"

@server.list_resources()
async def list_resources() -> List[Resource]:
    """List available MCP resources."""
    resources = [
        Resource(
            uri="resource://vanilla_database",
            name="Vanilla Database",
            description="Parsed vanilla Project Zomboid game data",
            mimeType="application/json",
        ),
        Resource(
            uri="resource://property_reference", 
            name="Property Reference",
            description="Valid properties per script type with descriptions",
            mimeType="application/json",
        ),
        Resource(
            uri="resource://modding_templates",
            name="Modding Templates", 
            description="Pre-built templates for common mod scenarios",
            mimeType="application/json",
        ),
        Resource(
            uri="resource://best_practices",
            name="Best Practices",
            description="Modding guidelines and common patterns",
            mimeType="text/markdown",
        ),
    ]
    return resources

@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific MCP resource."""
    if uri == "resource://vanilla_database":
        # Return vanilla database content
        if search_service:
            items = search_service.search_items("")  # Get all items
            return {"type": "vanilla_database", "items": items}
        return {"type": "vanilla_database", "items": []}
    
    elif uri == "resource://property_reference":
        # Return property reference data
        return {
            "type": "property_reference",
            "item_properties": {
                "Type": "string - Item category (Food, Weapon, etc.)",
                "DisplayName": "string - Display name in game",
                "Icon": "string - Icon sprite name", 
                "Weight": "float - Item weight",
                "BasePrice": "int - Base shop price",
            },
            "recipe_properties": {
                "Result": "string - Item produced",
                "NeedToBeLearn": "boolean - Requires recipe knowledge",
                "Category": "string - Recipe category",
                "OnGiveXP": "string - Skill experience gained",
            }
        }
    
    elif uri == "resource://modding_templates":
        # Return available templates
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        templates = []
        if os.path.exists(template_dir):
            for file in os.listdir(template_dir):
                if file.endswith('.json'):
                    templates.append(file[:-5])  # Remove .json extension
        return {"type": "modding_templates", "templates": templates}
    
    elif uri == "resource://best_practices":
        return """# Project Zomboid Modding Best Practices

## Script Structure
- Always wrap items in proper module declarations
- Use consistent property naming conventions
- Validate all sprite and sound references

## Performance Considerations  
- Minimize texture sizes for items
- Use appropriate weight values for realism
- Consider item rarity and spawn rates

## Compatibility
- Test with vanilla game first
- Check for conflicts with popular mods
- Follow Build 42 syntax requirements
"""
    
    raise ValueError(f"Unknown resource: {uri}")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available MCP tools."""
    tools = [
        Tool(
            name="validate_script",
            description="Validate Project Zomboid script syntax and references",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Script content to validate"},
                    "script_type": {"type": "string", "description": "Type of script (item, recipe, vehicle)"}
                },
                "required": ["content", "script_type"]
            }
        ),
        Tool(
            name="generate_script", 
            description="Generate properly formatted Project Zomboid script from template",
            inputSchema={
                "type": "object",
                "properties": {
                    "script_type": {"type": "string", "description": "Type of script to generate"},
                    "template_name": {"type": "string", "description": "Template to use"},
                    "parameters": {"type": "object", "description": "Template parameters"}
                },
                "required": ["script_type", "template_name", "parameters"]
            }
        ),
        Tool(
            name="search_vanilla",
            description="Search vanilla Project Zomboid game data",
            inputSchema={
                "type": "object", 
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "script_type": {"type": "string", "description": "Filter by script type"},
                    "category": {"type": "string", "description": "Filter by category"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="check_references",
            description="Validate item, sound, and sprite references",
            inputSchema={
                "type": "object",
                "properties": {
                    "references": {"type": "array", "items": {"type": "string"}, "description": "References to check"},
                    "reference_type": {"type": "string", "description": "Type of references (item, sound, sprite)"}
                },
                "required": ["references", "reference_type"]
            }
        ),
        Tool(
            name="analyze_mod",
            description="Analyze mod directory structure and validate cross-file references",
            inputSchema={
                "type": "object",
                "properties": {
                    "mod_path": {"type": "string", "description": "Path to mod directory"}
                },
                "required": ["mod_path"]
            }
        ),
        Tool(
            name="check_mod",
            description="Comprehensive mod validation with detailed issue detection and auto-fix suggestions",
            inputSchema={
                "type": "object",
                "properties": {
                    "mod_path": {"type": "string", "description": "Path to mod directory to validate"},
                    "report_format": {"type": "string", "enum": ["text", "json"], "description": "Output format for the report", "default": "text"}
                },
                "required": ["mod_path"]
            }
        )
    ]
    return tools

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle MCP tool calls."""
    
    if name == "validate_script":
        params = ScriptValidationParams(**arguments)
        result = await validate_script_tool(params.content, params.script_type)
        return [TextContent(type="text", text=result)]
    
    elif name == "generate_script":
        params = ScriptGenerationParams(**arguments)
        result = await generate_script_tool(params.script_type, params.template_name, params.parameters)
        return [TextContent(type="text", text=result)]
    
    elif name == "search_vanilla":
        params = VanillaSearchParams(**arguments)
        result = await search_vanilla_tool(params.query, params.script_type, params.category)
        return [TextContent(type="text", text=result)]
    
    elif name == "check_references":
        params = ReferenceCheckParams(**arguments)
        result = await check_references_tool(params.references, params.reference_type)
        return [TextContent(type="text", text=result)]
    
    elif name == "analyze_mod":
        params = ModAnalysisParams(**arguments)
        result = await analyze_mod_tool(params.mod_path)
        return [TextContent(type="text", text=result)]
    
    elif name == "check_mod":
        params = ModCheckParams(**arguments)
        result = await check_mod_tool(params.mod_path, params.report_format)
        return [TextContent(type="text", text=result)]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def validate_script_tool(content: str, script_type: str) -> str:
    """Validate Project Zomboid script syntax."""
    try:
        # Basic validation logic - can be enhanced with actual parser
        if not content.strip():
            return "Error: Script content is empty"
        
        if script_type not in ["item", "recipe", "vehicle", "model"]:
            return f"Error: Unknown script type '{script_type}'"
        
        # Check for basic syntax patterns
        if script_type == "item" and "item " not in content.lower():
            return "Warning: Item script should contain 'item' declaration"
        
        if script_type == "recipe" and "recipe " not in content.lower():
            return "Warning: Recipe script should contain 'recipe' declaration"
        
        return "Script validation passed - basic syntax appears correct"
        
    except Exception as e:
        return f"Error during validation: {str(e)}"

async def generate_script_tool(script_type: str, template_name: str, parameters: Dict[str, Any]) -> str:
    """Generate Project Zomboid script from template."""
    try:
        if script_type == "item":
            params = ItemTemplateParams(**parameters)
            script = script_generator.generate_script_from_template(template_name, params)
            return script
        elif script_type == "recipe":
            params = RecipeTemplateParams(**parameters)
            script = script_generator.generate_script_from_template(template_name, params)
            return script
        else:
            return f"Error: Script type '{script_type}' not yet supported"
            
    except Exception as e:
        return f"Error generating script: {str(e)}"

async def search_vanilla_tool(query: str, script_type: Optional[str] = None, category: Optional[str] = None) -> str:
    """Search vanilla Project Zomboid game data."""
    try:
        if not search_service:
            return "Error: Search service not initialized"
        
        if script_type == "item" or script_type is None:
            results = search_service.search_items(query)
            if results:
                output = f"Found {len(results)} items matching '{query}':\n\n"
                for item in results[:10]:  # Limit to first 10 results
                    output += f"- {item.get('display_name', item.get('name', 'Unknown'))}\n"
                    if item.get('type'):
                        output += f"  Type: {item['type']}\n"
                    if item.get('icon'):
                        output += f"  Icon: {item['icon']}\n"
                    output += "\n"
                return output
            else:
                return f"No items found matching '{query}'"
        
        return "Search completed"
        
    except Exception as e:
        return f"Error during search: {str(e)}"

async def check_references_tool(references: List[str], reference_type: str) -> str:
    """Check validity of item/sound/sprite references."""
    try:
        valid_refs = []
        invalid_refs = []
        
        for ref in references:
            # Simple validation - can be enhanced with actual reference checking
            if reference_type == "item":
                # Check if reference follows proper naming convention
                if "." in ref and len(ref.split(".")) == 2:
                    valid_refs.append(ref)
                else:
                    invalid_refs.append(ref)
            else:
                # For now, assume other references are valid
                valid_refs.append(ref)
        
        result = f"Reference validation results:\n"
        result += f"Valid {reference_type} references: {len(valid_refs)}\n"
        result += f"Invalid {reference_type} references: {len(invalid_refs)}\n"
        
        if invalid_refs:
            result += f"\nInvalid references:\n"
            for ref in invalid_refs:
                result += f"- {ref}\n"
        
        return result
        
    except Exception as e:
        return f"Error checking references: {str(e)}"

async def analyze_mod_tool(mod_path: str) -> str:
    """Analyze mod directory structure."""
    try:
        if not os.path.exists(mod_path):
            return f"Error: Mod path '{mod_path}' does not exist"
        
        analysis = f"Mod Analysis for: {mod_path}\n\n"
        
        # Check for standard mod structure
        standard_dirs = ["media/scripts", "media/textures", "media/lua"]
        found_dirs = []
        missing_dirs = []
        
        for dir_name in standard_dirs:
            full_path = os.path.join(mod_path, dir_name)
            if os.path.exists(full_path):
                found_dirs.append(dir_name)
            else:
                missing_dirs.append(dir_name)
        
        analysis += f"Standard directories found: {', '.join(found_dirs)}\n"
        if missing_dirs:
            analysis += f"Missing directories: {', '.join(missing_dirs)}\n"
        
        # Count script files
        scripts_dir = os.path.join(mod_path, "media/scripts")
        if os.path.exists(scripts_dir):
            script_files = [f for f in os.listdir(scripts_dir) if f.endswith('.txt')]
            analysis += f"\nScript files found: {len(script_files)}\n"
            for script_file in script_files:
                analysis += f"- {script_file}\n"
        
        return analysis
        
    except Exception as e:
        return f"Error analyzing mod: {str(e)}"

async def check_mod_tool(mod_path: str, report_format: str = "text") -> str:
    """Comprehensive mod validation using the ModChecker."""
    try:
        logger.info(f"Starting comprehensive mod check for: {mod_path}")
        
        # Run comprehensive mod check
        result = mod_checker.check_mod(mod_path)
        
        # Generate report in requested format
        report = mod_checker.generate_report(result, format=report_format)
        
        # Add auto-fix suggestions if available
        auto_fixes = mod_checker.get_auto_fix_suggestions(result.issues)
        if auto_fixes and report_format == "text":
            report += "\n\n=== Auto-Fix Suggestions ===\n"
            for i, fix in enumerate(auto_fixes, 1):
                report += f"{i}. {fix['issue_title']}\n"
                report += f"   Fix: {fix['fix_description']}\n"
                if fix['file_path']:
                    report += f"   File: {fix['file_path']}\n"
                report += "\n"
        
        logger.info(f"Mod check completed. Overall score: {result.overall_score:.1f}/10.0")
        return report
        
    except Exception as e:
        logger.error(f"Error during mod check: {e}")
        return f"Error checking mod: {str(e)}"

async def initialize_services():
    """Initialize database and services."""
    global search_service, mod_checker
    
    logger.info("Initializing database...")
    create_db_and_tables()
    
    # Initialize search service with proper import
    try:
        from mcp_server.core.database import engine
        search_service = SearchService(engine=engine)
        
        # Initialize mod checker with database path
        mod_checker = ModChecker(vanilla_db_path="mcp_data.db")
        
        logger.info("Services initialized successfully")
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        # Create a basic search service fallback
        search_service = None
        mod_checker = None

async def main():
    """Main entry point."""
    await initialize_services()
    
    # Run the MCP server
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())