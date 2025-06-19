#!/usr/bin/env python3
"""Modern Project Zomboid MCP Server using FastMCP

A modernized Model Context Protocol server that provides intelligent script validation,
generation, and contextual assistance for Project Zomboid mod development.

This server uses the FastMCP framework for simplified development and enhanced features.
"""

import asyncio
import json
import logging
import os
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import BaseModel, Field

from mcp_server.core.database import create_db_and_tables, engine
from mcp_server.core.enhanced_data_extractor import extract_vanilla_data
from mcp_server.core.mod_checker import ModChecker
from mcp_server.core.models import ItemTemplateParams, RecipeTemplateParams
from mcp_server.core.script_generator import ScriptGenerator
from mcp_server.core.search_service import SearchService

# Configure logging to stderr only (FastMCP handles stdout)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)


@dataclass
class ServerContext:
    """Application context for the MCP server."""
    search_service: SearchService
    script_generator: ScriptGenerator
    mod_checker: ModChecker


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[ServerContext]:
    """Manage server startup and shutdown lifecycle."""
    logger.info("Initializing Project Zomboid MCP Server...")

    # Initialize database
    create_db_and_tables()

    # Initialize services
    search_service = SearchService(engine=engine)
    script_generator = ScriptGenerator()
    mod_checker = ModChecker(vanilla_db_path="mcp_data.db")

    # Check if database needs population
    try:
        test_results = search_service.search_items("hammer")
        if len(test_results) == 0:
            logger.info("Database appears empty, extracting vanilla data...")
            extract_vanilla_data(comprehensive=True)
            logger.info("Vanilla data extraction completed")
    except Exception as e:
        logger.warning(f"Could not check database status: {e}")

    context = ServerContext(
        search_service=search_service,
        script_generator=script_generator,
        mod_checker=mod_checker
    )

    logger.info("Project Zomboid MCP Server initialized successfully")

    try:
        yield context
    finally:
        logger.info("Shutting down Project Zomboid MCP Server...")


# Create the FastMCP server with lifespan management
mcp = FastMCP(
    "Project Zomboid",
    lifespan=server_lifespan,
    dependencies=["pydantic>=2.0.0", "sqlalchemy>=2.0.0", "rich>=13.0.0"]
)


# Pydantic models for tool parameters
class ScriptValidationRequest(BaseModel):
    """Request model for script validation."""
    content: str = Field(description="Script content to validate")
    script_type: str = Field(description="Type of script (item, recipe, vehicle)")


class ScriptGenerationRequest(BaseModel):
    """Request model for script generation."""
    script_type: str = Field(description="Type of script to generate")
    template_name: str = Field(description="Template to use")
    parameters: dict[str, Any] = Field(description="Template parameters")


class ModAnalysisRequest(BaseModel):
    """Request model for mod analysis."""
    mod_path: str = Field(description="Path to mod directory")
    report_format: str | None = Field(default="text", description="Report format (text or json)")


class ReferenceCheckRequest(BaseModel):
    """Request model for reference validation."""
    references: list[str] = Field(description="References to validate")
    reference_type: str = Field(description="Type of references (item, sound, sprite)")


# Resources - Expose Project Zomboid data and configuration
@mcp.resource("pz://vanilla_database")
def get_vanilla_database() -> str:
    """Get vanilla Project Zomboid game data from the database."""
    context = mcp.get_context()
    app_context = context.request_context.lifespan_context

    # Get a sample of items to return
    items = app_context.search_service.search_items("")

    return json.dumps({
        "type": "vanilla_database",
        "total_items": len(items),
        "sample_items": items[:10] if items else [],
        "message": "Use search_vanilla tool to find specific items"
    })


@mcp.resource("pz://property_reference")
def get_property_reference() -> str:
    """Get reference documentation for Project Zomboid script properties."""
    return json.dumps({
        "type": "property_reference",
        "item_properties": {
            "Type": "string - Item category (Food, Weapon, etc.)",
            "DisplayName": "string - Display name in game",
            "Icon": "string - Icon sprite name",
            "Weight": "float - Item weight",
            "BasePrice": "int - Base shop price",
            "Categories": "string - Weapon/tool categories",
            "ConditionMax": "int - Maximum condition/durability",
            "MinDamage": "float - Minimum damage dealt",
            "MaxDamage": "float - Maximum damage dealt",
            "CriticalChance": "int - Critical hit chance percentage",
            "AttachmentType": "string - What can be attached to this item"
        },
        "recipe_properties": {
            "Result": "string - Item produced by recipe",
            "NeedToBeLearn": "boolean - Requires recipe knowledge",
            "Category": "string - Recipe category for UI",
            "OnGiveXP": "string - Skill experience gained",
            "Time": "float - Time required to craft",
            "Sound": "string - Sound played during crafting"
        },
        "vehicle_properties": {
            "template": "string - Base vehicle template to inherit from",
            "skin": "string - Vehicle skin/appearance",
            "script": "string - Vehicle script for behavior"
        }
    })


