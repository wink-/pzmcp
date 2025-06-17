# Roadmap

This document outlines potential future directions and enhancements for the MCP Server Prototype. These are ideas for improvement and are not yet committed development tasks.

## Short to Medium Term

*   **Formal Testing Suite:**
    *   Implement a comprehensive suite of unit and integration tests using a framework like `pytest` or `unittest`.
    *   This will improve code reliability and make refactoring safer.

*   **Advanced Data Queries:**
    *   Extend `GameDataRepository` with more sophisticated query methods:
        *   Find items by tags or other specific properties.
        *   Filter recipes by required skills, ingredients, or tools.
        *   Search for vehicles based on performance characteristics or parts.

*   **Script Schema Validation:**
    *   Implement a system for validating the structure and data types of parsed script files against a defined schema.
    *   This would help catch errors in script files more proactively.

*   **Enhanced CLI Features:**
    *   Add more interactive elements or more complex query options to the CLI.
    *   Support for outputting data in different formats (e.g., JSON, CSV).

## Medium to Long Term

*   **Web API Interface:**
    *   Develop a web API (e.g., using Flask or FastAPI) to expose the game data.
    *   This would allow other applications (e.g., game clients, web-based tools) to consume the data programmatically over HTTP.

*   **Performance Enhancements:**
    *   Profile the application with very large sets of script files.
    *   Optimize parsing, data storage, and querying for better performance and memory usage if bottlenecks are identified.

*   **Plugin System / Extensibility:**
    *   Design a plugin system to allow for:
        *   Support for new or custom script types without modifying the core parser.
        *   Custom data transformation or validation rules.

*   **Documentation Generation from Scripts:**
    *   Create tools that can parse the game scripts and automatically generate human-readable documentation (e.g., item lists, recipe books) in formats like HTML or Markdown.

*   **Configuration Management:**
    *   Allow for more flexible configuration of the server (e.g., script paths, logging levels, feature flags) through a configuration file.

## Community and Contributions

*   Establish contribution guidelines if the project were to be open-sourced.
*   Set up issue tracking and a process for community feedback.
