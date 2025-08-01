# MCP Development Server

A powerful local development toolkit that extends any MCP-compatible AI model with file operations, git integration, and command utilities. Works with Claude, custom models, or any MCP client.

## 🚀 New Chat Sessions - Start Here!

**For AI assistants starting a new conversation with this project:**

Run these commands immediately to get full context:
```bash
list_tools      # See all available MCP tools
project_status  # Get current project overview  
show_examples   # View common usage patterns
git_status      # Check repository state
```

**Quick Context Files:**
- `CHAT_CONTEXT.md` - Essential session startup information
- `DEV_GUIDE.md` - Development patterns and workflows
- `session_starter.py` - Reference script with key project info

## Quick Start

### With Claude Desktop
```bash
uv run mcp install server.py
```

### With Custom MCP Client
```bash
# Start server in stdio mode
uv run python server.py

# Or via MCP dev server
uv run mcp dev server.py
```
TODO: dunno how true any of this section is

### Self-Updating (any client)
Use the `reinstall_server` tool from within your AI assistant

## Tool Categories

### 📁 File Operations
| Tool | Purpose | Safety Features |
|------|---------|----------------|
| `read_file` | Read entire file | - |
| `read_lines` | Read specific line ranges | Efficient for large files |
| `write_file` | Overwrite entire file | Auto-backup, protected files list |
| `patch_file` | Find & replace specific text | Auto-backup, prevents ambiguous matches |
| `append_file` | Add to end of file | Protected files list |
| `find_in_file` | Search with context | Shows surrounding lines |
| `find_files` | Search by pattern | Supports glob patterns like `*.py` |
| `list_directory` | List contents | Shows file sizes |

### 🔧 Git Operations
| Tool | Purpose | Safety Features |
|------|---------|----------------|
| `git_status` | Show repo status | Read-only |
| `git_branch` | List branches | Read-only |
| `git_log` | Show commit history | Read-only |
| `git_diff` | Show unstaged changes | Read-only |
| `git_diff_staged` | Show staged changes | Read-only |
| `git_add` | Stage files | Requires explicit file list |
| `git_commit` | Commit changes | Requires 5+ char message |
| `git_push` | Push to remote | **BLOCKS pushes to main/master** |
| `git_checkout` | Switch/create branches | Safe branch operations |

### ⚙️ System Operations
| Tool | Purpose | Notes |
|------|---------|-------|
| `reinstall_server` | Update MCP server | Auto-detects uv path |

## Safety Features

### File Protection
- **Protected files**: `pyproject.toml`, `uv.lock`, `.gitignore`, `.git`, `__pycache__`
- **Automatic backups**: All file modifications create `.backup` files
- **Ambiguity prevention**: `patch_file` errors if multiple matches found

### Git Protection
- **Main branch protection**: Cannot push to `main` or `master` branches
- **Explicit confirmation**: Use UI single-use approval for sensitive operations
- **Branch safety**: Encourages feature branch workflow

## Common Workflows

### Adding a new tool
```python
# 1. Add utility function to appropriate utils file
# 2. Import in server.py
# 3. Add @mcp.tool() wrapper
# 4. Use reinstall_server tool
# 5. Hard restart Claude Desktop (critical!)
# 6. Start new chat session to verify tools appear
```

### Safe development workflow
```bash
# 1. Create feature branch
git_checkout("feature/new-feature", create_new=True)

# 2. Make changes using patch_file instead of write_file
patch_file("server.py", old_code, new_code)

# 3. Commit and push to feature branch
git_add(".")
git_commit("Add new feature")
git_push()  # Safe - not on main branch

# 4. Merge via GitHub PR (manual step)
```

## Roadmap & Vision

### Current State
- ✅ Core file operations with safety features
- ✅ Git integration with branch protection
- ✅ Self-updating server capabilities
- ✅ Works with Claude Desktop

### Planned Features
- 🔄 **Orchestrator/Worker Architecture**: Multi-agent workflows with task delegation
- 🔄 **Model Agnostic**: Swap between Claude, GPT, local models, custom fine-tunes
- 🔄 **Custom UI**: Web interface for direct model interaction
- 🔄 **Advanced Workflows**: Automated code review, testing, deployment pipelines
- 🔄 **Plugin System**: Extensible architecture for domain-specific tools

### Architecture Goals
- **Model Independence**: Works with any MCP-compatible AI model
- **UI Flexibility**: CLI, web interface, or integrate with existing tools
- **Orchestration Ready**: Foundation for multi-agent collaborative workflows
- **Enterprise Ready**: Security, logging, access controls for team usage