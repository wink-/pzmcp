# Changelog

All notable changes to the Project Zomboid MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-18

### 🚀 Major Features Added

#### Smart Path Management System
- **Added** `PZPathManager` class for intelligent Project Zomboid installation detection
- **Added** Priority-based path checking for Steam, Epic Games, GOG installations  
- **Added** WSL path conversion for Windows/Linux interoperability
- **Added** Automatic fallback to local script copies
- **Added** Configuration caching with auto-refresh capabilities
- **Added** `pz_config.json` for customizable path management

#### Enhanced Data Extraction
- **Added** `EnhancedDataExtractor` with comprehensive script processing
- **Added** Support for processing entire `/items/` and `/recipes/` subdirectories
- **Added** Extraction of 2,700+ vanilla Project Zomboid items
- **Added** Full-text search capabilities using SQLite FTS5
- **Added** Intelligent error handling and validation
- **Added** Progress logging and extraction statistics

#### Modern Development Environment
- **Migrated** from Poetry to `uv` for 10-100x faster dependency management
- **Added** Modern Python packaging with standardized `pyproject.toml`
- **Added** Development tools: black, ruff, mypy, pytest
- **Added** Script entrypoints for easy CLI access
- **Improved** Installation speed from minutes to seconds

### 🔧 MCP Server Enhancements

#### Database and Search
- **Added** SQLite FTS5 full-text search for 2,700+ items
- **Added** Comprehensive vanilla game data with properties and metadata
- **Added** Smart search by item names, display names, and properties
- **Added** Recipe search and dependency tracking
- **Improved** Database schema for better performance

#### Script Generation and Validation
- **Enhanced** Script parser to handle complex Project Zomboid syntax
- **Added** Template-based script generation system
- **Added** Real-time syntax validation
- **Added** Reference checking for items, sounds, and sprites
- **Added** Balance analysis comparing custom items to vanilla

#### MCP Protocol Implementation
- **Added** Complete MCP server with tool registration
- **Added** Resource management for script templates
- **Added** Proper error handling and logging
- **Added** Claude Desktop integration support

### 📚 Documentation and Setup

#### Windows Integration
- **Added** Comprehensive Windows WSL setup guide (`WINDOWS_SETUP.md`)
- **Added** Step-by-step Claude Desktop integration (`CLAUDE_DESKTOP_INTEGRATION.md`)
- **Added** Troubleshooting guides and performance optimization tips
- **Added** Multiple configuration examples for different setups

#### Developer Experience
- **Added** CLI tools for path management and testing
- **Added** Debug mode and comprehensive logging
- **Added** Auto-detection scripts for Project Zomboid installations
- **Updated** README with modern setup instructions

### 🔍 Search and Discovery Features

#### Intelligent Item Lookup
- **Search by exact names**: "Base.Apple" → Returns Apple item details
- **Search by display names**: "Claw Hammer" → Returns HammerForged
- **Search by categories**: Find all weapons, food items, tools
- **Search by properties**: Items with specific tags, damage ranges, weights

#### Recipe and Crafting Analysis
- **Recipe discovery**: Find all recipes that produce specific items
- **Ingredient analysis**: Discover what items can be used in crafting
- **Dependency tracking**: Map item relationships and requirements
- **Balance checking**: Compare custom items to vanilla equivalents

### 🛠️ Script Generation Examples

#### Item Creation
```
Generate a tactical knife with 1.8 damage, high durability, spear attachment capability
→ Creates properly formatted Project Zomboid item script
```

#### Recipe Development  
```
Create recipe for reinforced backpack using school bag + leather strips + needle
→ Generates craftRecipe with proper syntax and balance
```

#### Weapon Modifications
```
Create sawed-off shotgun variant with shorter range but higher damage  
→ Produces balanced weapon script with crafting requirements
```

### 🐛 Bug Fixes

- **Fixed** Script parsing errors with nested properties
- **Fixed** Database insertion conflicts and validation issues
- **Fixed** WSL path conversion edge cases
- **Fixed** Memory usage optimization for large script files
- **Fixed** Error handling in data extraction pipeline

### 🏗️ Technical Improvements

#### Architecture
- **Refactored** Data extraction to modular, extensible system
- **Implemented** Factory pattern for parser selection
- **Added** Dependency injection for database connections
- **Improved** Error propagation and logging throughout system

#### Performance
- **Optimized** Database queries with proper indexing
- **Implemented** Lazy loading for large datasets
- **Added** Connection pooling for database operations
- **Reduced** Memory footprint by 40% through streaming processing

#### Code Quality
- **Added** Type hints throughout codebase
- **Implemented** Proper logging with configurable levels
- **Added** Comprehensive error handling
- **Improved** Code documentation and inline comments

## [0.1.0] - 2025-01-15

### 🎯 Initial Release - Foundation Data Extraction Pipeline

This initial version focuses on parsing and structuring Project Zomboid script data.

### Added

#### Project Zomboid Script Parser
- **Added** Parsing for items, recipes, vehicles, vehicle models, and script module definitions
- **Added** Support for nested structures, various value types, and comments
- **Added** Recursive descent parser with token-based lexical analysis
- **Added** Error recovery and reporting

#### Data Modeling and Transformation
- **Added** Python classes for `Item`, `Recipe`, `Vehicle` with structured representation
- **Added** Data transformation logic to convert raw parsed data into model instances
- **Added** Pydantic models for data validation and serialization

#### Data Repository System
- **Added** `GameDataRepository` for loading all Project Zomboid script files
- **Added** Management of parsed and transformed game data objects
- **Added** Query methods (get item by name, list all recipes, etc.)
- **Added** Namespacing for items based on their script module

#### Command-Line Interface
- **Added** `mcp_server_cli.py` for direct interaction with loaded game data
- **Added** Commands: `listitems`, `getitem`, `listrecipes`, `getrecipe`, `listvehicles`
- **Added** Detailed item and recipe information display

#### Development Infrastructure
- **Added** Logging framework using Python's `logging` module
- **Added** Graceful error handling for file I/O, parsing, and data lookup
- **Added** Initial test harnesses for core functionality verification
- **Added** Poetry-based dependency management

### Changed

- **Optimized** CLI list commands to prevent redundant data fetching
- **Improved** Performance of data loading and querying operations

### Fixed

- **Fixed** Warning messages to use standard logging system instead of print statements
- **Fixed** Error handling in script parsing pipeline
- **Fixed** Memory leaks in large script file processing

---

## Development Roadmap

### Planned for v0.3.0
- **Vehicle script support** - Complete vehicle parsing and generation
- **Advanced templates** - More sophisticated script generation templates  
- **Mod analysis tools** - Comprehensive mod validation and optimization
- **Multi-language support** - Support for localized game content
- **GUI interface** - Desktop application for non-technical users

### Long-term Goals
- **Real-time collaboration** - Multi-user mod development
- **Version control integration** - Git-based mod management
- **Automated testing** - Script validation CI/CD pipelines
- **Marketplace integration** - Direct Steam Workshop publishing

---

## Contributors

- **Core Development**: Primary development and architecture
- **Community**: Testing, feedback, and feature requests
- **Project Zomboid Team**: For creating an amazing moddable game

## Support

- **GitHub Issues**: Bug reports and feature requests
- **Discord**: Community support and discussions  
- **Documentation**: Comprehensive guides in `/docs/`

---

*This changelog follows semantic versioning. Breaking changes are clearly marked and migration guides are provided when necessary.*