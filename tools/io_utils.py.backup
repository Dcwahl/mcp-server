"""File I/O utilities for the MCP server"""
import os
import glob
from pathlib import Path

# Protected files that should not be overwritten
PROTECTED_FILES = {
    'pyproject.toml',
    'uv.lock',
    '.gitignore',
    '.git',
    '__pycache__'
}

def read_file_content(file_path: str) -> str:
    """Read the contents of a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def list_directory_contents(directory_path: str = ".") -> str:
    """List contents of a directory"""
    try:
        items = []
        for item in Path(directory_path).iterdir():
            item_type = "dir" if item.is_dir() else "file"
            size = ""
            if item.is_file():
                try:
                    size = f" ({item.stat().st_size} bytes)"
                except:
                    pass
            items.append(f"{item_type}: {item.name}{size}")
        return "\n".join(sorted(items))
    except Exception as e:
        return f"Error listing directory: {str(e)}"

def write_file_content(file_path: str, content: str) -> str:
    """Write content to a file with safety checks"""
    try:
        file_name = Path(file_path).name
        if file_name in PROTECTED_FILES:
            return f"Error: {file_name} is protected and cannot be overwritten"
        
        # Create backup for existing files
        if Path(file_path).exists():
            backup_path = f"{file_path}.backup"
            with open(file_path, 'r', encoding='utf-8') as original:
                with open(backup_path, 'w', encoding='utf-8') as backup:
                    backup.write(original.read())
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

def find_files_by_pattern(pattern: str, directory: str = ".") -> str:
    """Find files matching a glob pattern"""
    try:
        search_path = Path(directory) / pattern
        matches = glob.glob(str(search_path), recursive=True)
        
        if not matches:
            return f"No files found matching pattern '{pattern}' in {directory}"
        
        # Sort and format results
        results = []
        for match in sorted(matches):
            path = Path(match)
            if path.is_file():
                size = path.stat().st_size
                results.append(f"{match} ({size} bytes)")
            else:
                results.append(f"{match} (directory)")
        
        return f"Found {len(results)} matches:\n" + "\n".join(results)
    except Exception as e:
        return f"Error searching files: {str(e)}"
