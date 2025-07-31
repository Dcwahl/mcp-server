"""
MCP Development Server - Local development tools for Claude
"""

from mcp.server.fastmcp import FastMCP
from tools.io_utils import read_file_content, list_directory_contents, write_file_content, find_files_by_pattern
from tools.git_utils import (
    get_git_status, get_git_branch, get_git_log, git_add_files, 
    git_commit, git_push, git_checkout_branch, git_diff, git_diff_staged
)

# Create an MCP server
mcp = FastMCP("DevTools")

# File Operations
@mcp.tool()
def read_file(file_path: str) -> str:
    """Read the contents of a file"""
    return read_file_content(file_path)

@mcp.tool()
def list_directory(directory_path: str = ".") -> str:
    """List contents of a directory"""
    return list_directory_contents(directory_path)

@mcp.tool()
def write_file(file_path: str, content: str) -> str:
    """Write content to a file (use with caution)"""
    return write_file_content(file_path, content)

@mcp.tool()
def find_files(pattern: str, directory: str = ".") -> str:
    """Find files matching a pattern (e.g., '*.py', '*.js')"""
    return find_files_by_pattern(pattern, directory)

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
    return git_diff()

@mcp.tool()
def git_diff_staged() -> str:
    """Show diff of staged changes"""
    return git_diff_staged()

# Git Write Operations (use with caution)
@mcp.tool()
def git_add(files: str) -> str:
    """Add files to git staging area. Use '.' for all files"""
    return git_add_files(files)

@mcp.tool()
def git_commit(message: str) -> str:
    """Commit staged changes with a message"""
    return git_commit(message)

@mcp.tool()
def git_push(branch: str = None) -> str:
    """Push commits to remote repository"""
    return git_push(branch)

@mcp.tool()
def git_checkout(branch_name: str, create_new: bool = False) -> str:
    """Checkout existing branch or create new branch if create_new=True"""
    return git_checkout_branch(branch_name, create_new)
