"""
AST-based code analysis tools for better codebase understanding
"""

import ast
import os
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass

@dataclass
class FunctionInfo:
    name: str
    file_path: str
    line_number: int
    args: List[str]
    docstring: Optional[str]
    is_method: bool
    class_name: Optional[str] = None

@dataclass
class ClassInfo:
    name: str
    file_path: str
    line_number: int
    methods: List[str]
    base_classes: List[str]
    docstring: Optional[str]

class CodeAnalyzer:
    def __init__(self, project_root: str = "/Users/diegowahl/mcp-server"):
        self.project_root = Path(project_root)
        self.excluded_dirs = {'.venv', '__pycache__', '.git', 'node_modules'}
    
    def get_python_files(self) -> List[Path]:
        """Get all Python files in the project"""
        files = []
        for py_file in self.project_root.rglob("*.py"):
            if not any(excluded in py_file.parts for excluded in self.excluded_dirs):
                files.append(py_file)
        return files
    
    def parse_file(self, file_path: Path) -> Optional[ast.AST]:
        """Parse a Python file into AST"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return ast.parse(content)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
    
    def find_function_definitions(self, file_path: Path) -> List[FunctionInfo]:
        """Find all function definitions in a file"""
        tree = self.parse_file(file_path)
        if not tree:
            return []
        
        functions = []
        current_class = None
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                current_class = node.name
            elif isinstance(node, ast.FunctionDef):
                # Get function arguments
                args = [arg.arg for arg in node.args.args]
                
                # Get docstring
                docstring = None
                if (node.body and isinstance(node.body[0], ast.Expr) 
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                    docstring = node.body[0].value.value
                
                # Determine if it's a method
                is_method = current_class is not None
                
                functions.append(FunctionInfo(
                    name=node.name,
                    file_path=str(file_path),
                    line_number=node.lineno,
                    args=args,
                    docstring=docstring,
                    is_method=is_method,
                    class_name=current_class
                ))
        
        return functions
    
    def find_function_calls(self, file_path: Path, target_function: str) -> List[Tuple[int, str]]:
        """Find all calls to a specific function in a file"""
        tree = self.parse_file(file_path)
        if not tree:
            return []
        
        calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Handle different call patterns
                func_name = None
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                
                if func_name == target_function:
                    # Get the line content for context
                    try:
                        with open(file_path, 'r') as f:
                            lines = f.readlines()
                            line_content = lines[node.lineno - 1].strip()
                    except:
                        line_content = f"<line {node.lineno}>"
                    
                    calls.append((node.lineno, line_content))
        
        return calls
    
    def find_imports(self, file_path: Path) -> Dict[str, List[str]]:
        """Find all imports in a file"""
        tree = self.parse_file(file_path)
        if not tree:
            return {}
        
        imports = {"from_imports": [], "direct_imports": []}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports["direct_imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports["from_imports"].append(f"from {module} import {alias.name}")
        
        return imports
    
    def find_class_definitions(self, file_path: Path) -> List[ClassInfo]:
        """Find all class definitions in a file"""
        tree = self.parse_file(file_path)
        if not tree:
            return []
        
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Get base classes
                bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        bases.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        bases.append(f"{base.value.id}.{base.attr}")
                
                # Get methods
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append(item.name)
                
                # Get docstring
                docstring = None
                if (node.body and isinstance(node.body[0], ast.Expr) 
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                    docstring = node.body[0].value.value
                
                classes.append(ClassInfo(
                    name=node.name,
                    file_path=str(file_path),
                    line_number=node.lineno,
                    methods=methods,
                    base_classes=bases,
                    docstring=docstring
                ))
        
        return classes

def find_function_usages(function_name: str, project_root: str = "/Users/diegowahl/mcp-server") -> str:
    """Find all usages of a function across the project"""
    analyzer = CodeAnalyzer(project_root)
    py_files = analyzer.get_python_files()
    
    results = []
    total_usages = 0
    
    for file_path in py_files:
        calls = analyzer.find_function_calls(file_path, function_name)
        if calls:
            relative_path = file_path.relative_to(analyzer.project_root)
            results.append(f"\n📁 **{relative_path}**:")
            for line_num, line_content in calls:
                results.append(f"  Line {line_num}: `{line_content}`")
                total_usages += 1
    
    if not results:
        return f"🔍 No usages found for function '{function_name}'"
    
    header = f"🔍 Found {total_usages} usage(s) of function '{function_name}':"
    return header + "\n" + "\n".join(results)

def get_function_signature(function_name: str, project_root: str = "/Users/diegowahl/mcp-server") -> str:
    """Get the signature and location of a function"""
    analyzer = CodeAnalyzer(project_root)
    py_files = analyzer.get_python_files()
    
    results = []
    
    for file_path in py_files:
        functions = analyzer.find_function_definitions(file_path)
        for func in functions:
            if func.name == function_name:
                relative_path = Path(func.file_path).relative_to(analyzer.project_root)
                
                # Format signature
                args_str = ", ".join(func.args) if func.args else ""
                signature = f"{func.name}({args_str})"
                
                # Build result
                result = f"📍 **{relative_path}:{func.line_number}**\n"
                if func.is_method and func.class_name:
                    result += f"   Method in class `{func.class_name}`\n"
                result += f"   `def {signature}`"
                
                if func.docstring:
                    # Show first line of docstring
                    first_line = func.docstring.split('\n')[0].strip()
                    result += f"\n   📝 {first_line}"
                
                results.append(result)
    
    if not results:
        return f"🔍 No function named '{function_name}' found"
    
    return f"🔍 Function definitions for '{function_name}':\n\n" + "\n\n".join(results)

def analyze_file_structure(file_path: str, project_root: str = "/Users/diegowahl/mcp-server") -> str:
    """Analyze the structure of a specific file"""
    analyzer = CodeAnalyzer(project_root)
    file_path_obj = Path(file_path)
    
    # Make path relative to project if it's absolute
    if file_path_obj.is_absolute():
        try:
            file_path_obj = file_path_obj.relative_to(analyzer.project_root)
        except ValueError:
            pass
    
    full_path = analyzer.project_root / file_path_obj
    
    if not full_path.exists():
        return f"❌ File not found: {file_path}"
    
    # Get functions and classes
    functions = analyzer.find_function_definitions(full_path)
    classes = analyzer.find_class_definitions(full_path)
    imports = analyzer.find_imports(full_path)
    
    results = [f"📁 **File Structure: {file_path_obj}**\n"]
    
    # Imports
    if imports["direct_imports"] or imports["from_imports"]:
        results.append("📦 **Imports:**")
        for imp in imports["direct_imports"]:
            results.append(f"  • import {imp}")
        for imp in imports["from_imports"]:
            results.append(f"  • {imp}")
        results.append("")
    
    # Classes
    if classes:
        results.append("🏛️ **Classes:**")
        for cls in classes:
            methods_str = ", ".join(cls.methods) if cls.methods else "no methods"
            bases_str = f" ({', '.join(cls.base_classes)})" if cls.base_classes else ""
            results.append(f"  • `{cls.name}`{bases_str} - {methods_str}")
        results.append("")
    
    # Functions
    if functions:
        results.append("⚙️ **Functions:**")
        for func in functions:
            if not func.is_method:  # Skip methods (already shown in classes)
                args_str = f"({', '.join(func.args)})" if func.args else "()"
                results.append(f"  • `{func.name}{args_str}` - line {func.line_number}")
        results.append("")
    
    return "\n".join(results)

def get_project_overview(project_root: str = "/Users/diegowahl/mcp-server") -> str:
    """Get a high-level overview of the project structure"""
    analyzer = CodeAnalyzer(project_root)
    py_files = analyzer.get_python_files()
    
    all_functions = []
    all_classes = []
    
    for file_path in py_files:
        functions = analyzer.find_function_definitions(file_path)
        classes = analyzer.find_class_definitions(file_path)
        all_functions.extend(functions)
        all_classes.extend(classes)
    
    results = [f"🔍 **Project Overview: {len(py_files)} Python files**\n"]
    
    # Group by file
    file_summaries = {}
    for file_path in py_files:
        relative_path = file_path.relative_to(analyzer.project_root)
        functions = analyzer.find_function_definitions(file_path)
        classes = analyzer.find_class_definitions(file_path)
        
        func_count = len([f for f in functions if not f.is_method])
        method_count = len([f for f in functions if f.is_method])
        class_count = len(classes)
        
        summary = []
        if class_count:
            summary.append(f"{class_count} class(es)")
        if func_count:
            summary.append(f"{func_count} function(s)")
        if method_count:
            summary.append(f"{method_count} method(s)")
        
        file_summaries[str(relative_path)] = ", ".join(summary) or "empty"
    
    results.append("📁 **Files:**")
    for file_path, summary in sorted(file_summaries.items()):
        results.append(f"  • `{file_path}` - {summary}")
    
    return "\n".join(results)