@mcp.resource("pz://templates/available")
def get_available_templates() -> str:
    """Get list of available script templates."""
    context = mcp.get_context()
    app_context = context.request_context.lifespan_context

    template_dir = Path(__file__).parent / "templates"
    templates = []

    if template_dir.exists():
        for file in template_dir.glob("*.json"):
            templates.append(file.stem)

    return json.dumps({
        "type": "available_templates",
        "templates": templates,
        "template_directory": str(template_dir)
    })


@mcp.resource("pz://best_practices")
def get_best_practices() -> str:
    """Get Project Zomboid modding best practices and guidelines."""
    return """# Project Zomboid Modding Best Practices

## Script Structure
- Always wrap items in proper module declarations
- Use consistent property naming conventions (PascalCase for most properties)
- Validate all sprite and sound references exist
- Include proper DisplayName for all user-facing items

## Performance Considerations  
- Minimize texture sizes for items (prefer 64x64 or smaller for most items)
- Use appropriate weight values for realism (0.1-10.0 for most items)
- Consider item rarity and spawn rates when setting BasePrice
- Avoid excessive ConditionMax values (1-15 is typical range)

## Item Design Guidelines
- Weapons: Set appropriate MinDamage/MaxDamage ranges
- Tools: Include proper AttachmentType for multi-tools
- Food: Set appropriate hunger reduction and cooking requirements
- Clothing: Include proper BodyLocation and protection values

## Recipe Best Practices
- Always specify realistic Time values (50-500 for most recipes)
- Use existing vanilla items as ingredients when possible
- Set appropriate skill requirements and XP rewards
- Include proper Category for UI organization

## Compatibility
- Test with vanilla game first before adding complex mods
- Check for conflicts with popular mods like Hydrocraft
- Follow Build 42+ syntax requirements for future compatibility
- Use semantic versioning for mod releases

## Common Pitfalls to Avoid
- Missing semicolons at end of property lines
- Incorrect capitalization in property names
- Referencing non-existent sprites or sounds
- Unbalanced weapon damage or tool durability
- Missing module declarations
"""


# Tools - Provide functionality for mod development
@mcp.tool()
async def validate_script(request: ScriptValidationRequest, ctx: Context) -> str:
    """Validate Project Zomboid script syntax and check for common issues."""
    ctx.info(f"Validating {request.script_type} script...")

    try:
        if not request.content.strip():
            return "❌ Error: Script content is empty"

        if request.script_type not in ["item", "recipe", "vehicle", "model"]:
            return f"❌ Error: Unknown script type '{request.script_type}'"

        # Basic syntax validation
        issues = []
        lines = request.content.split('\n')

        # Check for module declaration
        has_module = any('module ' in line.lower() for line in lines[:5])
        if not has_module:
            issues.append("⚠️  Warning: No module declaration found in first 5 lines")

        # Check for proper script type declaration
        script_keyword = request.script_type.lower()
        if script_keyword == "item":
            # Look for actual item declarations, not just comments containing "item"
            has_item_declaration = any(
                'item ' in line.lower() and not line.strip().startswith('//')
                for line in lines
            )
            if not has_item_declaration:
                issues.append(f"⚠️  Warning: No '{script_keyword}' declaration found")
        elif script_keyword == "recipe":
            # Look for actual recipe declarations, not just comments containing "recipe"
            has_recipe_declaration = any(
                'recipe ' in line.lower() and not line.strip().startswith('//')
                for line in lines
            )
            if not has_recipe_declaration:
                issues.append(f"⚠️  Warning: No '{script_keyword}' declaration found")

        # Check for common syntax issues
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('//'):
                continue

            # Check for missing semicolons on property lines
            if '=' in line and not line.endswith(',') and not line.endswith('{') and not line.endswith('}'):
                if not line.endswith(','):
                    issues.append(f"⚠️  Line {i}: Missing comma after property assignment")

        if issues:
            result = "✅ Script validation completed with issues:\n\n"
            result += "\n".join(issues)
        else:
            result = "✅ Script validation passed - syntax appears correct"

        await ctx.report_progress(1, 1)
        return result

    except Exception as e:
        return f"❌ Error during validation: {e!s}"


