#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/diegowahl/mcp-server')

try:
    from tools.base_tool import registry, Tool, ToolMetadata
    print("✅ Successfully imported base_tool components")
    
    from tools import file_tools
    print("✅ Successfully imported file_tools")
    
    from tools import ast_tools  
    print("✅ Successfully imported ast_tools")
    
    # Test registry
    tools = registry.list_tools()
    print(f"✅ Registry has {len(tools)} tools registered")
    
    for tool in tools:
        print(f"   - {tool.name}: {tool.category}")
        
    # Test a simple execution
    result = registry.execute_tool("read_file", file_path="/Users/diegowahl/mcp-server/README.md")
    print(f"✅ Tool execution successful: {len(result)} characters read")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
