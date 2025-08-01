"""
AST Analysis Tools - Class-based implementations with advanced caching

This module contains class-based implementations of AST analysis tools
that benefit significantly from the caching system.
"""

import ast
import os
from typing import Optional, List, Dict, Any
from .base_tool import Tool, ToolMetadata, ToolError, register_tool


@register_tool
class AnalyzeFileStructureTool(Tool):
    """Tool for analyzing Python file structure using AST"""
    
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="analyze_file_structure",
            description="Analyze the structure of a specific file (imports, classes, functions)",
            category="code_analysis",
            context_modes=["general", "exploration", "debugging", "refactoring"],
            requires_filesystem=True,
            performance_cost="medium"
        )
    
    def validate_params(self, **kwargs):
        file_path = kwargs.get('file_path')
        if not file_path:
            raise ToolError("file_path parameter is required", self.metadata.name)
        
        # Convert to absolute path if relative
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.project_root, file_path)
            
        if not os.path.exists(file_path):
            raise ToolError(f"File not found: {file_path}", self.metadata.name)
            
        return {"file_path": file_path}
    
    def apply(self, **kwargs) -> str:
        """Analyze file structure using AST"""
        from .ast_utils import analyze_file_structure
        validated_params = self.validate_params(**kwargs)
        # Pass project_root to maintain compatibility with existing function
        return analyze_file_structure(validated_params["file_path"], self.project_root)
    
    def get_cache_key(self, **kwargs) -> Optional[str]:
        """Cache based on file path - content hash will be handled by cache manager"""
        file_path = kwargs.get('file_path', '')
        return f"analyze_file_structure:{file_path}"
    
    def get_file_dependencies(self, **kwargs) -> Optional[List[str]]:
        """This tool depends on the file being analyzed"""
        file_path = kwargs.get('file_path', '')
        if file_path and os.path.exists(file_path):
            return [file_path]
        return None


@register_tool
class GetProjectOverviewTool(Tool):
    """Tool for getting high-level project overview"""
    
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="get_project_overview",
            description="Get a high-level overview of the entire project structure",
            category="code_analysis",
            context_modes=["general", "exploration"],
            requires_filesystem=True,
            performance_cost="high"  # This is expensive as it scans all files
        )
    
    def validate_params(self, **kwargs):
        project_root = kwargs.get('project_root', self.project_root)
        
        if not os.path.exists(project_root):
            raise ToolError(f"Project root not found: {project_root}", self.metadata.name)
            
        return {"project_root": project_root}
    
    def apply(self, **kwargs) -> str:
        """Get project overview"""
        from .ast_utils import get_project_overview
        validated_params = self.validate_params(**kwargs)
        return get_project_overview(validated_params["project_root"])
    
    def get_cache_key(self, **kwargs) -> Optional[str]:
        """Cache based on project root"""
        project_root = kwargs.get('project_root', self.project_root)
        return f"get_project_overview:{project_root}"
    
    def get_file_dependencies(self, **kwargs) -> Optional[List[str]]:
        """This tool depends on all Python files in the project"""
        project_root = kwargs.get('project_root', self.project_root)
        
        if not os.path.exists(project_root):
            return None
            
        # Find all Python files that would be analyzed
        python_files = []
        for root, dirs, files in os.walk(project_root):
            # Skip common non-source directories
            dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.venv', 'node_modules'}]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        return python_files


@register_tool
class FindFunctionUsagesTool(Tool):
    """Tool for finding function usages across the project"""
    
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="find_function_usages",
            description="Find all usages of a function across the project",
            category="code_analysis",
            context_modes=["general", "debugging", "refactoring"],
            requires_filesystem=True,
            performance_cost="high"
        )
    
    def validate_params(self, **kwargs):
        function_name = kwargs.get('function_name')
        if not function_name:
            raise ToolError("function_name parameter is required", self.metadata.name)
            
        project_root = kwargs.get('project_root', self.project_root)
        
        if not os.path.exists(project_root):
            raise ToolError(f"Project root not found: {project_root}", self.metadata.name)
            
        return {"function_name": function_name, "project_root": project_root}
    
    def apply(self, **kwargs) -> str:
        """Find function usages"""
        from .ast_utils import find_function_usages
        validated_params = self.validate_params(**kwargs)
        return find_function_usages(validated_params["function_name"], validated_params["project_root"])
    
    def get_cache_key(self, **kwargs) -> Optional[str]:
        """Cache based on function name and project root"""
        function_name = kwargs.get('function_name', '')
        project_root = kwargs.get('project_root', self.project_root)
        return f"find_function_usages:{function_name}:{project_root}"
    
    def get_file_dependencies(self, **kwargs) -> Optional[List[str]]:
        """This tool depends on all Python files in the project"""
        project_root = kwargs.get('project_root', self.project_root)
        
        if not os.path.exists(project_root):
            return None
            
        # Find all Python files
        python_files = []
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.venv', 'node_modules'}]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        return python_files


@register_tool
class GetFunctionSignatureTool(Tool):
    """Tool for getting function signature and documentation"""
    
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="get_function_signature",
            description="Get the signature, location, and documentation of a function",
            category="code_analysis",
            context_modes=["general", "exploration", "debugging"],
            requires_filesystem=True,
            performance_cost="medium"
        )
    
    def validate_params(self, **kwargs):
        function_name = kwargs.get('function_name')
        if not function_name:
            raise ToolError("function_name parameter is required", self.metadata.name)
            
        project_root = kwargs.get('project_root', self.project_root)
        
        if not os.path.exists(project_root):
            raise ToolError(f"Project root not found: {project_root}", self.metadata.name)
            
        return {"function_name": function_name, "project_root": project_root}
    
    def apply(self, **kwargs) -> str:
        """Get function signature"""
        from .ast_utils import get_function_signature
        validated_params = self.validate_params(**kwargs)
        return get_function_signature(validated_params["function_name"], validated_params["project_root"])
    
    def get_cache_key(self, **kwargs) -> Optional[str]:
        """Cache based on function name and project root"""
        function_name = kwargs.get('function_name', '')
        project_root = kwargs.get('project_root', self.project_root)
        return f"get_function_signature:{function_name}:{project_root}"
    
    def get_file_dependencies(self, **kwargs) -> Optional[List[str]]:
        """This tool depends on all Python files in the project"""
        project_root = kwargs.get('project_root', self.project_root)
        
        if not os.path.exists(project_root):
            return None
            
        # Find all Python files
        python_files = []
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.venv', 'node_modules'}]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        return python_files
