# Project Zomboid MCP Server

<div align="center">

![Project Zomboid MCP Server](https://img.shields.io/badge/Project%20Zomboid-MCP%20Server-green?style=for-the-badge&logo=gamemaker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-Package%20Manager-purple?style=for-the-badge&logo=python&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-Desktop%20Ready-orange?style=for-the-badge&logo=anthropic&logoColor=white)

**Intelligent script validation, generation, and contextual assistance for Project Zomboid mod development**

*Transform your modding workflow with AI-enhanced tooling*

</div>

## 🚀 Overview

The Project Zomboid MCP Server is a comprehensive **Model Context Protocol** server that revolutionizes Project Zomboid mod development. It provides intelligent script validation, generation, and contextual assistance through AI-enhanced tooling, making modding accessible to developers of all skill levels.

### ✨ Key Features

- 🔍 **2,700+ Vanilla Items** - Complete searchable database with full-text search
- 🎯 **Smart Auto-Detection** - Automatically finds your Project Zomboid installation  
- ⚡ **Lightning Fast Setup** - One-command installation with uv package manager
- 🤖 **Claude Desktop Integration** - Seamless AI-assisted development
- ✅ **Real-time Validation** - Syntax checking and reference validation
- 🛠️ **Script Generation** - Template-based creation with balanced stats
- 🔧 **WSL Compatible** - Perfect for Windows developers

## 🎮 What It Does

Transform your modding experience:

```
"Use the Project Zomboid MCP to find me a crowbar"
→ Returns: Crowbar item with damage: 1.0, durability: 10, categories: Blunt;Improvised

"Create a steel katana with 2.5 damage and high durability"  
→ Generates: Complete Project Zomboid script with balanced stats

"Validate this script for syntax errors"
→ Analyzes: Line-by-line validation with specific error locations
```

## 🚀 Quick Start

### For Windows Users (Recommended)

1. **Install WSL** (if not already installed):
   ```powershell
   wsl --install
   ```

2. **Clone and setup**:
   ```bash
   git clone https://github.com/your-username/pzmcp.git
   cd pzmcp
   
   # Install uv (fast Python package manager)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source ~/.bashrc
   
   # Install dependencies and extract game data
   uv sync
   uv run python -c "
   from mcp_server.core.enhanced_data_extractor import extract_with_path_manager
   extract_with_path_manager(comprehensive=True)
   "
   ```

3. **Configure Claude Desktop** - See [CLAUDE_DESKTOP_INTEGRATION.md](CLAUDE_DESKTOP_INTEGRATION.md)

4. **Start modding with AI assistance!** 🎉

> **📖 Need detailed setup instructions?** See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for complete step-by-step guidance.

### For Linux/macOS Users

```bash
git clone https://github.com/your-username/pzmcp.git
cd pzmcp

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup and extract data  
uv sync
uv run python -c "
from mcp_server.core.enhanced_data_extractor import extract_with_path_manager
extract_with_path_manager(comprehensive=True)
"
```

## 🔧 Usage Examples

### Search and Discovery

```bash
# Find specific items
uv run python -c "
import sqlite3
conn = sqlite3.connect('mcp_data.db')
cursor = conn.cursor()
cursor.execute('SELECT item_name, display_name FROM items_fts WHERE display_name MATCH \"baseball bat\"')
for item in cursor.fetchall(): print(f'{item[0]}: {item[1]}')
"
```

### Script Generation

Create a custom item script:

```python
# Generate a tactical knife
from mcp_server.core.enhanced_data_extractor import EnhancedDataExtractor
# Use via Claude Desktop for natural language generation
```

### With Claude Desktop

Once configured, simply chat with Claude:

```
"Use the Project Zomboid MCP to help me create a survival mod with custom weapons"
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                MCP Server Core                      │
├─────────────────────────────────────────────────────┤
│  Path Manager  │  Enhanced Parser  │  Script Gen    │
├─────────────────────────────────────────────────────┤
│          SQLite FTS5 Database Layer                 │
├─────────────────────────────────────────────────────┤
│  Game Data     │  Templates       │  Validation     │
│  (2,700+ items)│  (JSON-based)   │  (Real-time)    │
└─────────────────────────────────────────────────────┘
```

### Data Pipeline

```
Project Zomboid Installation
        ↓
Path Manager (Auto-detection)
        ↓  
Enhanced Data Extractor
        ↓
SQLite FTS5 Database
        ↓
MCP Tools & Claude Integration
```

## 🛠️ MCP Tools Available

When integrated with Claude Desktop, you get access to:

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| `search_vanilla` | Find vanilla game items | *"Find all melee weapons with damage > 2.0"* |
| `generate_script` | Create new item/recipe scripts | *"Generate a tactical knife with spear attachment"* |
| `validate_script` | Check syntax and references | *"Validate this weapon script for errors"* |
| `check_references` | Verify item dependencies | *"Check if all referenced items exist"* |
| `analyze_mod` | Comprehensive mod analysis | *"Analyze my mod for balance issues"* |

## 🎯 Real-World Examples

### Item Research
```
User: "Find me all the different types of axes in Project Zomboid"
Claude: Using the Project Zomboid MCP to search for axes...
→ Returns: HandAxe, WoodAxe, AxeStone, FireAxe with full stats
```

### Balanced Script Creation
```
User: "Create a reinforced crowbar that's better than normal but not overpowered"
Claude: Analyzing vanilla crowbar stats and generating balanced alternative...
→ Creates: Complete item script with appropriate damage/durability increases
```

### Recipe Development
```
User: "Make a recipe to craft the reinforced crowbar using a normal crowbar and steel"
Claude: Generating craftRecipe with proper skill requirements...
→ Produces: Balanced recipe requiring Metalworking skill and appropriate materials
```

## 📁 Project Structure

```
pzmcp/
├── mcp_server/           # Core MCP server implementation
│   ├── core/            # Database, extraction, path management
│   ├── parsers/         # Script parsers for items/recipes/vehicles
│   └── templates/       # JSON templates for script generation
├── media/scripts/       # Project Zomboid script files (copied)
├── docs/               # Documentation and guides
│   ├── WINDOWS_SETUP.md
│   ├── CLAUDE_DESKTOP_INTEGRATION.md
│   └── CHANGELOG.md
├── pz_path_manager.py  # Smart PZ installation detection
├── pyproject.toml      # Modern Python packaging
└── README.md          # This file
```

## ⚡ Performance

- **🚀 10-100x faster** dependency management with uv
- **⚡ Sub-second search** across 2,700+ items
- **💾 Efficient storage** using SQLite FTS5
- **🔄 Auto-detection** of Project Zomboid installations
- **📱 Lightweight** - works on modest hardware

## 🔧 Advanced Configuration

### Custom Project Zomboid Paths

```bash
# Add custom installation path
uv run python pz_path_manager.py --add "my_pz" "C:\Custom\ProjectZomboid\media\scripts" 1
```

### Multiple Environments

Configure different Claude Desktop environments for development vs production mods.

### Debug Mode

```bash
# Run with debug logging
uv run python run_server.py --debug
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run the linter**: `uv run ruff check .`
5. **Submit a pull request**

### Development Setup

```bash
git clone https://github.com/your-username/pzmcp.git
cd pzmcp
uv sync --dev  # Install with development dependencies
uv run pytest  # Run tests
```

## 📚 Documentation

- **[Windows Setup Guide](WINDOWS_SETUP.md)** - Complete WSL installation and configuration
- **[Claude Desktop Integration](CLAUDE_DESKTOP_INTEGRATION.md)** - AI assistant setup
- **[Changelog](CHANGELOG.md)** - Version history and features
- **[PRD](PRD.md)** - Product requirements and architecture

## 🐛 Troubleshooting

### Common Issues

**MCP Server won't start?**
- Check WSL is installed and running
- Verify paths in Claude Desktop config
- Ensure database has been populated

**Database empty?**
- Run data extraction: `uv run python -c "from mcp_server.core.enhanced_data_extractor import extract_with_path_manager; extract_with_path_manager()"`
- Check Project Zomboid installation path

**Claude Desktop can't connect?**
- Restart Claude Desktop completely after config changes
- Check JSON syntax in MCP configuration
- Verify WSL paths are correct

### Get Help

- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Comprehensive guides for setup and usage
- **Community**: Discord servers for Project Zomboid modding

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **The Indie Stone** - For creating Project Zomboid and making it so moddable
- **Anthropic** - For Claude and the MCP protocol
- **Project Zomboid Modding Community** - For inspiration and feedback
- **Contributors** - Everyone who helps improve this tool

## 🚀 Roadmap

### v0.3.0 - Advanced Features
- Complete vehicle script support
- Advanced template system
- Lua script integration
- Performance optimization tools

### v1.0.0 - Production Ready
- GUI interface for non-technical users
- Steam Workshop integration
- Automated testing pipelines
- Enterprise support for mod teams

---

<div align="center">

**Transform your Project Zomboid modding workflow today!**

[📖 Setup Guide](WINDOWS_SETUP.md) • [🤖 Claude Integration](CLAUDE_DESKTOP_INTEGRATION.md) • [📋 Changelog](CHANGELOG.md)

*Made with ❤️ for the Project Zomboid modding community*

</div>