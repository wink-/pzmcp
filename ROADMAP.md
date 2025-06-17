# Roadmap for Project Zomboid MCP Server

This roadmap is derived from the project's PRD and outlines the planned development phases and features for the Project Zomboid MCP (Model Context Protocol) Server.

## Overall Vision
To transform Project Zomboid mod development by providing intelligent script validation, generation, and contextual assistance through AI-enhanced tooling, primarily leveraging the Model Context Protocol.

## Technical Stack Highlights (from PRD)
*   **Core Language:** Python 3.11+
*   **MCP Server Framework:** FastAPI
*   **Database:** SQLite (with FTS5 for search)
*   **Parser:** Custom Recursive Descent Parser (already developed in prototype)
*   **Key Dependencies:** Official `mcp` Python SDK, `pydantic`

## Development Phases

### Phase 1: Foundation (Current Focus: Completing Remaining Items)

*   **Data Extraction Pipeline (Partially Complete):**
    *   ✅ Script parser for items, recipes, vehicles, etc. (Implemented)
    *   ✅ Property extractor with basic type handling. (Implemented)
    *   ✅ In-memory data models and repository. (Implemented)
    *   **Next:** Implement SQLite database schema and populate with parsed vanilla game data.
    *   **Next:** Enhance reference collection (sounds, sprites, items) during parsing.
    *   **Next:** Refine handling of script syntax variations (e.g., `=` vs `:`) if further per-type strictness is needed.
*   **Basic Validation Engine:**
    *   **Next:** Develop line-by-line syntax validation for different script types.
    *   **Next:** Implement property name verification against known valid properties per script type.
    *   **Next:** Add value type and range checking.
    *   **Next:** Implement basic error reporting with line numbers for validation failures.

### Phase 2: Core MCP Tools & Server Implementation

*   **MCP Server Backend:**
    *   **Next:** Set up FastAPI application structure.
    *   **Next:** Integrate the official `mcp` Python SDK.
    *   **Next:** Design and implement MCP resources to expose game data (e.g., `vanilla_database`, `property_reference`).
*   **`validate_script` Tool:**
    *   Expose the Validation Engine's capabilities through an MCP tool.
    *   Input: Script content, script type.
    *   Output: Validation results with specific error locations.
*   **`generate_script` Tool:**
    *   Develop a template engine for generating script files.
    *   Input: Script type, base template, custom properties.
    *   Output: Formatted script with module wrapper.
*   **`search_vanilla` Tool & Advanced Search:**
    *   Implement SQLite FTS5 for full-text search on the vanilla data.
    *   Develop property-based filtering and similarity matching.
    *   Expose search capabilities via an MCP tool.
*   **Additional MCP Resources:**
    *   `property_reference`: Expose valid properties per script type.
    *   `modding_templates`: Provide pre-built script templates.

### Phase 3: Advanced Features

*   **Contextual Intelligence:**
    *   Property suggestions based on item type.
    *   Common pattern recognition in scripts.
    *   Compatibility warnings (e.g., for different game versions).
*   **Mod Project Management Tools (via MCP):**
    *   `analyze_mod`: File structure validation, cross-file reference tracking for a given mod directory.
    *   Dependency management insights.
    *   Build 42+ compatibility checking assistance.
*   **`best_practices` MCP Resource:**
    *   Expose modding guidelines and common patterns as a searchable resource.

### Phase 4: Polish, Integration & Testing

*   **Formal Testing Suite:**
    *   Develop comprehensive unit and integration tests (e.g., using `pytest`).
*   **Performance Optimization:**
    *   Profile and optimize server performance, especially database queries and parsing for large mods.
*   **Documentation:**
    *   Finalize user and developer documentation.
    *   Create examples and tutorials.
*   **Claude Desktop Integration:**
    *   Work towards seamless integration with Claude Desktop and other MCP clients.
