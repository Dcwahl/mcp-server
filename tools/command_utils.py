"""Command utilities for the MCP server"""
import subprocess
import os
import shutil

def run_command_in_directory(command: list, cwd: str = "/Users/diegowahl/mcp-server", env: dict = None) -> str:
    """Run a shell command in a specific directory"""
    try:
        # Use current environment and add to it if needed
        if env is None:
            env = os.environ.copy()
        
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60,
            env=env
        )
        
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        
        if result.returncode == 0:
            return "\n".join(output) if output else "Command completed successfully"
        else:
            return f"Command failed (exit code {result.returncode}):\n" + "\n".join(output)
            
    except subprocess.TimeoutExpired:
        return "Error: Command timed out"
    except Exception as e:
        return f"Error running command: {str(e)}"

def find_uv_path() -> str:
    """Find the full path to uv executable"""
    # Try to find uv in common locations
    possible_paths = [
        "/Users/diegowahl/.local/bin/uv",  # Default uv install location
        shutil.which("uv"),  # Try to find in PATH
        "/opt/homebrew/bin/uv",  # Homebrew location
        "/usr/local/bin/uv"  # Other common location
    ]
    
    for path in possible_paths:
        if path and os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    
    return "uv"  # Fallback to just "uv"

def reinstall_mcp_server() -> str:
    """Reinstall this MCP server (useful after making changes)"""
    uv_path = find_uv_path()
    
    # Create environment with extended PATH
    env = os.environ.copy()
    additional_paths = [
        "/Users/diegowahl/.local/bin",
        "/opt/homebrew/bin", 
        "/usr/local/bin"
    ]
    
    current_path = env.get("PATH", "")
    for path in additional_paths:
        if path not in current_path:
            current_path = f"{path}:{current_path}"
    env["PATH"] = current_path
    
    return run_command_in_directory([uv_path, "run", "mcp", "install", "server.py"], env=env)
