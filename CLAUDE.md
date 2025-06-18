# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Project Zomboid MCP (Model Context Protocol) Server - a Python-based application that provides intelligent script validation, generation, and contextual assistance for Project Zomboid mod development. The project uses FastAPI to implement MCP server functionality with SQLite FTS5 for full-text search capabilities.

## Development Commands

**Using uv (Recommended - Cross-platform):**
```bash
# Install dependencies (run from project root)
uv sync

# Run tests
uv run pytest

# Run MCP server (Model Context Protocol)
uv run python run_server.py

# Run legacy FastAPI server (for testing)  
uv run uvicorn mcp_server.main:app --reload

# CLI usage
uv run python mcp_server_cli.py ./media/scripts listitems
uv run python mcp_server_cli.py ./media/scripts getitem Base.Apple

# Extract and populate database with Project Zomboid data
uv run python -c "from mcp_server.core.enhanced_data_extractor import extract_with_path_manager; extract_with_path_manager(comprehensive=True)"
```

**Alternative - Using Python directly:**
```bash
# Install dependencies
python install_dependencies.py

# Test the server
python simple_test.py

# Run MCP server
python run_server.py

# Windows batch file
run_server.bat
```

**MCP Server Tools:**
- `validate_script` - Validate Project Zomboid script syntax
- `generate_script` - Generate scripts from templates
- `search_vanilla` - Search vanilla game data
- `check_references` - Validate item/sound/sprite references
- `analyze_mod` - Analyze mod directory structure

**Legacy FastAPI endpoints:**
```bash
curl http://localhost:8000/extract-vanilla-data
curl "http://localhost:8000/search/items?q=apple"
```

## Architecture

The codebase follows a layered architecture with these key components:

**Root Level:**
- `script_parser.py` - Custom recursive descent parser for Project Zomboid script syntax
- `data_models.py` - Pydantic models for game entities (Items, Recipes, Vehicles)
- `data_transformer.py` - Converts parsed data into model instances
- `data_repository.py` - In-memory data management with querying capabilities

**MCP Server (`/mcp_server/`):**
- `main.py` - FastAPI application with MCP protocol endpoints
- `core/database.py` - SQLAlchemy setup with FTS5 full-text search
- `core/script_generator.py` - Template-based script generation system
- `parsers/` - Specialized parsers for different script types
- `templates/` - JSON templates for generating new scripts

**Data Flow:**
1. Parse Project Zomboid scripts with custom lexer/tokenizer
2. Transform into Pydantic models with validation
3. Store in SQLite database with FTS5 indexing
4. Expose via FastAPI endpoints and CLI tools

## Key Patterns

**Parser Architecture:** Custom recursive descent parser handles Project Zomboid's unique script syntax variations and nested structures.

**Repository Pattern:** Centralized data access through `data_repository.py` provides both in-memory and persistent storage options.

**Template System:** JSON-based templates in `/templates/` drive script generation with parameter substitution.

**Full-Text Search:** SQLite FTS5 enables intelligent content discovery across all game data.

## Project Zomboid Script Syntax

The parser handles PZ-specific syntax including:
- Module declarations and imports
- Item definitions with nested properties
- Recipe structures with ingredients/results
- Vehicle configurations with complex hierarchies
- Special syntax for attachments, evolving recipes, and sound events

## Testing

Comprehensive test suite covers parser functionality, data transformation, and API endpoints. Run with `uv run pytest` for full test execution.