"""Command utilities for the MCP server"""
import subprocess
import os

def run_command_in_directory(command: list, cwd: str = "/Users/diegowahl/mcp-server") -> str:
    """Run a shell command in a specific directory"""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
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

def reinstall_mcp_server() -> str:
    """Reinstall this MCP server (useful after making changes)"""
    return run_command_in_directory(["uv", "run", "mcp", "install", "server.py"])
