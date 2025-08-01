"""Project introspection utilities for the MCP server"""
import os
import inspect
from pathlib import Path

def list_all_tools() -> str:
    """List all available MCP tools with descriptions"""
    try:
        # This would be better with actual MCP introspection, but for now we'll hardcode
        tools = {
            "File Operations": {
                "read_file": "Read entire file contents",
                "read_lines": "Read specific line ranges (efficient for large files)",
                "write_file": "Overwrite entire file (use with caution)",
                "patch_file": "Find & replace specific text (safer than write_file)",
                "append_file": "Add content to end of file",
                "find_in_file": "Search for text with context lines",
                "find_files": "Find files by glob pattern (*.py, **/*.js, etc.)",
                "list_directory": "List directory contents with file sizes"
            },
            "Git Operations": {
                "git_status": "Show repository status",
                "git_branch": "Show current branch and list all branches",
                "git_log": "Show recent commit history",
                "git_diff": "Show unstaged changes",
                "git_diff_staged": "Show staged changes",
                "git_add": "Stage files for commit",
                "git_commit": "Commit staged changes",
                "git_push": "Push to remote (BLOCKS main branch)",
                "git_checkout": "Switch or create branches"
            },
            "System Operations": {
                "reinstall_server": "Reinstall MCP server after changes",
                "list_tools": "Show this tool inventory",
                "project_status": "Get current project overview"
            },
            "Code Analysis": {
                "find_function_usages_tool": "Find all usages of a function across the project",
                "get_function_signature_tool": "Get function signature, location, and documentation",
                "analyze_file_structure_tool": "Analyze file structure (imports, classes, functions)",
                "get_project_overview_tool": "Get high-level overview of project structure"
            }
        }
        
        output = ["# Available MCP Tools\n"]
        for category, tool_dict in tools.items():
            output.append(f"## {category}")
            for tool, description in tool_dict.items():
                output.append(f"- **{tool}**: {description}")
            output.append("")
        
        return "\n".join(output)
    except Exception as e:
        return f"Error listing tools: {str(e)}"

def get_project_status() -> str:
    """Get current project overview and status"""
    try:
        # Get basic project info
        project_root = "/Users/diegowahl/mcp-server"
        
        # Count project files (8 Python files: main.py, server.py, session_starter.py, tools/*.py)
        py_files = 8
        total_files = 20  # Approximate, focusing on project files
        
        # Get git info (we'll import this)
        from .git_utils import get_git_status, get_current_branch, get_git_log
        
        current_branch = get_current_branch()
        recent_commits = get_git_log(3)  # Last 3 commits
        
        status = [
            "# Project Status Overview",
            "",
            f"**Project**: MCP Development Server",
            f"**Location**: {project_root}",
            f"**Files**: {py_files} Python files, {total_files} total files",
            f"**Current branch**: {current_branch}",
            "",
            "## Recent Git Activity",
            recent_commits,
            "",
            "## Project Structure",
            "- `server.py` - Main MCP server with tool definitions",
            "- `tools/io_utils.py` - File operations (read, write, patch, find)",
            "- `tools/git_utils.py` - Git integration with safety features", 
            "- `tools/command_utils.py` - System commands and server management",
            "- `tools/project_utils.py` - Project introspection (this file)",
            "",
            "## Current Focus",
            "MAJOR ARCHITECTURAL REDESIGN: Moving to class-based tool registry system",
            "inspired by Serena's architecture. Implementing Tool base class, ToolRegistry,",
            "memory management, and caching strategy. See CURRENT_OBJECTIVE.md for details.",
            "",
            "## Key Features",
            "- ✅ Efficient file editing with patch_file",
            "- ✅ Git operations with main branch protection",
            "- ✅ Self-updating server with reinstall_server",
            "- ✅ Comprehensive safety features and backups",
            "",
            "## Quick Commands for New Sessions",
            "- `list_tools` - See all available tools",
            "- `project_status` - Get this overview", 
            "- `git_status` - Check repository state",
            "- `find_files *.py .` - See all Python files"
        ]
        
        return "\n".join(status)
    except Exception as e:
        return f"Error getting project status: {str(e)}"

def show_tool_usage_examples() -> str:
    """Show common usage patterns and examples"""
    examples = [
        "# Common Tool Usage Examples",
        "",
        "## File Operations",
        "```python",
        "# Read specific lines instead of entire file",
        "read_lines('server.py', 1, 20)",
        "",
        "# Safe text replacement (preferred over write_file)",
        "patch_file('server.py', ",
        "    old_text='def old_function():', ",
        "    new_text='def new_function():')",
        "",
        "# Search for code patterns",
        "find_in_file('server.py', '@mcp.tool()', context_lines=2)",
        "",
        "# Find all Python files recursively", 
        "find_files('**/*.py', '.')",
        "```",
        "",
        "## Git Workflow",
        "```python",
        "# Safe development workflow",
        "git_checkout('feature/new-tool', create_new=True)",
        "# ... make changes ...",
        "git_add('.')",
        "git_commit('Add new tool functionality')",
        "git_push()  # Safe - blocks main branch",
        "```",
        "",
        "## Server Management", 
        "```python",
        "# After making changes to server code",
        "reinstall_server()  # Updates MCP registration",
        "# Then restart Claude Desktop to pick up changes",
        "```",
        "",
        "## Project Navigation",
        "```python",
        "# Get oriented in new conversation",
        "list_tools()      # See what's available",
        "project_status()  # Current state overview",
        "git_status()      # Repository status",
        "```"
    ]
    
    return "\n".join(examples)
