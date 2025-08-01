# Current Development Objective

## Goal: Tool Registry Architecture Redesign

We're planning a significant architectural improvement to move from our current function-based MCP tools to a class-based tool registry system, inspired by Serena's sophisticated architecture.

## What We Learned from Serena Analysis

**Serena's Strengths We Want to Adopt:**
1. **Class-Based Tool System** - Each tool inherits from `Tool` base class with `apply()` method
2. **Tool Registry** - Centralized discovery and management of tools
3. **Context/Mode System** - Different tool sets for different workflows (exploration, debugging, refactoring)
4. **Memory Management** - Persistent project understanding across sessions
5. **Smart Caching** - Content-hash based caching for expensive operations

**What We'll Skip:**
- Full LSP integration (too complex for our scope)
- Multi-language support initially (stay Python-focused)
- GUI dashboard (MCP provides UI integration)

## Current State Assessment

**What Works Well:**
- Basic file operations (read, write, patch, find)
- Git integration with safety features
- AST-based code analysis (analyze_file_structure, get_project_overview)
- Self-updating server capability
- Comprehensive documentation and context management

**What Needs Improvement:**
- Function-based tools are harder to compose and extend
- No persistent memory between sessions
- No caching strategy for expensive operations
- Limited contextual workflow support
- AST tools need better cross-file reference tracking

## Planned Architecture Changes

### Phase 1: Tool Registry Foundation
- [ ] Create `Tool` base class with standardized interface
- [ ] Implement `ToolRegistry` for tool discovery and management
- [ ] Convert existing file operations to class-based tools
- [ ] Convert git operations to class-based tools
- [ ] Convert AST analysis tools to class-based tools

### Phase 2: Context & Memory Systems
- [ ] Implement context system (exploration, debugging, refactoring modes)
- [ ] Create memory management for persistent project insights
- [ ] Add tool filtering based on active context
- [ ] Implement cross-session state persistence

### Phase 3: Caching Strategy
- [ ] Content-hash based caching for AST analysis
- [ ] Cache project overviews and file structures
- [ ] Implement cache invalidation on file changes
- [ ] Add performance metrics and cache hit rates

### Phase 4: Enhanced Code Analysis
- [ ] Improve cross-file reference tracking
- [ ] Add symbol dependency mapping
- [ ] Implement intelligent context gathering
- [ ] Create code pattern recognition tools

## Success Criteria

**Technical:**
- Tool registration is automatic and discoverable
- Tools can be composed into workflows
- Performance improves through caching
- Memory system maintains useful context

**User Experience:**
- New chat sessions have relevant project context
- Tools adapt to the type of work being done
- Common workflows become more efficient
- Better code understanding for complex projects

## Files to Monitor During Development

**Core Implementation:**
- `server.py` - Main MCP server registration
- `tools/tool_registry.py` - New tool management system
- `tools/base_tool.py` - Base tool class definition
- `tools/memory_manager.py` - Context persistence system

**Documentation Updates:**
- `CURRENT_OBJECTIVE.md` - This file
- `CHAT_CONTEXT.md` - Session startup guide
- `DEV_GUIDE.md` - Development patterns
- `README.md` - Main documentation

## Testing Strategy

**Manual Testing:**
- Test tool registry with existing workflows
- Validate memory persistence across sessions
- Verify caching improves performance
- Ensure backward compatibility during transition

**Integration Testing:**
- All existing tools work through new registry
- MCP server registration handles class-based tools
- Tool discovery and execution is reliable
- Memory loading/saving is robust

## Risk Mitigation

**Backward Compatibility:**
- Keep function wrappers during transition
- Gradual migration of tools to new system
- Fallback mechanisms for tool failures

**Complexity Management:**
- Start with simple base classes
- Add features incrementally
- Maintain clear separation of concerns
- Document design decisions thoroughly

## Next Steps

1. **Design Review** - Finalize tool base class interface
2. **Foundation Building** - Implement core registry system
3. **Migration Planning** - Strategy for converting existing tools
4. **Testing Framework** - Ensure reliability during transition

---

*This objective represents a significant architectural improvement that will make our MCP server more extensible, performant, and user-friendly while learning from proven patterns in the Serena codebase.*
