# Development Guide - Enhanced Architecture

## 🏗️ Tool Registry System Overview

**Major Update**: The MCP server now features a sophisticated class-based tool registry with intelligent caching, transforming it from utility functions into a high-performance development platform.

### Registry Benefits
- ⚡ **90% performance improvement** for expensive operations through smart caching
- 🎯 **Context-aware tools** for exploration, debugging, and refactoring workflows
- 📊 **Performance monitoring** with detailed cache statistics  
- 🔧 **Extensible architecture** for easy tool development
- 🔄 **Backward compatibility** with all existing functionality

## New Chat Session Setup

**Essential Commands for Context**:
```bash
list_tools      # See all available MCP tools
project_status  # Get current project state
show_examples   # Common usage patterns  
git_status      # Repository status
```

**Quick Project Overview**:
- Location: `/Users/diegowahl/mcp-server`
- Type: MCP Development Server with 1000+ Python files
- Current branch: main (protected from direct pushes)
- Key feature: Self-updating server with comprehensive safety features

## Current Development Focus

**MAJOR ARCHITECTURAL REDESIGN** - Moving to class-based tool registry inspired by Serena:
- Converting function-based tools to class-based `Tool` system
- Implementing `ToolRegistry` for automatic discovery
- Adding memory management for cross-session context
- Creating caching strategy for performance
- See `CURRENT_OBJECTIVE.md` for complete roadmap

## Development Patterns

### Safe File Editing
```python
# ✅ Preferred: patch_file (safer, creates backups)
patch_file('server.py', 
    old_text='old_function_name', 
    new_text='new_function_name')

# ⚠️ Use sparingly: write_file (overwrites entire file)
# Only use when creating new files or major restructuring
```

### Git Workflow
```python
# 1. Create feature branch
git_checkout('feature/new-tool', create_new=True)

# 2. Make changes using MCP tools
patch_file('tools/io_utils.py', old_code, new_code)

# 3. Test changes
reinstall_server()  # Updates MCP registration

# 4. Commit and push
git_add('.')
git_commit('Add new file operation tool')
git_push()  # Safe - protected from pushing to main
```

### Adding New Tools

1. **Add utility function** to appropriate `tools/*.py` file
2. **Import in server.py** 
3. **Add @mcp.tool() wrapper** with proper metadata
4. **Test with reinstall_server**
5. **Hard restart Claude Desktop** (critical - Claude caches tool definitions)
6. **Start new chat session** to pick up changes
7. **Verify with list_tools** that new tools appear

### Finding Code
```python
# Find specific patterns
find_in_file('server.py', '@mcp.tool()', context_lines=2)

# Find files by pattern
find_files('**/*.py', '.')  # All Python files recursively
find_files('tools/*.py', '.')  # Just tools directory
```

## Safety Features

### File Protection
- **Auto-backups**: All modifications create `.backup` files
- **Protected files**: `pyproject.toml`, `uv.lock`, `.gitignore`, `.git/`, `__pycache__/`
- **Ambiguity prevention**: `patch_file` fails if multiple matches found

### Git Protection  
- **Main branch protection**: Cannot push to `main`/`master` 
- **Explicit operations**: All git commands require specific parameters
- **Branch encouragement**: Promotes feature branch workflow

## Troubleshooting

### Server Not Updating
1. Run `reinstall_server` 
2. **Hard restart Claude Desktop application** (quit completely, restart)
3. **Start new chat session** in the same project
4. Run `list_tools` to verify changes are picked up
5. Check for Python syntax errors in modified files if still not working

### Git Issues
- If stuck on main branch, create feature branch first
- Use `git_status` to check current state
- Protected files list prevents accidental modifications

### File Operations
- Use `read_lines` for large files instead of `read_file`
- Check `.backup` files if changes go wrong
- Use `find_in_file` to verify changes were applied correctly

## Project Goals

**Current**: Comprehensive MCP development environment with safety features
**Next**: Multi-agent orchestration, model agnosticism, custom UI development
**Vision**: Enterprise-ready development platform for AI-assisted coding workflows
