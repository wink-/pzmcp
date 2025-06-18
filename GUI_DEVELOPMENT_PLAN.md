# Project Zomboid MCP Studio - GUI Development Plan

## 🎯 Project Vision

Transform the Project Zomboid MCP Server into **"PZ MCP Studio"** - a professional desktop application that revolutionizes Project Zomboid mod development through an intuitive graphical interface powered by AI assistance.

## 🛠️ Technology Stack

### Core Framework: Tauri
- **Frontend**: React + TypeScript + Vite
- **Backend**: Rust (Tauri Core)
- **Styling**: Tailwind CSS + Headless UI
- **State Management**: Zustand or Redux Toolkit
- **Code Editor**: Monaco Editor (VS Code engine)
- **AI Integration**: Claude SDK for TypeScript

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                 PZ MCP Studio (Tauri)                  │
├─────────────────────────────────────────────────────────┤
│  Frontend (React + TypeScript)                         │
│  ├── UI Components (Tailwind + Headless UI)            │
│  ├── Monaco Editor (Script Editing)                    │
│  ├── Claude SDK (AI Integration)                       │
│  └── State Management (Zustand)                        │
├─────────────────────────────────────────────────────────┤
│  Tauri Core (Rust)                                     │
│  ├── IPC Communication                                 │
│  ├── File System Access                                │
│  ├── Process Management                                │
│  └── Security Layer                                    │
├─────────────────────────────────────────────────────────┤
│  Python MCP Server Backend                             │
│  ├── Database Operations (SQLite FTS5)                 │
│  ├── Script Parsing & Validation                       │
│  ├── Path Management                                   │
│  └── Data Extraction                                   │
└─────────────────────────────────────────────────────────┘
```

## 🎨 User Interface Design

### Main Application Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🎮 PZ MCP Studio                                     🔍 ⚙️ 💬 📋 ❓ │
├─────────────────────────────────────────────────────────────────────┤
│ 🔍 Global Search: "Find items, generate scripts, ask Claude..."     │
├─────────────┬─────────────────────────────┬─────────────────────────┤
│   Sidebar   │        Main Content         │     Properties/AI       │
│             │                             │                         │
│ 📁 Explorer │ ┌─────────────────────────┐ │ ┌─────────────────────┐ │
│ ├─📄 Items  │ │                         │ │ │   💬 Claude Chat    │ │
│ ├─🍳 Recipes│ │     Script Editor       │ │ │                     │ │
│ ├─🚗 Vehicles│ │   (Monaco Editor)       │ │ │ "Create a tactical  │ │
│ ├─📋 My Mods│ │                         │ │ │  knife with..."     │ │
│ └─🔍 Search │ └─────────────────────────┘ │ │                     │ │
│             │                             │ └─────────────────────┘ │
│ 🏠 Dashboard│ ┌─────────────────────────┐ │ ┌─────────────────────┐ │
│ ⚡ Quick Gen │ │   Visual Script Builder │ │ │   Item Properties   │ │
│ 🎯 Templates│ │    (Drag & Drop)        │ │ │                     │ │
│ 📊 Mod Check│ │                         │ │ │ Damage: ▓▓▓░░ 1.5   │ │
│             │ └─────────────────────────┘ │ │ Weight: ▓▓░░░ 2.0   │ │
│             │                             │ │ [ Balance Check ]   │ │
└─────────────┴─────────────────────────────┴─────────────────────────┘
```

## 🚀 Development Phases

### Phase 1: Foundation (4-6 weeks)

#### 1.1 Tauri App Setup
- **Initialize Tauri project** with React + TypeScript
- **Configure build system** with Vite and Tailwind CSS
- **Set up development environment** with hot reload
- **Create basic window management** and app shell

#### 1.2 Python Integration
- **IPC Communication Layer** between Tauri and Python MCP server
- **Process Management** - Start/stop Python server automatically
- **Error Handling** - Graceful fallbacks and user feedback
- **Database Connection** - SQLite access from frontend

#### 1.3 Core UI Components
- **Sidebar Navigation** with collapsible sections
- **Main Content Area** with tab management
- **Properties Panel** with dynamic forms
- **Status Bar** with connection status and notifications

