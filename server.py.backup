"""
MCP Development Server - Local development tools for Claude
"""

from mcp.server.fastmcp import FastMCP
from tools.io_utils import (
    read_file_content, list_directory_contents, write_file_content, find_files_by_pattern,
    patch_file as do_patch_file, append_to_file as do_append_file, 
    find_in_file as do_find_in_file, read_file_lines
)
from tools.git_utils import (
    get_git_status, get_git_branch, get_git_log, do_git_add, 
    do_git_commit, do_git_push, do_git_checkout, get_git_diff, get_git_diff_staged
)
from tools.command_utils import reinstall_mcp_server
from tools.project_utils import list_all_tools, get_project_status, show_tool_usage_examples
from tools.ast_utils import (
    find_function_usages, get_function_signature, 
    analyze_file_structure, get_project_overview
)

# Create an MCP server
mcp = FastMCP("DevTools")

# File Operations
@mcp.tool()
def read_file(file_path: str) -> str:
    """Read the contents of a file"""
    return read_file_content(file_path)

@mcp.tool()
def read_lines(file_path: str, start_line: int = None, end_line: int = None) -> str:
    """Read specific line ranges from a file (1-indexed)"""
    return read_file_lines(file_path, start_line, end_line)

@mcp.tool()
def list_directory(directory_path: str = ".") -> str:
    """List contents of a directory"""
    return list_directory_contents(directory_path)

@mcp.tool()
def write_file(file_path: str, content: str) -> str:
    """Write content to a file (use with caution)"""
    return write_file_content(file_path, content)

@mcp.tool()
def patch_file(file_path: str, old_text: str, new_text: str) -> str:
    """Replace specific text in a file (find and replace) - safer than rewriting entire file"""
    return do_patch_file(file_path, old_text, new_text)

@mcp.tool()
def append_file(file_path: str, content: str) -> str:
    """Append content to the end of a file"""
    return do_append_file(file_path, content)

@mcp.tool()
def find_in_file(file_path: str, pattern: str, context_lines: int = 3) -> str:
    """Search for text in a file and return matches with context"""
    return do_find_in_file(file_path, pattern, context_lines)

@mcp.tool()
def find_files(pattern: str, directory: str = ".") -> str:
    """Find files matching a pattern (e.g., '*.py', '*.js')"""
    return find_files_by_pattern(pattern, directory)

# Command Operations
@mcp.tool()
def reinstall_server() -> str:
    """Reinstall this MCP server (useful after making changes)"""
    return reinstall_mcp_server()

# Project Introspection
@mcp.tool()
def list_tools() -> str:
    """Show all available MCP tools with descriptions"""
    return list_all_tools()

@mcp.tool()
def project_status() -> str:
    """Get current project overview and status"""
    return get_project_status()

@mcp.tool()
def show_examples() -> str:
    """Show common tool usage patterns and examples"""
    return show_tool_usage_examples()

# Git Read Operations
@mcp.tool()
def git_status() -> str:
    """Get git status of the current repository"""
    return get_git_status()

@mcp.tool()
def git_branch() -> str:
    """Get current git branch and list all branches"""
    return get_git_branch()

@mcp.tool()
def git_log(limit: int = 10) -> str:
    """Get recent git commit history"""
    return get_git_log(limit)

@mcp.tool()
def git_diff() -> str:
    """Show diff of unstaged changes"""
    return get_git_diff()

@mcp.tool()
def git_diff_staged() -> str:
    """Show diff of staged changes"""
    return get_git_diff_staged()

# Git Write Operations (use with caution)
@mcp.tool()
def git_add(files: str) -> str:
    """Add files to git staging area. Use '.' for all files"""
    return do_git_add(files)

@mcp.tool()
def git_commit(message: str) -> str:
    """Commit staged changes with a message"""
    return do_git_commit(message)

@mcp.tool()
def git_push(branch: str = None) -> str:
    """Push commits to remote repository"""
    return do_git_push(branch)

@mcp.tool()
def git_checkout(branch_name: str, create_new: bool = False) -> str:
    """Checkout existing branch or create new branch if create_new=True"""
    return do_git_checkout(branch_name, create_new)


# AST-based Code Analysis Tools
@mcp.tool()
def find_function_usages_tool(function_name: str) -> str:
    """Find all usages of a function across the project"""
    return find_function_usages(function_name)

@mcp.tool()
def get_function_signature_tool(function_name: str) -> str:
    """Get the signature, location, and documentation of a function"""
    return get_function_signature(function_name)

@mcp.tool()
def analyze_file_structure_tool(file_path: str) -> str:
    """Analyze the structure of a specific file (imports, classes, functions)"""
    return analyze_file_structure(file_path)

@mcp.tool()
def get_project_overview_tool() -> str:
    """Get a high-level overview of the entire project structure"""
    return get_project_overview()
