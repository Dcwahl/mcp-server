"""Git utilities for the MCP server"""
import subprocess
import os
from pathlib import Path

def run_git_command(command: list, cwd: str = "/Users/diegowahl/mcp-server") -> str:
    """Run a git command safely"""
    try:
        # For write operations, don't check if we're in a git repo first (git init needs to work)
        if len(command) > 1 and command[1] == "init":
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
        else:
            # Check if we're in a git repository for other commands
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                return f"Error: Not in a git repository (checked {cwd})"
            
            # Run the actual command
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
        
        if result.returncode == 0:
            return result.stdout.strip() if result.stdout else "Command completed successfully"
        else:
            return f"Git error: {result.stderr.strip()}"
            
    except subprocess.TimeoutExpired:
        return "Error: Git command timed out"
    except Exception as e:
        return f"Error running git command: {str(e)}"

def get_current_branch() -> str:
    """Get the current git branch name"""
    result = run_git_command(["git", "branch", "--show-current"])
    if result.startswith("Error"):
        return ""
    return result.strip()

# Read-only operations
def get_git_status() -> str:
    """Get the current git status"""
    result = run_git_command(["git", "status", "--porcelain", "-b"])
    if result.startswith("Error"):
        return result
    
    lines = result.split('\n')
    if not lines or not lines[0]:
        return "Working directory clean"
    
    # Parse the branch info and changes
    output = []
    for line in lines:
        if line.startswith('##'):
            branch_info = line[3:]
            output.append(f"Branch: {branch_info}")
        elif line:
            status = line[:2]
            filename = line[3:]
            status_map = {
                'M ': 'Modified (staged)',
                ' M': 'Modified (unstaged)',
                'A ': 'Added',
                'D ': 'Deleted (staged)',
                ' D': 'Deleted (unstaged)',
                '??': 'Untracked',
                'R ': 'Renamed',
                'C ': 'Copied'
            }
            status_desc = status_map.get(status, f'Status: {status}')
            output.append(f"{status_desc}: {filename}")
    
    return '\n'.join(output)

def get_git_branch() -> str:
    """Get current branch and list all branches"""
    current = run_git_command(["git", "branch", "--show-current"])
    if current.startswith("Error"):
        return current
    
    all_branches = run_git_command(["git", "branch", "-a"])
    if all_branches.startswith("Error"):
        return f"Current branch: {current}\nError getting all branches: {all_branches}"
    
    return f"Current branch: {current}\n\nAll branches:\n{all_branches}"

def get_git_log(limit: int = 10) -> str:
    """Get recent commit history"""
    command = ["git", "log", f"--max-count={limit}", "--oneline", "--graph", "--decorate"]
    return run_git_command(command)

# Write operations
def do_git_add(files: str) -> str:
    """Add files to git staging area. Use '.' for all files"""
    if files.strip() == "":
        return "Error: No files specified"
    return run_git_command(["git", "add", files])

def do_git_commit(message: str) -> str:
    """Commit staged changes with a message"""
    if not message or len(message.strip()) < 5:
        return "Error: Commit message must be at least 5 characters"
    return run_git_command(["git", "commit", "-m", message])

def do_git_push(branch: str = None) -> str:
    """Push commits to remote. Blocks pushes to main branch for safety."""
    # Get current branch if no branch specified
    if branch is None:
        current_branch = get_current_branch()
        if not current_branch:
            return "Error: Could not determine current branch"
        
        # Block pushing to main
        if current_branch.lower() in ['main', 'master']:
            return f"Error: Pushing to {current_branch} branch is blocked for safety. Please create a feature branch or specify a different branch explicitly."
        
        return run_git_command(["git", "push"])
    else:
        # Block explicit pushes to main
        if branch.lower() in ['main', 'master']:
            return f"Error: Pushing to {branch} branch is blocked for safety. Use a feature branch instead."
        
        return run_git_command(["git", "push", "origin", branch])

def do_git_checkout(branch_name: str, create_new: bool = False) -> str:
    """Checkout existing branch or create new one"""
    if not branch_name or len(branch_name.strip()) < 1:
        return "Error: Branch name required"
    
    if create_new:
        return run_git_command(["git", "checkout", "-b", branch_name])
    else:
        return run_git_command(["git", "checkout", branch_name])

def get_git_diff() -> str:
    """Show diff of unstaged changes"""
    return run_git_command(["git", "diff"])

def get_git_diff_staged() -> str:
    """Show diff of staged changes"""
    return run_git_command(["git", "diff", "--staged"])