#### 1.4 Basic Search Interface
- **Global Search Bar** with auto-complete
- **Search Results View** with filtering and sorting
- **Item Detail Cards** showing properties and metadata
- **Search History** and saved queries

**Deliverables:**
- ✅ Working Tauri app with Python integration
- ✅ Basic UI shell and navigation
- ✅ Search functionality for vanilla items
- ✅ Item browsing and detail views

### Phase 2: Advanced Features (6-8 weeks)

#### 2.1 Script Editor Integration
- **Monaco Editor Setup** with Project Zomboid syntax highlighting
- **Custom Language Definition** for PZ script syntax
- **Real-time Validation** with error markers and tooltips
- **Auto-completion** using vanilla game data
- **Code Formatting** and beautification tools

#### 2.2 Visual Script Builder
- **Drag & Drop Recipe Editor** with ingredient selection
- **Property Form Builder** with sliders and validation
- **Template System** for quick script generation
- **Balance Analyzer** comparing to vanilla items
- **Preview Mode** showing generated script

#### 2.3 Claude AI Integration
- **Claude SDK Setup** for TypeScript
- **Chat Interface** with conversation history
- **Context-Aware Assistance** using current project data
- **Natural Language Script Generation** 
- **AI-Powered Code Review** and suggestions

#### 2.4 Mod Management System
- **Project Browser** for organizing multiple mods
- **File Tree View** with mod structure validation
- **Import/Export Tools** for mod packages
- **Dependency Tracking** and conflict detection
- **Version Control** basic Git integration

**Deliverables:**
- ✅ Full-featured script editor with validation
- ✅ Visual drag-drop script builder
- ✅ Claude AI chat integration
- ✅ Complete mod management workflow

### Phase 3: Mod Directory Validation & Polish (4-5 weeks)

#### 3.1 Comprehensive Mod Checker ⭐ NEW FEATURE
- **Directory Structure Validation**
  - Check for required folders (`media/scripts/`, `mod.info`, etc.)
  - Validate file naming conventions
  - Ensure proper folder hierarchy
  - Detect missing or misplaced files

- **Script Content Analysis**
  - Parse all `.txt` files for syntax errors
  - Validate item/recipe/vehicle references
  - Check for duplicate item IDs
  - Verify sound and texture references

- **Mod.info Validation**
  - Check required fields (name, id, description, etc.)
  - Validate version format
  - Verify dependency declarations
  - Check for special characters in mod ID

- **Balance & Performance Analysis**
  - Flag overpowered/underpowered items
  - Detect potential performance issues
  - Check recipe complexity and balance
  - Analyze mod size and asset count

- **Compatibility Checker**
  - Scan for conflicts with vanilla content
  - Check compatibility with popular mods
  - Validate Workshop requirements
  - Generate compatibility report

#### 3.2 Mod Checker Interface
```
┌─────────────────────────────────────────────────────────┐
│ 📊 Mod Checker - "Survival Expanded"                   │
├─────────────────────────────────────────────────────────┤
│ Overall Health: ████████░░ 8/10                        │
├─────────────────────────────────────────────────────────┤
│ ✅ Structure    │ ⚠️  Content      │ ❌ Performance    │
│                │                  │                   │
│ ✅ mod.info     │ ⚠️  3 warnings   │ ❌ 2 issues       │
│ ✅ media/       │ ✅ No duplicates │ ❌ Large textures │
│ ✅ scripts/     │ ⚠️  Reference    │ ❌ Complex recipe │
│ ✅ textures/    │    warnings      │                   │
├─────────────────────────────────────────────────────────┤
│ 📋 Issues Found (5)                                    │
│ ❌ recipe_metalworking.txt:45 - Invalid item reference │
│ ⚠️  item_weapons.txt:12 - Overpowered damage (3.5)     │
│ ❌ texture_knife.png - File size too large (2.1MB)     │
│ ⚠️  mod.info - Missing 'poster' field                  │
│ ⚠️  sound_reload.wav - File not found                  │
├─────────────────────────────────────────────────────────┤
│ [ Fix Auto ] [ Export Report ] [ Workshop Check ]      │
└─────────────────────────────────────────────────────────┘
```

