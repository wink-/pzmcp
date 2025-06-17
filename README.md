# MCP Server Prototype

## Overview

The MCP (Master Control Program) Server Prototype is a Python-based application designed to parse, manage, and provide access to game data defined in text-based script files. These script files typically define game entities such as items, recipes, vehicles, and more, using a custom C-like or JSON-like syntax.

The primary goal of this prototype is to establish a robust foundation for reading and interpreting these script files, making the data available for use by other game components or tools.

## Components

The server is comprised of several key Python modules:

*   **`script_parser.py`**: Contains the lexer and parser responsible for reading the raw script files and converting them into a structured dictionary format. It handles syntax, comments, and various data structures within the scripts.
*   **`data_models.py`**: Defines Python classes (e.g., `Item`, `Recipe`, `Vehicle`) that represent the game entities. These models use type hints and provide a clear, object-oriented way to work with the data.
*   **`data_transformer.py`**: Bridges the gap between the parser's dictionary output and the data models. It transforms the raw parsed data into instances of the defined data model classes.
*   **`data_repository.py`**: Acts as a central store for all loaded game data. It orchestrates the file reading, parsing, and transformation process. It then provides an API to query the loaded data (e.g., fetch an item by its name, list all available recipes).
*   **`mcp_server_cli.py`**: A command-line interface (CLI) that allows users to interact with the loaded game data. It uses the `GameDataRepository` to fetch and display information.

## CLI Usage

The primary way to interact with the MCP Server Prototype is through `mcp_server_cli.py`.

**Basic Syntax:**

```bash
python mcp_server_cli.py <path_to_script_directory> <command> [command_arguments]
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

*   List all loaded recipes:
    ```bash
    python mcp_server_cli.py ./media/scripts listrecipes
    ```

*   Get details for a specific recipe:
    ```bash
    python mcp_server_cli.py ./media/scripts getrecipe MyRecipeName
    ```

## Script File Format

The script files generally use a C-like or JSON-like syntax. They consist of blocks defining modules, items, recipes, vehicles, etc., with properties specified as key-value pairs.

Example snippet:

```
module MyModule
{
    item MyItem
    {
        DisplayName = "My Awesome Item",
        Type = Normal,
        Weight = 1.0,
        Icon = MyItemIcon
    }
}
```

The parser is designed to be relatively flexible with this format.