@mcp.tool()
async def generate_script(request: ScriptGenerationRequest, ctx: Context) -> str:
    """Generate a properly formatted Project Zomboid script from template."""
    ctx.info(f"Generating {request.script_type} script using template '{request.template_name}'...")

    try:
        app_context = ctx.request_context.lifespan_context

        if request.script_type == "item":
            params = ItemTemplateParams(**request.parameters)
            script = app_context.script_generator.generate_script_from_template(
                request.template_name, params
            )
            return f"✅ Item script generated successfully:\n\n```\n{script}\n```"

        elif request.script_type == "recipe":
            params = RecipeTemplateParams(**request.parameters)
            script = app_context.script_generator.generate_script_from_template(
                request.template_name, params
            )
            return f"✅ Recipe script generated successfully:\n\n```\n{script}\n```"

        else:
            return f"❌ Error: Script type '{request.script_type}' not yet supported for generation"

    except Exception as e:
        return f"❌ Error generating script: {e!s}"


@mcp.tool()
async def search_vanilla(query: str, script_type: str | None = None, category: str | None = None, ctx: Context | None = None) -> str:
    """Search vanilla Project Zomboid game data for items, weapons, tools, etc."""
    if ctx:
        ctx.info(f"Searching vanilla data for: '{query}'")

    try:
        app_context = mcp.get_context().request_context.lifespan_context

        if script_type == "item" or script_type is None:
            results = app_context.search_service.search_items(query)
            if results:
                output = f"🔍 Found {len(results)} items matching '{query}':\n\n"
                for item in results[:10]:  # Limit to first 10 results
                    name = item.get('item_name', 'Unknown')
                    display = item.get('display_name', 'No display name')
                    module = item.get('module_name', 'Unknown')
                    output += f"**{name}** - {display}\n"
                    output += f"  Module: {module}\n"

                    # Parse and display ALL properties
                    props_json = item.get('properties_json', '{}')
                    try:
                        props = json.loads(props_json)
                        if props:
                            output += f"  **Full Properties:**\n"
                            # Sort properties for consistent display
                            for key, value in sorted(props.items()):
                                output += f"    {key} = {value}\n"
                        else:
                            output += f"  No detailed properties available\n"
                    except Exception as e:
                        output += f"  Error parsing properties: {e}\n"

                    output += "\n"

                if len(results) > 10:
                    output += f"... and {len(results) - 10} more results\n"

                return output
            else:
                return f"❌ No items found matching '{query}'"

        return "✅ Search completed"

    except Exception as e:
        return f"❌ Error during search: {e!s}"


@mcp.tool()
async def check_references(request: ReferenceCheckRequest, ctx: Context) -> str:
    """Validate item, sound, and sprite references exist in the game data."""
    ctx.info(f"Checking {len(request.references)} {request.reference_type} references...")

    try:
        valid_refs = []
        invalid_refs = []

        app_context = ctx.request_context.lifespan_context

        for ref in request.references:
            await ctx.report_progress(len(valid_refs) + len(invalid_refs), len(request.references))

            if request.reference_type == "item":
                # Check if item exists in database
                results = app_context.search_service.search_items(ref)
                exact_match = any(item.get('item_name') == ref for item in results)
                if exact_match:
                    valid_refs.append(ref)
                else:
                    invalid_refs.append(ref)
            else:
                # For non-item references, do basic validation
                if '.' in ref and len(ref.split('.')) >= 2:
                    valid_refs.append(ref)
                else:
                    invalid_refs.append(ref)

        result = "🔍 Reference validation results:\n\n"
        result += f"✅ Valid {request.reference_type} references: {len(valid_refs)}\n"
        result += f"❌ Invalid {request.reference_type} references: {len(invalid_refs)}\n"

        if invalid_refs:
            result += "\n**Invalid references:**\n"
            for ref in invalid_refs:
                result += f"- {ref}\n"

        if valid_refs and len(valid_refs) <= 10:
            result += "\n**Valid references:**\n"
            for ref in valid_refs:
                result += f"- {ref}\n"

        return result

    except Exception as e:
        return f"❌ Error checking references: {e!s}"


@mcp.tool()
async def analyze_mod(request: ModAnalysisRequest, ctx: Context) -> str:
    """Perform comprehensive analysis of a Project Zomboid mod directory."""
    ctx.info(f"Analyzing mod at: {request.mod_path}")

    try:
        if not os.path.exists(request.mod_path):
            return f"❌ Error: Mod path '{request.mod_path}' does not exist"

        app_context = ctx.request_context.lifespan_context

        # Run comprehensive mod check
        result = app_context.mod_checker.check_mod(request.mod_path)

        # Generate report in requested format
        report = app_context.mod_checker.generate_report(result, format=request.report_format)

        # Add auto-fix suggestions if available
        auto_fixes = app_context.mod_checker.get_auto_fix_suggestions(result.issues)
        if auto_fixes and request.report_format == "text":
            report += "\n\n## 🔧 Auto-Fix Suggestions\n"
            for i, fix in enumerate(auto_fixes, 1):
                report += f"\n{i}. **{fix['issue_title']}**\n"
                report += f"   Fix: {fix['fix_description']}\n"
                if fix['file_path']:
                    report += f"   File: {fix['file_path']}\n"

        ctx.info(f"Mod analysis completed. Score: {result.overall_score:.1f}/10.0")
        return report

    except Exception as e:
        return f"❌ Error analyzing mod: {e!s}"