#### 3.3 Auto-Fix Capabilities
- **Smart Corrections** for common issues
- **Batch Operations** for multiple files
- **Backup Creation** before making changes
- **Undo/Redo** functionality for modifications

#### 3.4 User Experience Polish
- **Themes** - Dark/Light mode with Project Zomboid styling
- **Keyboard Shortcuts** for power users
- **Accessibility** features (screen reader support, high contrast)
- **Performance Optimization** for large mods
- **Error Recovery** and crash reporting

#### 3.5 Distribution & Updates
- **Auto-Updater** using Tauri's built-in system
- **Installer Creation** for Windows/Mac/Linux
- **Documentation Integration** with interactive help
- **Telemetry** (opt-in) for usage analytics

**Deliverables:**
- ✅ Comprehensive mod validation system
- ✅ Auto-fix capabilities for common issues
- ✅ Polished user experience with themes
- ✅ Distribution-ready application with installer

## 🎯 Key Features Deep Dive

### 1. Intelligent Search & Discovery
- **Fuzzy Search** across all vanilla content
- **Visual Filters** with sliders and checkboxes
- **Saved Searches** and search history
- **Comparison Mode** for side-by-side analysis
- **Export Search Results** to various formats

### 2. Advanced Script Editor
- **Syntax Highlighting** for Project Zomboid scripts
- **IntelliSense** with vanilla game data
- **Error Squiggles** with fix suggestions
- **Code Folding** and minimap navigation
- **Multi-tab Editing** with session restore

### 3. Visual Script Builder
- **Template Gallery** with preview thumbnails
- **Property Editors** with real-time validation
- **Balance Indicators** showing vanilla comparisons
- **Dependency Visualization** with node graphs
- **Export Options** (clipboard, file, direct integration)

### 4. Claude AI Assistant
- **Contextual Chat** aware of current project
- **Natural Language Queries** ("Make this weapon stronger")
- **Code Generation** from descriptions
- **Review Mode** for quality suggestions
- **Learning Mode** that improves over time

### 5. Mod Directory Validator ⭐
- **Real-time Monitoring** of mod directories
- **Issue Categories** (Critical, Warning, Info)
- **Automated Fixes** for common problems
- **Workshop Preparation** checklist
- **Performance Impact** analysis

### 6. Project Management
- **Workspace Organization** with project templates
- **Asset Management** for textures and sounds
- **Version Control** integration with Git
- **Collaboration Tools** for team development
- **Export Pipeline** to Steam Workshop

## 🔧 Technical Implementation Details

### Tauri Configuration
```rust
// tauri.conf.json highlights
{
  "tauri": {
    "allowlist": {
      "fs": {
        "all": true,
        "scope": ["$APPDATA/pzmcp/*", "$HOME/.pzmcp/*"]
      },
      "shell": {
        "execute": true,
        "scope": ["python", "git"]
      },
      "dialog": {
        "open": true,
        "save": true
      }
    }
  }
}
```

### Python IPC Communication
```typescript
// Frontend TypeScript
import { invoke } from '@tauri-apps/api/tauri';

interface SearchResult {
  item_name: string;
  display_name: string;
  properties: Record<string, any>;
}

async function searchItems(query: string): Promise<SearchResult[]> {
  return await invoke('search_vanilla_items', { query });
}
```

```rust
// Rust backend
#[tauri::command]
async fn search_vanilla_items(query: String) -> Result<Vec<SearchResult>, String> {
  // Communicate with Python MCP server
  let output = Command::new("python")
    .args(["-c", &format!("from mcp_server import search; search('{}')", query)])
    .output()
    .map_err(|e| e.to_string())?;
  
  // Parse and return results
  serde_json::from_slice(&output.stdout).map_err(|e| e.to_string())
}
```

### Claude SDK Integration
```typescript
import { Anthropic } from '@anthropic-ai/sdk';

class ClaudeAssistant {
  private client: Anthropic;
  
  async generateScript(prompt: string, context: ModContext): Promise<string> {
    const response = await this.client.messages.create({
      model: 'claude-3-sonnet-20240229',
      max_tokens: 2000,
      messages: [{
        role: 'user',
        content: `${context.toPrompt()}\n\nUser request: ${prompt}`
      }]
    });
    
    return response.content[0].text;
  }
}
```

