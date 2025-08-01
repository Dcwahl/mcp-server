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

def read_file_lines(file_path: str, start_line: int = None, end_line: int = None) -> str:
    """Read specific line ranges from a file (1-indexed)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if start_line is None and end_line is None:
            return ''.join(lines)
        
        # Convert to 0-indexed
        start_idx = (start_line - 1) if start_line else 0
        end_idx = end_line if end_line else len(lines)
        
        if start_idx < 0 or start_idx >= len(lines):
            return f"Error: Start line {start_line} out of range (file has {len(lines)} lines)"
        
        selected_lines = lines[start_idx:end_idx]
        return ''.join(selected_lines)
    except Exception as e:
        return f"Error reading file lines: {str(e)}"

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

def patch_file(file_path: str, old_text: str, new_text: str) -> str:
    """Replace specific text in a file (find and replace)"""
    try:
        file_name = Path(file_path).name
        if file_name in PROTECTED_FILES:
            return f"Error: {file_name} is protected and cannot be modified"
        
        # Read current content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if old_text exists
        if old_text not in content:
            return f"Error: Text not found in file. Make sure the old_text exactly matches what's in the file."
        
        # Count occurrences
        occurrences = content.count(old_text)
        if occurrences > 1:
            return f"Error: Found {occurrences} matches for the text. Please be more specific to avoid ambiguity."
        
        # Create backup
        backup_path = f"{file_path}.backup"
        with open(backup_path, 'w', encoding='utf-8') as backup:
            backup.write(content)
        
        # Perform replacement
        new_content = content.replace(old_text, new_text)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return f"Successfully patched {file_path} (backup created at {backup_path})"
        
    except Exception as e:
        return f"Error patching file: {str(e)}"

def append_to_file(file_path: str, content: str) -> str:
    """Append content to the end of a file"""
    try:
        file_name = Path(file_path).name
        if file_name in PROTECTED_FILES:
            return f"Error: {file_name} is protected and cannot be modified"
        
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
        
        return f"Successfully appended to {file_path}"
        
    except Exception as e:
        return f"Error appending to file: {str(e)}"

def find_in_file(file_path: str, pattern: str, context_lines: int = 3) -> str:
    """Search for text in a file and return matches with context"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        matches = []
        for i, line in enumerate(lines):
            if pattern in line:
                # Get context around the match
                start_idx = max(0, i - context_lines)
                end_idx = min(len(lines), i + context_lines + 1)
                
                context = []
                for j in range(start_idx, end_idx):
                    prefix = ">>> " if j == i else "    "
                    context.append(f"{prefix}{j+1:4d}: {lines[j].rstrip()}")
                
                matches.append(f"Match at line {i+1}:\n" + "\n".join(context))
        
        if not matches:
            return f"No matches found for '{pattern}' in {file_path}"
        
        return f"Found {len(matches)} match(es) in {file_path}:\n\n" + "\n\n".join(matches)
        
    except Exception as e:
        return f"Error searching file: {str(e)}"

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
