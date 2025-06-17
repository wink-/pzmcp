# Project Zomboid MCP Server Development Plan

## Project Overview and Goals

### Vision
Create an MCP server that transforms Project Zomboid mod development by providing intelligent script validation, generation, and contextual assistance through AI-enhanced tooling.

### Primary Goals
1. **Reduce Syntax Errors**: Validate scripts in real-time with type-specific syntax checking
2. **Accelerate Development**: Generate properly formatted script templates instantly
3. **Enhance Discovery**: Make vanilla game data searchable and accessible
4. **Improve AI Assistance**: Enable Claude and other AI assistants to provide accurate, context-aware modding help
5. **Streamline Workflow**: Automate repetitive tasks like reference validation and file structure creation

## Technical Architecture and Components

### Core Architecture

```
┌─────────────────────────────────────────────┐
│           MCP Server Core                   │
├─────────────────────────────────────────────┤
│  Parser Engine  │  Validation  │  Generator │
├─────────────────────────────────────────────┤
│          Data Layer (SQLite/JSON)           │
├─────────────────────────────────────────────┤
│  Vanilla Data   │  Templates   │  Docs      │
└─────────────────────────────────────────────┘
```

### MCP Tools Implementation

1. **`validate_script`**
   - Input: Script content, script type
   - Output: Validation results with specific error locations
   - Features: Syntax checking, reference validation, property range validation

2. **`generate_script`**
   - Input: Script type, base template, custom properties
   - Output: Properly formatted script with module wrapper
   - Features: Template selection, property suggestions, automatic formatting

3. **`search_vanilla`**
   - Input: Query string, filters (type, category, properties)
   - Output: Matching vanilla items/recipes/vehicles with full definitions
   - Features: Fuzzy search, property filtering, similarity ranking

4. **`check_references`**
   - Input: Item/sound/sprite references
   - Output: Validation status and suggestions for invalid references
   - Features: Batch checking, similarity suggestions, usage examples

5. **`analyze_mod`**
   - Input: Mod directory path
   - Output: Comprehensive analysis report
   - Features: Structure validation, cross-file reference checking, compatibility warnings

### MCP Resources

1. **`vanilla_database`**
   - Content: Parsed vanilla game data
   - Structure: Categorized by type (items, recipes, vehicles, etc.)
   - Access: Read-only, searchable, filterable

2. **`property_reference`**
   - Content: Valid properties per script type with descriptions
   - Structure: Hierarchical with value types and ranges
   - Access: Read-only, version-specific

3. **`modding_templates`**
   - Content: Pre-built templates for common mod scenarios
   - Structure: Categorized by use case
   - Access: Read-only, customizable

4. **`best_practices`**
   - Content: Modding guidelines and common patterns
   - Structure: Searchable documentation
   - Access: Read-only, contextual

## Detailed Feature Specifications

### Phase 1: Foundation (Weeks 1-4)

#### 1.1 Data Extraction Pipeline
```python
# Core components needed:
- Script parser for each type (item, recipe, vehicle, etc.)
- Property extractor with type detection
- Reference collector for sounds/sprites/items
- Database schema design and population
```

**Implementation Details:**
- Parse vanilla game files from `ProjectZomboid/media/scripts/`
- Handle syntax variations (= vs :) per script type
- Extract all unique properties, values, and references
- Build searchable index with relationships

#### 1.2 Basic Validation Engine
```python
# Validation rules by script type:
- Item Scripts: property = value, valid properties, reference checks
- Recipe Scripts: property:value, ingredient validation, result checks
- Vehicle Scripts: part hierarchy, physics constraints
- Model Scripts: texture paths, attachment points
```

**Features:**
- Line-by-line syntax validation
- Property name verification
- Value type and range checking
- Basic error reporting with line numbers

### Phase 2: Core Tools (Weeks 5-8)

#### 2.1 Script Generation System
```python
# Template engine features:
- Dynamic property insertion
- Automatic formatting per script type
- Module wrapper generation
- Import statement handling
```

