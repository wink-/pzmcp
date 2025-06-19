# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Project Zomboid MCP (Model Context Protocol) Server - a Python-based application that provides intelligent script validation, generation, and contextual assistance for Project Zomboid mod development. The project uses FastAPI to implement MCP server functionality with SQLite FTS5 for full-text search capabilities.

## Development Commands

**Setup Commands:**
```bash
# Setup and install dependencies
uv sync

# Extract Project Zomboid data from repository scripts (first time setup or after updating scripts)
uv run python -c "from mcp_server.core.enhanced_data_extractor import extract_vanilla_data; extract_vanilla_data(comprehensive=True)"

# Run tests
uv run pytest

# Run tests with coverage
uv run coverage run -m pytest && uv run coverage report

# Test the modern server specifically
uv run pytest tests/test_modern_server.py -v

# Test with MCP development tools
mcp dev mcp_server/modern_server.py
```

**Running the Server (Multiple Options):**

### Option 1: Modern FastMCP Server (Recommended)
```bash
# Modern server with FastMCP
uv run python run_modern_server.py

# Or using mcp CLI tools
mcp dev mcp_server/modern_server.py
mcp install mcp_server/modern_server.py
```
**Claude Desktop Config:** Use `claude_desktop_config_modern.json`

### Option 2: WSL-based MCP Server (Legacy)
```bash
# In WSL
uv run python run_server.py
```
**Claude Desktop Config:** Use `claude_desktop_config_wsl.json`

### Option 3: Native Windows MCP Server (Legacy)
```cmd
# Windows Command Prompt/PowerShell
.\start_mcp_native.bat
```
**Claude Desktop Config:** Use `claude_desktop_config_native_windows.json`

### Option 4: FastAPI HTTP Server (For broader compatibility)
```cmd
# Windows - HTTP API on localhost:8000
.\start_http_server.bat

# Or direct command
uv run uvicorn mcp_server.main:app --reload --host 0.0.0.0 --port 8000
```
**Access:** http://localhost:8000 (API docs: http://localhost:8000/docs)

### Option 5: Docker HTTP Server (Containerized)
```cmd
# Windows - Docker container with HTTP API
.\start_mcp_server.bat

# Or direct docker-compose
docker-compose up --build
```
**Access:** http://localhost:8000 (API docs: http://localhost:8000/docs)

**Legacy/Alternative Commands:**
```bash
# Direct Python (if uv not available)
python run_server.py

# FastAPI server (for testing/development)
uv run uvicorn mcp_server.main:app --reload

# CLI tools
uv run python mcp_server_cli.py ./media/scripts listitems
uv run python mcp_server_cli.py ./media/scripts getitem Base.Apple
```

**MCP Server Tools:**
- `validate_script` - Validate Project Zomboid script syntax with intelligent error detection
- `generate_script` - Generate scripts from templates with parameter validation
- `search_vanilla` - Search vanilla game data with fuzzy matching and auto-completion
- `check_references` - Validate item/sound/sprite references against database
- `analyze_mod` - Comprehensive mod analysis with performance recommendations

**Modern Server Features (FastMCP):**
- **Resources**: Live game data access, property references, best practices
- **Prompts**: Guided workflows for item creation, script fixing, mod optimization
- **Auto-completion**: Intelligent suggestions for item names, script types, properties
- **Progress tracking**: Real-time feedback during long operations
- **Error handling**: Comprehensive validation with helpful suggestions
- **Lifespan management**: Automatic database initialization and cleanup

**Testing/Development endpoints:**
```bash
# FastAPI server endpoints (when running uvicorn server)
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

# Development Guidelines

This document contains critical information about working with this codebase. Follow these guidelines precisely.

## Core Development Rules

1. Package Management
   - ONLY use uv, NEVER pip
   - Installation: `uv add package`
   - Running tools: `uv run tool`
   - Upgrading: `uv add --dev package --upgrade-package package`
   - FORBIDDEN: `uv pip install`, `@latest` syntax

2. Code Quality
   - Type hints required for all code
   - Public APIs must have docstrings
   - Functions must be focused and small
   - Follow existing patterns exactly
   - Line length: 88 chars maximum

3. Testing Requirements
   - Framework: `uv run --frozen pytest`
   - Async testing: use anyio, not asyncio
   - Coverage: test edge cases and errors
   - New features require tests
   - Bug fixes require regression tests

- For commits fixing bugs or adding features based on user reports add:
  ```bash
  git commit --trailer "Reported-by:<name>"
  ```
  Where `<name>` is the name of the user.

- For commits related to a Github issue, add
  ```bash
  git commit --trailer "Github-Issue:#<number>"
  ```
- NEVER ever mention a `co-authored-by` or similar aspects. In particular, never
  mention the tool used to create the commit message or PR.

## Pull Requests

- Create a detailed message of what changed. Focus on the high level description of
  the problem it tries to solve, and how it is solved. Don't go into the specifics of the
  code unless it adds clarity.

- Always add `jerome3o-anthropic` and `jspahrsummers` as reviewer.

- NEVER ever mention a `co-authored-by` or similar aspects. In particular, never
  mention the tool used to create the commit message or PR.

## Python Tools

## Code Formatting

1. Ruff
   - Format: `uv run --frozen ruff format .`
   - Check: `uv run --frozen ruff check .`
   - Fix: `uv run --frozen ruff check . --fix`
   - Critical issues:
     - Line length (88 chars)
     - Import sorting (I001)
     - Unused imports
   - Line wrapping:
     - Strings: use parentheses
     - Function calls: multi-line with proper indent
     - Imports: split into multiple lines

2. Type Checking
   - Tool: `uv run --frozen pyright`
   - Requirements:
     - Explicit None checks for Optional
     - Type narrowing for strings
     - Version warnings can be ignored if checks pass

3. Pre-commit
   - Config: `.pre-commit-config.yaml`
   - Runs: on git commit
   - Tools: Prettier (YAML/JSON), Ruff (Python)
   - Ruff updates:
     - Check PyPI versions
     - Update config rev
     - Commit config first

## Error Resolution

1. CI Failures
   - Fix order:
     1. Formatting
     2. Type errors
     3. Linting
   - Type errors:
     - Get full line context
     - Check Optional types
     - Add type narrowing
     - Verify function signatures

2. Common Issues
   - Line length:
     - Break strings with parentheses
     - Multi-line function calls
     - Split imports
   - Types:
     - Add None checks
     - Narrow string types
     - Match existing patterns
   - Pytest:
     - If the tests aren't finding the anyio pytest mark, try adding PYTEST_DISABLE_PLUGIN_AUTOLOAD=""
       to the start of the pytest run command eg:
       `PYTEST_DISABLE_PLUGIN_AUTOLOAD="" uv run --frozen pytest`

3. Best Practices
   - Check git status before commits
   - Run formatters before type checks
   - Keep changes minimal
   - Follow existing patterns
   - Document public APIs
   - Test thoroughly