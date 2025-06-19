# Modern Project Zomboid MCP Server Features

This document showcases the new features available in the modernized FastMCP-based Project Zomboid MCP server.

## 🚀 Quick Start

### Installation and Setup

```bash
# Install dependencies
uv sync

# Extract vanilla data (first time only)
uv run python -c "from mcp_server.core.enhanced_data_extractor import extract_vanilla_data; extract_vanilla_data(comprehensive=True)"

# Run the modern server
uv run python run_modern_server.py

# Or use MCP development tools
mcp dev mcp_server/modern_server.py
```

### Claude Desktop Integration

1. Copy `claude_desktop_config_modern.json` settings to Claude Desktop
2. Restart Claude Desktop
3. The server will appear as "Project Zomboid" in your available tools

## 🛠️ Enhanced Tools

### Smart Script Validation

The `validate_script` tool now provides intelligent error detection:

```python
# Example usage in Claude:
validate_script({
    "content": """module MyMod {
        item CustomSword {
            DisplayName = "Custom Sword",
            Type = Weapon,
            Weight = 2.0
        }
    }""",
    "script_type": "item"
})
```

**New Features:**
- ✅ Detects missing module declarations
- ✅ Validates script type consistency  
- ✅ Checks for common syntax errors (missing commas, etc.)
- ✅ Provides specific line-by-line feedback

### Enhanced Search with Auto-completion

The `search_vanilla` tool now includes:

```python
# Auto-completion for item names
search_vanilla("ham")  # Suggests: Hammer, Ham, Hamburger

# Fuzzy matching for better results
search_vanilla("claw hammer")  # Finds related tools
```

**New Features:**
- 🔍 Auto-completion starts after 2 characters
- 🎯 Fuzzy matching for partial names
- 📊 Rich result formatting with properties
- ⚡ Fast SQLite FTS5 search backend

### Intelligent Script Generation

Enhanced template system with validation:

```python
generate_script({
    "script_type": "item",
    "template_name": "basic_weapon",
    "parameters": {
        "name": "CustomAxe",
        "display_name": "Custom Axe",
        "weight": 3.5,
        "min_damage": 1.2,
        "max_damage": 2.8
    }
})
```

**New Features:**
- ✅ Parameter validation with Pydantic models
- 🎨 Template auto-completion
- 🔧 Generated scripts include proper formatting
- 📋 Validates against Project Zomboid syntax rules

## 📚 Resources

### Live Game Data Access

Access comprehensive Project Zomboid data:

```python
# Get vanilla database overview
read_resource("pz://vanilla_database")

# Get property reference guide
read_resource("pz://property_reference")

# Get modding best practices
read_resource("pz://best_practices")

# List available templates
read_resource("pz://templates/available")
```

### Resource Features

- 🔄 **Live Data**: Always up-to-date with your database
- 📖 **Documentation**: Built-in reference for all properties
- 🎯 **Best Practices**: Curated modding guidelines
- 📝 **Templates**: Available script templates

## 💬 Guided Prompts

### Item Creation Workflow

```python
# Get guided assistance for creating items
create_item_prompt("Katana", "Weapon")
```

**Generates:**
1. Search for similar vanilla items
2. Property recommendations
3. Complete script generation
4. Validation and error checking

### Script Fixing Assistant

```python
# Get help fixing broken scripts
fix_script_prompt(
    script_content="your broken script here",
    error_message="optional error details"
)
```

**Provides:**
1. Issue identification
2. Explanation of problems
3. Corrected script version
4. Balance and improvement suggestions

### Mod Optimization Guide

```python
# Get comprehensive mod analysis
optimize_mod_prompt("/path/to/your/mod")
```

**Analyzes:**
1. Performance bottlenecks
2. Script validation
3. Balance recommendations
4. Compatibility checks

## ⚡ Auto-completion

The modern server provides intelligent auto-completion for:

### Tool Parameters
- **search_vanilla**: Item name suggestions
- **generate_script**: Script types and template names
- **validate_script**: Script type options
- **check_references**: Reference type options

### Prompt Parameters
- **create_item_prompt**: Item type suggestions
- **recipe_creation_prompt**: Difficulty levels

### How It Works
- Completions start after 2 characters
- Uses actual database content for suggestions
- Filters results based on partial input
- Provides context-aware recommendations

## 🧪 Testing and Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Test specific components
uv run pytest tests/test_modern_server.py -v

# Run with coverage
uv run coverage run -m pytest && uv run coverage report
```

### Development Mode

```bash
# Use MCP Inspector for interactive testing
mcp dev mcp_server/modern_server.py

# Install in Claude Desktop for production use
mcp install mcp_server/modern_server.py
```

### Code Quality

```bash
# Format code
uv run ruff format .

# Check for issues
uv run ruff check .

# Type checking
uv run mypy mcp_server/

# Pre-commit hooks
uv run pre-commit run --all-files
```

## 🔧 Configuration

### Environment Variables

```bash
# Optional: Specify custom database path
export PZMCP_DB_PATH="/path/to/custom/database.db"

# Optional: Enable debug logging
export PZMCP_LOG_LEVEL="DEBUG"
```

### Server Options

```bash
# Run with HTTP transport for testing
uv run python run_modern_server.py --http

# Default stdio transport (for MCP clients)
uv run python run_modern_server.py
```

## 🆚 Legacy vs Modern Server

| Feature | Legacy Server | Modern Server |
|---------|---------------|---------------|
| Architecture | Manual protocol handling | FastMCP decorators |
| Resources | JSON strings | Structured data access |
| Tools | Basic functionality | Enhanced with progress tracking |
| Prompts | ❌ Not available | ✅ Guided workflows |
| Auto-completion | ❌ Not available | ✅ Intelligent suggestions |
| Error Handling | Basic messages | Comprehensive validation |
| Testing | Limited | Full test suite |
| Code Quality | Manual | Automated with pre-commit |

## 🔮 Future Enhancements

Planned features for upcoming releases:

- 🔐 **Authentication**: OAuth support for protected operations
- 🌐 **HTTP Transport**: Streamable HTTP for web deployments
- 🎮 **Real-time Updates**: Live file watching and updates
- 🤖 **AI Assistance**: LLM-powered script optimization
- 📊 **Analytics**: Mod usage and performance metrics
- 🔄 **Sync**: Multi-instance database synchronization

## 📞 Support

For questions, issues, or contributions:

- 📋 Check the test suite for usage examples
- 📖 Review the CLAUDE.md for complete documentation
- 🐛 Report issues with detailed reproduction steps
- 💡 Suggest features with use case descriptions

---

*This modern MCP server represents a significant upgrade in functionality, reliability, and developer experience for Project Zomboid mod development.*