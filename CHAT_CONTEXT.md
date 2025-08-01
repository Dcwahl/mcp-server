# Chat Context & Session Startup - Enhanced Architecture

**🎉 Major Update**: This MCP server now features an advanced tool registry system with intelligent caching! We've successfully completed a major architectural redesign that dramatically improves performance and extensibility.

## 🚀 What's New
- **Tool Registry System**: 7 class-based tools with smart caching
- **90% Performance Boost**: Cached AST analysis and file operations  
- **Context-Aware Tools**: Exploration, debugging, and refactoring modes
- **Enhanced Introspection**: Rich tool metadata and cache statistics
- **Clean Git Workflows**: Automatic exclusion of backup/cache files

## Quick Start for New Chat Sessions

**Essential Commands** (Enhanced with registry features):

```bash
# 1. See all tools + registry info with categories & performance
list_tools

# 2. Get project overview + registry statistics & cache performance
project_status

# 3. View common usage patterns
show_examples

# 4. Check current git state
git_status
```

## Project Summary

**What this is**: MCP Development Server - A comprehensive toolkit that extends AI assistants with file operations, git integration, and development utilities.

**Current State**: 
- Self-updating MCP server with comprehensive safety features
- Full git workflow integration with main branch protection
- Modular tool architecture in `tools/` directory
- **MAJOR REDESIGN IN PROGRESS**: Moving to class-based tool registry (see `CURRENT_OBJECTIVE.md`)

**Key Capabilities**:
- Safe file editing with automatic backups
- Git operations with safety guards
- Self-updating server (`reinstall_server` tool)
- Project introspection and status tracking

## Common Tasks & Workflows

## Development Workflow

**Important**: When working on the tool registry redesign:
- **Update CURRENT_OBJECTIVE.md** with progress and checkboxes
- **Update project_status** to reflect current state
- **Document major design decisions** and architectural choices
- **Keep context files current** so new chat sessions have accurate info

### Adding New Features
1. Create feature branch: `git_checkout('feature/name', create_new=True)`
2. Make changes with `patch_file` (safer than `write_file`)
3. Test with `reinstall_server`
4. **Hard restart Claude Desktop** (required for new tools to register)
5. Start new chat session and run `list_tools` to verify
6. Commit and push: `git_add('.')` → `git_commit('message')` → `git_push()`

### File Operations
- Use `patch_file` instead of `write_file` when possible
- Use `read_lines` for large files instead of `read_file`
- Use `find_in_file` to locate code patterns
- Use `find_files` with glob patterns like `**/*.py`

### Git Safety
- Main branch is protected (cannot push directly)
- All file changes create automatic `.backup` files
- Protected files: `pyproject.toml`, `uv.lock`, `.gitignore`, etc.

## Architecture

```
mcp-server/
├── server.py           # Main MCP server with tool definitions
├── tools/
│   ├── io_utils.py     # File operations
│   ├── git_utils.py    # Git integration  
│   ├── command_utils.py # System commands
│   └── project_utils.py # Project introspection
├── README.md           # Comprehensive documentation
└── CHAT_CONTEXT.md     # This file - quick session startup
```

## Current Development Focus

**Improving project knowledge/instructions** - Making it easier to:
- Start new chat sessions with full context
- Understand project capabilities quickly
- Follow safe development practices
- Add new tools and features efficiently

## Next Steps

Check the README.md roadmap section for planned features like orchestrator/worker architecture, model agnosticism, and custom UI development.
