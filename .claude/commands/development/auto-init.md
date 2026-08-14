# Auto-Init - Automatic Project Initialization with Archon RAG & Serena

## Purpose
Automatically initialize AI assistant with complete project context, leveraging Archon knowledge base and Serena semantic search.

## Execution

### Step 1: Connect to MCP Servers
Silently connect to available MCP servers (Serena, Archon, Filesystem).

### Step 2: Query Archon Knowledge Base FIRST (CRITICAL)
**BEFORE analyzing local files, retrieve context from Archon:**

**Archon RAG Queries:**
```
1. "Retrieve all stored documentation for [language from PROJECT_INFO]"
   - Gets: Pytest, Pydantic, Maestro, framework docs you've stored
   
2. "Search knowledge base for [framework] best practices and patterns"
   - Gets: Implementation patterns, coding standards
   
3. "Find past architectural decisions for similar projects"
   - Gets: Why certain tech choices were made
   
4. "Retrieve common gotchas and solutions for [tech stack]"
   - Gets: Lessons learned, known issues
   
5. "Get team conventions and coding standards"
   - Gets: Established patterns, naming conventions
```

**Example Archon queries based on your knowledge base:**
- "Retrieve Pytest documentation patterns"
- "Get Pydantic validation examples" 
- "Find Maestro orchestration patterns"
- "Search for ReactNative best practices"

### Step 3: Load Project Information
Read and understand:
- `PROJECT_INFO.md` - Project details
- `CLAUDE.md` - AI assistant rules
- `README.md` - Project overview

### Step 4: Use Serena for Semantic Code Search
**Search codebase semantically (not just keywords):**
```
- Find authentication implementations
- Locate validation patterns
- Discover error handling approaches
- Identify testing strategies
- Search for similar feature implementations
```

### Step 5: Analyze Project Structure
Run `tree -L 3 -I 'node_modules|__pycache__|.git|dist|build'`

### Step 6: Synthesize Context
Combine:
- Archon stored knowledge (your docs)
- Serena code patterns (existing implementations)
- Local project files
- Project structure

### Step 7: Provide Comprehensive Summary

```
✓ Initialized successfully!

Project: [Name from PROJECT_INFO]
Language: [Primary language]
Framework: [Main framework]

MCP Servers Connected:
- Serena: ✓ (Semantic search ready)
- Archon: ✓ (Knowledge base: 7 items found)
- Filesystem: ✓

Archon Knowledge Retrieved:
- Pytest Documentation (1939 chunks)
- Pydantic Documentation (1060 chunks)
- Maestro Documentation (1032 chunks)
- [Other docs...]

Key Patterns Found (via Serena):
- [Authentication pattern in src/auth/]
- [Validation pattern in src/models/]
- [Testing pattern in tests/]

Project Structure:
[Directory listing]

Ready to help with full context from:
✓ Your stored documentation (Archon)
✓ Existing code patterns (Serena)
✓ Project conventions (local files)

What would you like to work on?
```

## Notes
- This command runs automatically on startup
- **Always queries Archon BEFORE local analysis**
- **Always uses Serena for semantic code understanding**
- Silently handles MCP connection failures
- References your stored docs for accurate code generation
