# Chat Context & Session Startup

This file provides everything you need to quickly orient Claude (or any AI assistant) when starting a new chat session with this MCP project.

## Quick Start for New Chat Sessions

Run these commands to get oriented immediately:

```bash
# 1. See all available tools
list_tools

# 2. Get current project overview  
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

**Key Capabilities**:
- Safe file editing with automatic backups
- Git operations with safety guards
- Self-updating server (`reinstall_server` tool)
- Project introspection and status tracking

## Common Tasks & Workflows

### Adding New Features
1. Create feature branch: `git_checkout('feature/name', create_new=True)`
2. Make changes with `patch_file` (safer than `write_file`)
3. Test with `reinstall_server`
4. Commit and push: `git_add('.')` → `git_commit('message')` → `git_push()`

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
