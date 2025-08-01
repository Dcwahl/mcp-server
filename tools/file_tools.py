"""
File Operation Tools - Class-based implementations

This module contains class-based implementations of file operation tools
that integrate with the new tool registry system.
"""

import os
from typing import Optional
from .base_tool import Tool, ToolMetadata, ToolError, register_tool
from .io_utils import read_file_content, list_directory_contents  # Keep using existing utilities


@register_tool
class ReadFileTool(Tool):
    """Tool for reading file contents"""
    
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="read_file",
            description="Read the contents of a file",
            category="file_operations",
            context_modes=["general", "exploration", "debugging", "refactoring"],
            requires_filesystem=True,
            performance_cost="low"
        )
    
    def validate_params(self, **kwargs):
        file_path = kwargs.get('file_path')
        if not file_path:
            raise ToolError("file_path parameter is required", self.metadata.name)
        
        # Convert to absolute path if relative
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.project_root, file_path)
            
        return {"file_path": file_path}
    
    def apply(self, **kwargs) -> str:
        """Read file contents"""
        validated_params = self.validate_params(**kwargs)
        return read_file_content(validated_params["file_path"])
    
    def get_cache_key(self, **kwargs) -> Optional[str]:
        """Cache based on file path and modification time"""
        file_path = kwargs.get('file_path', '')
        if os.path.exists(file_path):
            mtime = os.path.getmtime(file_path)
            return f"read_file:{file_path}:{mtime}"
        return f"read_file:{file_path}:0"
    
    def get_file_dependencies(self, **kwargs) -> Optional[list]:
        """This tool depends on the file being read"""
        file_path = kwargs.get('file_path', '')
        if file_path:
            return [file_path]
        return None


@register_tool  
class ListDirectoryTool(Tool):
    """Tool for listing directory contents"""
    
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="list_directory",
            description="List contents of a directory with file sizes",
            category="file_operations", 
            context_modes=["general", "exploration"],
            requires_filesystem=True,
            performance_cost="low"
        )
    
    def validate_params(self, **kwargs):
        directory_path = kwargs.get('directory_path', '.')
        
        # Convert to absolute path if relative
        if not os.path.isabs(directory_path):
            directory_path = os.path.join(self.project_root, directory_path)
            
        return {"directory_path": directory_path}
    
    def apply(self, **kwargs) -> str:
        """List directory contents"""
        validated_params = self.validate_params(**kwargs)
        return list_directory_contents(validated_params["directory_path"])
    
    def get_cache_key(self, **kwargs) -> Optional[str]:
        """Cache based on directory path and modification time"""
        directory_path = kwargs.get('directory_path', '.')
        if os.path.exists(directory_path):
            mtime = os.path.getmtime(directory_path) 
            return f"list_directory:{directory_path}:{mtime}"
        return f"list_directory:{directory_path}:0"
    
    def get_file_dependencies(self, **kwargs) -> Optional[list]:
        """This tool depends on the directory being listed"""
        directory_path = kwargs.get('directory_path', '.')
        if directory_path:
            return [directory_path]
        return None


@register_tool
class FindFilesTool(Tool):
    """Tool for finding files by pattern"""
    
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="find_files",
            description="Find files matching a pattern (e.g., '*.py', '*.js')",
            category="file_operations",
            context_modes=["general", "exploration", "debugging"],
            requires_filesystem=True,
            performance_cost="medium"
        )
    
    def validate_params(self, **kwargs):
        pattern = kwargs.get('pattern')
        if not pattern:
            raise ToolError("pattern parameter is required", self.metadata.name)
            
        directory = kwargs.get('directory', '.')
        
        # Convert to absolute path if relative
        if not os.path.isabs(directory):
            directory = os.path.join(self.project_root, directory)
            
        return {"pattern": pattern, "directory": directory}
    
    def apply(self, **kwargs) -> str:
        """Find files matching pattern"""
        from .io_utils import find_files_by_pattern
        validated_params = self.validate_params(**kwargs) 
        return find_files_by_pattern(validated_params["pattern"], validated_params["directory"])
    
    def get_cache_key(self, **kwargs) -> Optional[str]:
        """Cache based on directory and pattern"""
        pattern = kwargs.get('pattern', '')
        directory = kwargs.get('directory', '.')
        # For file searches, we could cache but it's tricky with directory changes
        # For now, let's not cache this one
        return None