**Key Components:**
- Template library with common patterns
- Property suggestion based on item type
- Automatic reference resolution
- Preview and iteration support

#### 2.2 Advanced Search Capabilities
```python
# Search features:
- Full-text search across all scripts
- Property-based filtering
- Similarity matching for typos
- Category browsing (weapons, food, tools, etc.)
```

**Implementation:**
- SQLite FTS5 for full-text search
- Property indexing for fast filtering
- Levenshtein distance for fuzzy matching
- Hierarchical category system

### Phase 3: Advanced Features (Weeks 9-12)

#### 3.1 Contextual Intelligence
```python
# Context-aware features:
- Property suggestions based on item type
- Common pattern recognition
- Compatibility warnings
- Performance impact analysis
```

**Capabilities:**
- Learn from vanilla patterns
- Suggest optimal property values
- Warn about deprecated features
- Recommend best practices

#### 3.2 Mod Project Management
```python
# Project features:
- File structure validation
- Cross-file reference tracking
- Dependency management
- Build 42 compatibility checking
```

**Tools:**
- Project scaffold generator
- Batch validation across files
- Reference integrity checking
- Version migration assistance

## Implementation Timeline

### Month 1: Foundation
- **Week 1-2**: Set up project structure, implement parsers
- **Week 3-4**: Build data extraction pipeline, populate database

### Month 2: Core Functionality
- **Week 5-6**: Implement validation engine and error reporting
- **Week 7-8**: Build script generation and search tools

### Month 3: Advanced Features
- **Week 9-10**: Add contextual intelligence and suggestions
- **Week 11-12**: Implement mod project management tools

### Month 4: Polish and Integration
- **Week 13-14**: Testing, bug fixes, performance optimization
- **Week 15-16**: Documentation, examples, Claude Desktop integration

## Resource Requirements

### Technical Stack
```yaml
Core:
  - Language: Python 3.11+
  - Framework: FastAPI for MCP server
  - Database: SQLite with FTS5
  - Parser: Custom recursive descent parser
  
Dependencies:
  - mcp: Official MCP Python SDK
  - pydantic: Data validation
  - pytest: Testing framework
  - rich: Enhanced CLI output
```

### Data Sources
1. **Vanilla Game Files**: ~50MB of script files to parse
2. **Documentation**: Official wiki and modding guides
3. **Community Resources**: Popular mod examples
4. **Update Tracking**: Build 42 changes and new features

### Development Resources
- 1 Senior Developer (full-time, 4 months)
- Game license for testing
- CI/CD pipeline setup
- Documentation writer (part-time, month 4)

## Expected Benefits and Outcomes

### For Modders
1. **80% Reduction in Syntax Errors**: Real-time validation catches mistakes before testing
2. **5x Faster Script Creation**: Templates and generation tools accelerate development
3. **Instant Reference Lookup**: No more manual searching through vanilla files
4. **Learning Acceleration**: Contextual help and examples guide new modders

### For AI Assistants
1. **Accurate Code Generation**: AI can validate output before presenting to users
2. **Contextual Understanding**: Access to full game data enables better suggestions
3. **Error Prevention**: Validation tools prevent AI from suggesting invalid code
4. **Enhanced Capabilities**: AI can search, analyze, and generate with confidence

### Success Metrics
- **Adoption**: 1000+ active users within 6 months
- **Error Reduction**: Measurable decrease in mod compilation errors
- **Time Savings**: 50% reduction in development time for common tasks
- **AI Integration**: Used by Claude Desktop for 90% of PZ modding queries

## Next Steps

1. **Prototype Development**: Build minimal viable parser for item scripts
2. **Community Feedback**: Share plan with PZ modding community
3. **Partnership**: Reach out to The Indie Stone for official support
4. **Funding**: Explore sponsorship from modding platforms
5. **Team Building**: Recruit contributors familiar with PZ modding

This MCP server will revolutionize Project Zomboid modding by bridging the gap between modders' needs and AI assistance capabilities, making mod development more accessible, efficient, and enjoyable for everyone.