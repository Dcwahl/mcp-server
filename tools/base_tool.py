"""
Base Tool Class for MCP Development Server

This module provides the foundation for the class-based tool system,
inspired by Serena's architecture but adapted for MCP integration.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ToolMetadata:
    """Metadata about a tool for registration and discovery"""
    name: str
    description: str
    category: str
    context_modes: List[str]  # Which contexts this tool is relevant for
    requires_git: bool = False
    requires_filesystem: bool = False
    is_destructive: bool = False  # Whether tool modifies files/state
    performance_cost: str = "low"  # low, medium, high


class Tool(ABC):
    """
    Base class for all MCP tools in the registry system.
    
    This provides a standardized interface that all tools must implement,
    making them composable and allowing for better error handling,
    caching, and context awareness.
    """
    
    def __init__(self, project_root: str = "/Users/diegowahl/mcp-server"):
        self.project_root = project_root
        self._metadata: Optional[ToolMetadata] = None
        
    @property
    @abstractmethod
    def metadata(self) -> ToolMetadata:
        """Return metadata about this tool"""
        pass
    
    @abstractmethod
    def apply(self, **kwargs) -> str:
        """
        Execute the tool's main functionality.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            str: Tool output/result
            
        Raises:
            ToolError: If execution fails
        """
        pass
    
    def validate_params(self, **kwargs) -> Dict[str, Any]:
        """
        Validate and normalize parameters before execution.
        
        Override this to add tool-specific validation logic.
        Default implementation passes through all parameters.
        """
        return kwargs
    
    def can_execute(self, context: Optional[str] = None) -> bool:
        """
        Check if tool can execute in the current context.
        
        Args:
            context: Current workflow context (exploration, debugging, etc.)
            
        Returns:
            bool: Whether tool can execute
        """
        if context and context not in self.metadata.context_modes:
            return False
        return True
    
    def get_cache_key(self, **kwargs) -> Optional[str]:
        """
        Generate cache key for this tool execution.
        
        Override this for tools that can benefit from caching.
        Return None if tool should not be cached.
        """
        return None
    
    def get_file_dependencies(self, **kwargs) -> Optional[List[str]]:
        """
        Get list of files this tool execution depends on.
        
        Used for cache invalidation when files change.
        Override this for tools that read files.
        """
        return None
    
    def pre_execute_hook(self, **kwargs) -> None:
        """Hook called before tool execution. Override for setup logic."""
        pass
    
    def post_execute_hook(self, result: str, **kwargs) -> None:
        """Hook called after tool execution. Override for cleanup logic."""
        pass


class ToolError(Exception):
    """Base exception for tool execution errors"""
    
    def __init__(self, message: str, tool_name: str, details: Optional[Dict] = None):
        self.tool_name = tool_name
        self.details = details or {}
        super().__init__(f"{tool_name}: {message}")


class ToolRegistry:
    """
    Central registry for managing and discovering tools.
    
    Handles tool registration, context filtering, and execution coordination.
    """
    
    def __init__(self):
        self._tools: Dict[str, Type[Tool]] = {}
        self._instances: Dict[str, Tool] = {}
        self._contexts: Dict[str, List[str]] = {
            "exploration": [],
            "debugging": [],
            "refactoring": [],
            "general": []
        }
        
    def register_tool(self, tool_class: Type[Tool]) -> None:
        """
        Register a tool class in the registry.
        
        Args:
            tool_class: Tool class to register
        """
        # Create temporary instance to get metadata
        temp_instance = tool_class()
        metadata = temp_instance.metadata
        
        self._tools[metadata.name] = tool_class
        
        # Register in appropriate contexts
        for context in metadata.context_modes:
            if context in self._contexts:
                self._contexts[context].append(metadata.name)
            else:
                self._contexts[context] = [metadata.name]
                
        logger.info(f"Registered tool: {metadata.name} in contexts: {metadata.context_modes}")
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """
        Get a tool instance by name.
        
        Args:
            name: Tool name
            
        Returns:
            Tool instance or None if not found
        """
        if name not in self._instances:
            if name in self._tools:
                self._instances[name] = self._tools[name]()
            else:
                return None
                
        return self._instances[name]
    
    def list_tools(self, context: Optional[str] = None) -> List[ToolMetadata]:
        """
        List available tools, optionally filtered by context.
        
        Args:
            context: Filter by context mode
            
        Returns:
            List of tool metadata
        """
        if context and context in self._contexts:
            tool_names = self._contexts[context]
        else:
            tool_names = list(self._tools.keys())
            
        metadata_list = []
        for name in tool_names:
            tool = self.get_tool(name)
            if tool:
                metadata_list.append(tool.metadata)
                
        return metadata_list
    
    def execute_tool(self, name: str, context: Optional[str] = None, **kwargs) -> str:
        """
        Execute a tool by name with error handling and hooks.
        
        Args:
            name: Tool name
            context: Current workflow context
            **kwargs: Tool parameters
            
        Returns:
            Tool execution result
            
        Raises:
            ToolError: If tool not found or execution fails
        """
        tool = self.get_tool(name)
        if not tool:
            raise ToolError(f"Tool '{name}' not found", name)
            
        if not tool.can_execute(context):
            raise ToolError(f"Tool '{name}' cannot execute in context '{context}'", name)
            
        try:
            # Validate parameters
            validated_params = tool.validate_params(**kwargs)
            
            # Check cache first
            cache_key = tool.get_cache_key(**validated_params)
            if cache_key:
                file_deps = tool.get_file_dependencies(**validated_params)
                # Try to import cache_manager here to avoid circular imports
                try:
                    from .cache_manager import cache_manager
                    cached_result = cache_manager.get(cache_key, file_deps)
                    if cached_result is not None:
                        logger.debug(f"Cache hit for tool: {name}")
                        return cached_result
                except ImportError:
                    # Cache manager not available, continue without caching
                    pass
            
            # Execute hooks and main logic
            tool.pre_execute_hook(**validated_params)
            result = tool.apply(**validated_params)
            tool.post_execute_hook(result, **validated_params)
            
            # Cache result if applicable
            if cache_key:
                try:
                    from .cache_manager import cache_manager
                    file_deps = tool.get_file_dependencies(**validated_params)
                    cache_manager.set(cache_key, result, file_deps)
                    logger.debug(f"Cached result for tool: {name}")
                except ImportError:
                    pass
            
            return result
            
        except Exception as e:
            if isinstance(e, ToolError):
                raise
            else:
                raise ToolError(f"Execution failed: {str(e)}", name, {"original_error": str(e)})
    
    def get_tools_by_category(self, category: str) -> List[ToolMetadata]:
        """Get all tools in a specific category"""
        all_tools = self.list_tools()
        return [tool for tool in all_tools if tool.category == category]
    
    def get_destructive_tools(self) -> List[ToolMetadata]:
        """Get all tools that modify files or state"""
        all_tools = self.list_tools()
        return [tool for tool in all_tools if tool.is_destructive]


# Global registry instance
registry = ToolRegistry()


def register_tool(tool_class: Type[Tool]) -> Type[Tool]:
    """
    Decorator for registering tools in the global registry.
    
    Usage:
        @register_tool
        class MyTool(Tool):
            ...
    """
    registry.register_tool(tool_class)
    return tool_class
