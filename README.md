# Project Zomboid MCP Server Prototype

## Overview

The Project Zomboid MCP (Model Context Protocol) Server Prototype is a Python-based application aimed at transforming Project Zomboid mod development. It achieves this by providing intelligent script validation, generation, and contextual assistance, primarily designed to be leveraged by AI-enhanced tooling and direct modder use.

This server parses and manages game data from Project Zomboid's script files (defining items, recipes, vehicles, etc.), making this data accessible and queryable. The long-term vision is to expose this information via the Model Context Protocol, enabling powerful integrations with AI assistants like Claude and other development tools.

## Core Goals (from PRD)

*   **Reduce Syntax Errors**: Validate scripts in real-time.
*   **Accelerate Development**: Generate script templates.
*   **Enhance Discovery**: Make vanilla game data searchable.
*   **Improve AI Assistance**: Provide accurate, context-aware modding help.

## Current Components

The prototype currently includes the following foundational Python modules:

*   **`script_parser.py`**: Lexer and parser for Project Zomboid script files, converting them into a structured dictionary format.
*   **`data_models.py`**: Python classes representing game entities (Items, Recipes, Vehicles, etc.).
*   **`data_transformer.py`**: Converts the parser's output into instances of the data models.
*   **`data_repository.py`**: Loads, manages, and provides query access to all parsed game data from a specified Project Zomboid script directory.
*   **`mcp_server_cli.py`**: A basic command-line interface (CLI) for direct interaction with the `GameDataRepository` to inspect loaded data.

## Planned MCP Tools & Server Functionality

While the current CLI allows for data inspection, the full vision includes developing a server (likely using FastAPI and the official `mcp` Python SDK) that will expose capabilities such as:

*   **`validate_script`**: For real-time syntax and reference checking.
*   **`generate_script`**: For creating new script files from templates.
*   **`search_vanilla`**: For in-depth searching of vanilla game data.
*   And other tools as outlined in the project's PRD.

## Basic CLI Usage (Current)

The CLI provides direct access to the data parsed by the current system.

**Syntax:**

```bash
python mcp_server_cli.py <path_to_pz_script_directory> <command> [command_arguments]
```

**Examples:**

*   List all loaded items:
    ```bash
    python mcp_server_cli.py ./media/scripts listitems
    ```

*   Get details for a specific item (e.g., "Base.Apple"):
    ```bash
    python mcp_server_cli.py ./media/scripts getitem Base.Apple
    ```

## Script File Format

Project Zomboid script files generally use a C-like or JSON-like syntax, defining modules, items, recipes, etc., with properties specified as key-value pairs. The parser is designed to handle this format.

Example:
```
module Base
{
    item Apple
    {
        Type = Food,
        DisplayName = Apple,
        Weight = 0.1
    }
}
```
