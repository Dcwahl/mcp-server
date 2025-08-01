#!/usr/bin/env python3
"""
Session Starter - Quick context setup for new AI chat sessions
Run this to get oriented in the MCP Development Server project
"""

CONTEXT_COMMANDS = [
    "list_tools",      # See all available MCP tools  
    "project_status",  # Get current project overview
    "show_examples",   # View common usage patterns
    "git_status"       # Check repository state
]

PROJECT_INFO = {
    "name": "MCP Development Server",
    "location": "/Users/diegowahl/mcp-server", 
    "description": "Comprehensive AI development toolkit with file ops, git integration, safety features",
    "files": "1000+ Python files",
    "key_features": [
        "Self-updating MCP server",
        "Safe file editing with backups", 
        "Git workflow with main branch protection",
        "Modular tool architecture"
    ]
}

QUICK_REFERENCE = {
    "file_editing": "Use patch_file instead of write_file when possible",
    "git_workflow": "Create feature branches, main branch is protected", 
    "server_updates": "Use reinstall_server after code changes",
    "finding_code": "Use find_in_file and find_files for navigation"
}

if __name__ == "__main__":
    print("=== MCP Development Server - Session Starter ===\n")
    
    print("🚀 PROJECT INFO:")
    print(f"  Name: {PROJECT_INFO['name']}")
    print(f"  Location: {PROJECT_INFO['location']}")
    print(f"  Files: {PROJECT_INFO['files']}")
    print(f"  Description: {PROJECT_INFO['description']}\n")
    
    print("🔧 KEY FEATURES:")
    for feature in PROJECT_INFO['key_features']:
        print(f"  • {feature}")
    print()
    
    print("⚡ ESSENTIAL COMMANDS TO RUN:")
    for cmd in CONTEXT_COMMANDS:
        print(f"  {cmd}")
    print()
    
    print("💡 QUICK REFERENCE:")
    for key, value in QUICK_REFERENCE.items():
        print(f"  {key}: {value}")
    print()
    
    print("📖 READ THESE FILES:")
    print("  • README.md - Comprehensive documentation")
    print("  • CHAT_CONTEXT.md - Quick session startup guide") 
    print("  • DEV_GUIDE.md - Development patterns and workflows")
