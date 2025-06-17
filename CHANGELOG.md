# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - YYYY-MM-DD

**Foundation - Data Extraction Pipeline (Initial Implementation)**

This initial version focuses on parsing and structuring Project Zomboid script data.

### Added

*   **Project Zomboid Script Parser:**
    *   Parses items, recipes, vehicles, vehicle models, and script module definitions.
    *   Handles nested structures, various value types, and comments.
*   **Data Modeling:**
    *   Python classes for `Item`, `Recipe`, `Vehicle`, etc., providing a structured representation of game entities.
*   **Data Transformation:**
    *   Logic to convert raw parsed data into instances of the defined data models.
*   **Data Repository (`GameDataRepository`):**
    *   Loads all Project Zomboid script files from a specified directory.
    *   Manages parsed and transformed game data objects.
    *   Provides methods to query data (e.g., get item by name, list all recipes).
    *   Includes namespacing for items based on their script module.
*   **Basic Command-Line Interface (`mcp_server_cli.py`):**
    *   Allows direct interaction for inspecting loaded game data.
*   **Logging Framework:**
    *   Integrated Python's `logging` module across components for diagnostics and error reporting.
*   **Error Handling:**
    *   Graceful handling of file I/O errors, script parsing errors, and data lookup issues.
*   **Initial Test Harnesses:**
    *   Basic test setups within each major module to verify core functionality.

### Changed

*   Optimized CLI list commands (`listitems`, `listrecipes`, `listvehicles`) to prevent redundant data fetching.

### Fixed

*   Ensured all warning messages utilize the standard logging system (e.g., `logger.warning()` instead of `print()`).
