#!/usr/bin/env python3
"""
Test script for the new tool registry system.

This script tests the class-based tools and caching functionality
to ensure everything works before we switch over.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/Users/diegowahl/mcp-server')

def test_tool_registry():
    """Test the tool registry system"""
    print("=== Testing Tool Registry System ===\n")
    
    try:
        # Import the registry
        from tools.base_tool import registry
        from tools import file_tools, ast_tools
        
        print("✅ Successfully imported registry and tools")
        
        # List registered tools
        tools = registry.list_tools()
        print(f"✅ Found {len(tools)} registered tools:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
        
        print()
        
        # Test a simple file operation
        print("=== Testing File Operations ===")
        
        # Test read_file tool
        result = registry.execute_tool("read_file", file_path="/Users/diegowahl/mcp-server/README.md")
        print(f"✅ read_file executed successfully ({len(result)} chars)")
        
        # Test it again to check caching
        result2 = registry.execute_tool("read_file", file_path="/Users/diegowahl/mcp-server/README.md")
        print(f"✅ read_file executed again (should be cached)")
        
        # Test list_directory
        result = registry.execute_tool("list_directory", directory_path="/Users/diegowahl/mcp-server")
        print(f"✅ list_directory executed successfully")
        
        print()
        
        # Test cache statistics
        print("=== Testing Cache System ===")
        from tools.cache_manager import cache_manager
        stats = cache_manager.get_stats()
        print(f"✅ Cache stats: {stats}")
        
        print()
        
        # Test AST analysis (expensive operation that benefits from caching)
        print("=== Testing AST Analysis ===")
        
        # Test analyze_file_structure
        result = registry.execute_tool("analyze_file_structure", 
                                     file_path="/Users/diegowahl/mcp-server/server.py")
        print(f"✅ analyze_file_structure executed successfully")
        
        # Test it again to verify caching
        result2 = registry.execute_tool("analyze_file_structure", 
                                      file_path="/Users/diegowahl/mcp-server/server.py")
        print(f"✅ analyze_file_structure executed again (should be cached)")
        
        # Check cache performance
        stats = cache_manager.get_stats()
        print(f"✅ Updated cache stats: {stats}")
        
        print("\n=== All Tests Passed! ===")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_context_filtering():
    """Test context-based tool filtering"""
    print("\n=== Testing Context Filtering ===")
    
    try:
        from tools.base_tool import registry
        
        # Test different contexts
        contexts = ["general", "exploration", "debugging", "refactoring"]
        
        for context in contexts:
            tools = registry.list_tools(context=context)
            print(f"✅ Context '{context}': {len(tools)} tools available")
            
        return True
        
    except Exception as e:
        print(f"❌ Context filtering test failed: {e}")
        return False


if __name__ == "__main__":
    print("MCP Development Server - Tool Registry Test\n")
    
    success = True
    
    # Run tests
    success &= test_tool_registry()
    success &= test_context_filtering()
    
    if success:
        print("\n🎉 All tests passed! The tool registry system is working correctly.")
        print("\nNext steps:")
        print("1. Update server.py to use server_enhanced.py")
        print("2. Run reinstall_server to update MCP registration")
        print("3. Hard restart Claude Desktop")
        print("4. Start new chat session to test")
    else:
        print("\n💥 Some tests failed. Check the errors above.")
        sys.exit(1)
