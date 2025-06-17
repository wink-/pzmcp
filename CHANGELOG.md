# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - YYYY-MM-DD

### Added

*   Initial MCP server prototype:
    *   Script parser for items, recipes, vehicles, models, and templates.
    *   Data models for structured representation of game entities.
    *   Data transformer to map parsed data to models.
    *   Data repository for loading and accessing game data.
    *   Command-Line Interface (CLI) for interacting with the data.
*   Comprehensive logging using Python's `logging` module across all components.
*   Error handling for file operations, parsing issues, and data lookup.
*   Namespacing for items based on their module definitions.
*   Basic test harnesses within each module for core functionality verification.

### Changed

*   Optimized CLI list commands (`listitems`, `listrecipes`, `listvehicles`) to prevent redundant data fetching calls.

### Fixed

*   Ensured all warning messages, specifically in `data_models.py`, use the standard logging system instead of `print()`.
