"""
MCP Development Server - Enhanced with Tool Registry System

This version integrates the new class-based tool registry while maintaining
backward compatibility with existing function-based tools.
"""

from mcp.server.fastmcp import FastMCP
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the tool registry system
from tools.base_tool import registry, ToolError

# Import and register class-based tools (this automatically registers them)
from tools import file_tools, ast_tools

# Import existing function-based tools for backward compatibility
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

# Create an MCP server
mcp = FastMCP("DevTools")


# Helper function to create MCP tools from registry
def create_mcp_tool_from_registry(tool_name: str):
    """Create an MCP tool function that uses the tool registry"""
    def mcp_tool_wrapper(**kwargs):
        try:
            return registry.execute_tool(tool_name, **kwargs)
        except ToolError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error in tool {tool_name}: {e}")
            return f"Unexpected error: {str(e)}"
    
    return mcp_tool_wrapper


# Register class-based tools with MCP
# File Operations (using new registry system)
@mcp.tool()
def read_file(file_path: str) -> str:
    """Read the contents of a file"""
    return create_mcp_tool_from_registry("read_file")(file_path=file_path)

@mcp.tool()
def list_directory(directory_path: str = ".") -> str:
    """List contents of a directory"""
    return create_mcp_tool_from_registry("list_directory")(directory_path=directory_path)

@mcp.tool()
def find_files(pattern: str, directory: str = ".") -> str:
    """Find files matching a pattern (e.g., '*.py', '*.js')"""
    return create_mcp_tool_from_registry("find_files")(pattern=pattern, directory=directory)


# File Operations (legacy function-based for operations not yet converted)
@mcp.tool()
def read_lines(file_path: str, start_line: int = None, end_line: int = None) -> str:
    """Read specific line ranges from a file (1-indexed)"""
    return read_file_lines(file_path, start_line, end_line)

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


# AST Analysis Tools (using new registry system)
@mcp.tool()
def analyze_file_structure_tool(file_path: str, project_root: str = "/Users/diegowahl/mcp-server") -> str:
    """Analyze the structure of a specific file (imports, classes, functions)"""
    return create_mcp_tool_from_registry("analyze_file_structure")(file_path=file_path, project_root=project_root)

@mcp.tool()
def get_project_overview_tool(project_root: str = "/Users/diegowahl/mcp-server") -> str:
    """Get a high-level overview of the entire project structure"""
    return create_mcp_tool_from_registry("get_project_overview")(project_root=project_root)

@mcp.tool()
def find_function_usages_tool(function_name: str, project_root: str = "/Users/diegowahl/mcp-server") -> str:
    """Find all usages of a function across the project"""
    return create_mcp_tool_from_registry("find_function_usages")(function_name=function_name, project_root=project_root)

@mcp.tool()
def get_function_signature_tool(function_name: str, project_root: str = "/Users/diegowahl/mcp-server") -> str:
    """Get the signature, location, and documentation of a function"""
    return create_mcp_tool_from_registry("get_function_signature")(function_name=function_name, project_root=project_root)


# Command Operations (legacy)
@mcp.tool()
def reinstall_server() -> str:
    """Reinstall this MCP server (useful after making changes)"""
    return reinstall_mcp_server()


# Project Introspection with Registry Integration
@mcp.tool()
def list_tools() -> str:
    """Show all available MCP tools with descriptions"""
    # Enhanced version that includes registry info
    legacy_tools = list_all_tools()
    
    # Add registry tool information
    registry_tools = registry.list_tools()
    if registry_tools:
        registry_info = "\n\n## Class-Based Tools (with caching)\n"
        for tool_metadata in registry_tools:
            registry_info += f"- **{tool_metadata.name}**: {tool_metadata.description} "
            registry_info += f"(Category: {tool_metadata.category}, "
            registry_info += f"Performance: {tool_metadata.performance_cost})\n"
        
        # Add cache statistics
        try:
            from tools.cache_manager import cache_manager
            stats = cache_manager.get_stats()
            registry_info += f"\n**Cache Stats**: {stats['hit_rate']} hit rate, "
            registry_info += f"{stats['entry_count']} entries, "
            registry_info += f"{stats['cache_size_mb']:.1f}MB used\n"
        except Exception:
            pass
            
        return legacy_tools + registry_info
    
    return legacy_tools

@mcp.tool()
def project_status() -> str:
    """Get current project overview and status"""
    base_status = get_project_status()
    
    # Add registry status
    registry_tools = registry.list_tools()
    registry_status = f"\n\n## Tool Registry Status\n"
    registry_status += f"- **Registered Tools**: {len(registry_tools)}\n"
    
    # Group by category
    categories = {}
    for tool in registry_tools:
        if tool.category not in categories:
            categories[tool.category] = []
        categories[tool.category].append(tool.name)
    
    for category, tools in categories.items():
        registry_status += f"- **{category.title()}**: {', '.join(tools)}\n"
    
    # Add cache info
    try:
        from tools.cache_manager import cache_manager
        stats = cache_manager.get_stats()
        registry_status += f"- **Cache Performance**: {stats['hit_rate']} hit rate, {stats['invalidations']} invalidations\n"
    except Exception:
        pass
        
    return base_status + registry_status

@mcp.tool()
def show_examples() -> str:
    """Show common tool usage patterns and examples"""
    return show_tool_usage_examples()


# Git Operations (legacy - these work well as-is)
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


# Cache Management Tools
@mcp.tool()
def cache_stats() -> str:
    """Get cache performance statistics"""
    try:
        from tools.cache_manager import cache_manager
        stats = cache_manager.get_stats()
        
        result = "# Cache Performance Statistics\n\n"
        result += f"**Hit Rate**: {stats['hit_rate']}\n"
        result += f"**Cache Hits**: {stats['hits']}\n"
        result += f"**Cache Misses**: {stats['misses']}\n"
        result += f"**Invalidations**: {stats['invalidations']}\n"
        result += f"**Cache Size**: {stats['cache_size_mb']:.1f} MB / {stats['max_size_mb']} MB\n"
        result += f"**Entries**: {stats['entry_count']}\n"
        
        return result
        
    except Exception as e:
        return f"Error getting cache stats: {e}"

@mcp.tool()
def clear_cache() -> str:
    """Clear all cache entries"""
    try:
        from tools.cache_manager import cache_manager
        cleared = cache_manager.clear()
        return f"Cleared {cleared} cache entries"
    except Exception as e:
        return f"Error clearing cache: {e}"


# Print startup information
def log_startup_info():
    """Log information about the enhanced server on startup"""
    registry_tools = registry.list_tools()
    logger.info(f"MCP Development Server starting with {len(registry_tools)} registry tools")
    
    for tool in registry_tools:
        logger.info(f"  - {tool.name} ({tool.category}, {tool.performance_cost} cost)")

# Call startup logging
log_startup_info()