### Mod Checker Engine
```typescript
interface ModCheckResult {
  overall_score: number;
  categories: {
    structure: CheckCategory;
    content: CheckCategory;
    performance: CheckCategory;
    compatibility: CheckCategory;
  };
  issues: ModIssue[];
  suggestions: ModSuggestion[];
}

class ModChecker {
  async validateMod(modPath: string): Promise<ModCheckResult> {
    return {
      overall_score: await this.calculateOverallScore(modPath),
      categories: {
        structure: await this.checkStructure(modPath),
        content: await this.checkContent(modPath),
        performance: await this.checkPerformance(modPath),
        compatibility: await this.checkCompatibility(modPath)
      },
      issues: await this.findIssues(modPath),
      suggestions: await this.generateSuggestions(modPath)
    };
  }
  
  private async checkStructure(modPath: string): Promise<CheckCategory> {
    // Validate directory structure, required files, naming conventions
  }
  
  private async checkContent(modPath: string): Promise<CheckCategory> {
    // Parse scripts, validate references, check for duplicates
  }
  
  private async checkPerformance(modPath: string): Promise<CheckCategory> {
    // Analyze asset sizes, recipe complexity, potential bottlenecks
  }
  
  private async checkCompatibility(modPath: string): Promise<CheckCategory> {
    // Check conflicts with vanilla, popular mods, Workshop requirements
  }
}
```

## 📦 Packaging & Distribution

### Build Targets
- **Windows**: `.msi` installer + portable `.exe`
- **macOS**: `.dmg` installer + `.app` bundle  
- **Linux**: `.AppImage` + `.deb` packages

### Auto-Update Strategy
- **GitHub Releases** as update source
- **Incremental Updates** for faster downloads
- **Beta Channel** for early testing
- **Rollback Capability** if issues occur

### Installation Requirements
- **Python 3.11+** (bundled with installer option)
- **Project Zomboid** (auto-detected during setup)
- **4GB RAM** minimum, 8GB recommended
- **1GB storage** for application and cache

## 🎉 Success Metrics

### User Experience Goals
- **Setup Time**: < 5 minutes from download to first use
- **Search Speed**: < 200ms for vanilla item queries
- **Script Generation**: < 30 seconds for complex items
- **Mod Validation**: < 60 seconds for typical mods

### Feature Adoption Targets
- **80%** of users utilize the search functionality
- **60%** of users try the visual script builder
- **40%** of users engage with Claude AI assistant
- **70%** of users run mod validation before publishing

### Quality Metrics
- **< 1%** crash rate during normal operation
- **< 5 seconds** application startup time
- **99%** accuracy in script validation
- **90%** user satisfaction in UX surveys

## 🗓️ Development Timeline

### Months 1-2: Foundation
- Tauri setup and Python integration
- Core UI components and navigation
- Basic search and item browsing
- Initial script editor integration

### Months 3-4: Advanced Features
- Visual script builder and templates
- Claude AI integration and chat interface
- Mod management and project organization
- Advanced editor features (validation, auto-complete)

### Months 5-6: Mod Checker & Polish
- Comprehensive mod validation system
- Auto-fix capabilities and suggestions
- User experience polish and themes
- Testing, optimization, and bug fixes

### Month 7: Release Preparation
- Documentation and help system
- Installer creation and distribution setup
- Beta testing with community
- Final polish and release candidate

## 🤝 Community Integration

### Beta Testing Program
- **Early Access** for active modders
- **Feedback Collection** through built-in tools
- **Feature Requests** voting system
- **Bug Bounty** program for critical issues

### Documentation Strategy
- **Interactive Tutorials** within the application
- **Video Guides** for complex workflows
- **Community Wiki** for tips and tricks
- **API Documentation** for extensibility

### Future Extensibility
- **Plugin System** for community addons
- **Theme Marketplace** for custom styling
- **Template Sharing** between users
- **Mod Showcase** integrated gallery

---

*This development plan transforms the Project Zomboid MCP Server into a professional desktop application that will revolutionize how Project Zomboid mods are created, validated, and maintained.*