# Prompts - Provide templates for common Project Zomboid workflows
@mcp.prompt()
def create_item_prompt(item_name: str, item_type: str = "Weapon") -> list[base.Message]:
    """Create a guided prompt for creating a new Project Zomboid item."""
    return [
        base.UserMessage(f"I want to create a new {item_type.lower()} called '{item_name}' for Project Zomboid."),
        base.UserMessage("Please help me by:"),
        base.UserMessage("1. Searching for similar vanilla items for reference"),
        base.UserMessage("2. Suggesting appropriate properties for this item type"),
        base.UserMessage("3. Generating a complete item script"),
        base.UserMessage("4. Validating the script for common issues"),
        base.UserMessage("Let's start by searching for similar items in the vanilla game data."),
    ]


@mcp.prompt()
def fix_script_prompt(script_content: str, error_message: str = "") -> list[base.Message]:
    """Create a prompt for fixing Project Zomboid script issues."""
    messages = [
        base.UserMessage("I have a Project Zomboid script that has issues and needs to be fixed."),
        base.UserMessage(f"Here's the script:\n\n```\n{script_content}\n```"),
    ]

    if error_message:
        messages.append(base.UserMessage(f"Error message: {error_message}"))

    messages.extend([
        base.UserMessage("Please help me:"),
        base.UserMessage("1. Validate the script and identify all issues"),
        base.UserMessage("2. Explain what each issue means"),
        base.UserMessage("3. Provide a corrected version of the script"),
        base.UserMessage("4. Suggest improvements for better balance/realism"),
    ])

    return messages


@mcp.prompt()
def optimize_mod_prompt(mod_path: str) -> list[base.Message]:
    """Create a prompt for optimizing mod performance and compatibility."""
    return [
        base.UserMessage(f"I need help optimizing my Project Zomboid mod located at: {mod_path}"),
        base.UserMessage("Please analyze the mod and help me:"),
        base.UserMessage("1. Check for performance issues (large textures, excessive items, etc.)"),
        base.UserMessage("2. Validate all script syntax and references"),
        base.UserMessage("3. Suggest balance improvements for weapons/items"),
        base.UserMessage("4. Check compatibility with popular mods"),
        base.UserMessage("5. Provide specific recommendations for optimization"),
        base.UserMessage("Let's start with a comprehensive mod analysis."),
    ]


@mcp.prompt()
def recipe_creation_prompt(result_item: str, difficulty: str = "medium") -> list[base.Message]:
    """Create a guided prompt for recipe creation."""
    return [
        base.UserMessage(f"I want to create a recipe that produces '{result_item}' with {difficulty} difficulty."),
        base.UserMessage("Please guide me through:"),
        base.UserMessage("1. Finding appropriate ingredients from vanilla items"),
        base.UserMessage("2. Setting realistic crafting time and skill requirements"),
        base.UserMessage("3. Choosing the right recipe category and tools needed"),
        base.UserMessage("4. Generating the complete recipe script"),
        base.UserMessage("5. Testing the recipe balance against similar vanilla recipes"),
        base.UserMessage("Let's start by searching for the target item and similar recipes."),
    ]


@mcp.prompt()
def debug_mod_prompt(issue_description: str) -> str:
    """Create a debugging prompt for mod issues."""
    return f"""I'm experiencing issues with my Project Zomboid mod: {issue_description}

Please help me debug this by:
1. Analyzing potential causes of this issue
2. Suggesting diagnostic steps to identify the problem
3. Providing solutions for common mod issues
4. Recommending tools or techniques for further debugging

Let's start by gathering more information about the mod structure and any error messages."""


# Note: Auto-completion support requires MCP SDK version with completion types
# This will be added in a future update when the completion API is stabilized


# Main entry point
async def main() -> None:
    """Run the modern Project Zomboid MCP server."""
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        # Run HTTP server for testing
        mcp.run(transport="sse", host="0.0.0.0", port=8000)
    else:
        # Run stdio server (default for MCP clients)
        mcp.run()


if __name__ == "__main__":
    asyncio.run(main())
