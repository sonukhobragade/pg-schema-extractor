# Prime Core - Deep Codebase Understanding with Archon RAG & Serena

## Purpose
Develop comprehensive understanding of project architecture, patterns, and conventions using Archon knowledge base and Serena semantic search.

## Process

### Step 1: Query Archon Knowledge Base FIRST
**CRITICAL: Retrieve stored documentation BEFORE analyzing code**

**Archon RAG Queries:**
```
"Retrieve all [framework] documentation from knowledge base"
"Get stored [language] best practices and patterns"
"Find architectural decision records"
"Search for implementation examples in stored docs"
"Retrieve testing patterns and strategies"
"Get error handling conventions from docs"
```

**Based on PROJECT_INFO.md, query specifically:**
- If Python: "Retrieve Pytest documentation", "Get Pydantic patterns"
- If JavaScript: "Get React patterns", "Retrieve Node.js best practices"
- If using Maestro: "Retrieve Maestro orchestration patterns"

### Step 2: Project Structure Analysis
```bash
tree -L 3 -I 'node_modules|__pycache__|.git|dist|build'
```

### Step 3: Read Key Files
- `CLAUDE.md` - AI rules and conventions
- `PROJECT_INFO.md` - Project details
- `README.md` - Project overview
- Main entry point (main.py, index.ts, main.go, etc.)
- Configuration files (package.json, pyproject.toml, go.mod, etc.)

### Step 4: Use Serena for Semantic Code Search
**CRITICAL: Use Serena to find patterns, not just grep**

**Serena Semantic Queries:**
```
"Find authentication implementations"
"Locate database connection patterns"
"Search for validation approaches"
"Find error handling patterns"
"Discover testing strategies"
"Identify API endpoint patterns"
"Find dependency injection examples"
"Locate configuration management"
```

**Cross-reference Serena findings with Archon docs:**
- Found auth pattern → Check Archon for auth best practices
- Found validation → Cross-reference with Pydantic docs in Archon
- Found testing → Compare with Pytest patterns in Archon

### Step 5: Dependency Analysis
Analyze:
- Critical dependencies and their purpose
- Development dependencies
- Version constraints

**Query Archon for each major dependency:**
```
"Retrieve [library-name] documentation and usage patterns"
"Get best practices for [dependency]"
"Find common gotchas with [library]"
```

### Step 6: Architecture Understanding
Identify:
- Project architecture (MVC, Clean Architecture, etc.)
- Module organization
- Data flow
- Integration points

**Use Serena to find:**
- Service layer patterns
- Repository patterns
- Controller/handler patterns
- Model definitions

**Cross-reference with Archon:**
- Compare found patterns with stored best practices
- Check architectural decisions
- Validate against team conventions

### Step 7: Synthesize Complete Picture

## Output Format

```
Project Architecture Summary
============================

Archon Knowledge Base Context:
✓ Retrieved: Pytest Documentation (1939 chunks)
✓ Retrieved: Pydantic Documentation (1060 chunks)
✓ Retrieved: Maestro Documentation (1032 chunks)
✓ Retrieved: [Framework] best practices
✓ Retrieved: Past architectural decisions

Structure (via tree):
src/
├── api/          # API routes and endpoints
├── models/       # Data models (Pydantic-based per Archon docs)
├── services/     # Business logic
├── tests/        # Tests (Pytest-based per Archon docs)
└── utils/        # Utilities

Key Components (via Serena semantic search):
- Authentication: src/api/auth.py
  Pattern: JWT-based, matches best practices from Archon
- Validation: src/models/*.py
  Pattern: Pydantic models, follows Archon documentation
- Testing: tests/*
  Pattern: Pytest fixtures and parametrization per Archon docs
- Error Handling: Custom exceptions in src/exceptions.py
  Pattern: Matches error handling best practices from Archon

Patterns & Conventions (Serena + Archon):
Coding Patterns:
- Async/await for I/O operations (Archon best practice)
- Pydantic for data validation (per stored Pydantic docs)
- Dependency injection via FastAPI (per Archon FastAPI patterns)

Naming Conventions:
- Files: snake_case
- Functions: snake_case verbs
- Classes: PascalCase nouns
- (Matches conventions from Archon knowledge base)

Testing Approach:
- Pytest with fixtures (per Archon Pytest documentation)
- Parametrized tests (Pytest best practice from Archon)
- Test coverage >80% (team standard from Archon)

Dependencies (cross-referenced with Archon):
✓ FastAPI 0.104.1 - Web framework
  Archon context: Retrieved FastAPI patterns and best practices
✓ Pydantic 2.5.0 - Data validation
  Archon context: Retrieved validation patterns and examples
✓ Pytest 7.4.0 - Testing
  Archon context: Retrieved testing strategies and fixtures
✓ SQLAlchemy 2.0.0 - Database ORM
  Archon context: Retrieved ORM patterns

Entry Points:
- main.py: FastAPI application initialization
- Follows pattern from Archon FastAPI docs

Development Setup (cross-referenced with Archon):
- Install: uv sync (per Archon Python best practices)
- Run: uvicorn main:app --reload
- Test: pytest (configured per Archon Pytest docs)
- Lint: ruff check --fix (per Archon standards)

Serena Pattern Insights:
Found 15 authentication-related implementations
Found 23 Pydantic validation patterns
Found 45 test fixtures (following Archon Pytest patterns)
Found 8 error handling patterns (matching Archon conventions)

Recommendations Based on Archon + Serena:
1. Current auth pattern matches Archon best practices ✓
2. Pydantic usage aligns with stored documentation ✓
3. Testing strategy follows Archon Pytest patterns ✓
4. Consider adding: [suggestions based on gaps vs Archon docs]

Notes:
- All patterns validated against Archon knowledge base
- Code patterns cross-referenced with stored documentation
- Conventions match team standards from Archon
- Ready to implement following established patterns
```

## Usage Notes

**This command:**
1. **ALWAYS queries Archon FIRST** to get your stored documentation
2. **Uses Serena for semantic understanding** of existing code
3. **Cross-references findings** between Archon docs and actual code
4. **Validates patterns** against your knowledge base
5. **Provides context-aware recommendations** based on YOUR docs

**Result:** You get deep understanding grounded in YOUR documentation and YOUR codebase patterns, not generic advice.

## When to Use
- First time in a new project
- After being away from project
- Before implementing significant features
- When you need to refresh on established patterns
- When onboarding new team members
