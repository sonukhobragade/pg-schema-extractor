# Review General with Archon RAG & Serena

## Purpose
Comprehensive code review using Archon best practices and Serena patterns as validation baseline.

## Review Process

### Step 1: Identify Changes
```bash
git diff
```

### Step 2: Query Archon for Standards

**Retrieve quality standards from YOUR knowledge base:**
```
"Retrieve code quality best practices for [language]"
"Get security guidelines from knowledge base"  
"Find testing standards"
"Retrieve performance best practices"
"Get documented coding conventions"
```

### Step 3: Use Serena to Find Project Patterns

**Discover how YOUR project does things:**
```
"Find error handling patterns in codebase"
"Search for validation approaches"
"Locate testing patterns"
"Find security implementations"
"Discover naming conventions"
```

### Step 4: Review Against Archon + Serena

#### Code Quality
**Validate against Archon docs:**
- [ ] Follows best practices from Archon knowledge base
- [ ] Uses patterns documented in Archon
- [ ] Avoids anti-patterns documented in Archon

**Validate against Serena patterns:**
- [ ] Matches naming conventions (found in X files via Serena)
- [ ] Follows file organization (discovered via Serena)
- [ ] Uses same error handling pattern (found in Y files)

#### Security
**Check against Archon security docs:**
- [ ] No secrets (per Archon security guidelines)
- [ ] Input validation (per Archon validation patterns)
- [ ] SQL injection prevention (per Archon database docs)

**Compare with Serena findings:**
- [ ] Uses same auth pattern as existing code
- [ ] Matches validation approach found in project

#### Error Handling
**Archon validation:**
- [ ] Follows error handling from Archon docs

**Serena validation:**
- [ ] Matches error pattern found in 15 files
- [ ] Uses same exception types as project

#### Performance
**Archon benchmarks:**
- [ ] Meets performance standards from Archon

**Serena comparison:**
- [ ] Similar complexity to existing implementations

#### Testing
**Archon standards:**
- [ ] Coverage meets Archon requirements
- [ ] Uses test patterns from Archon (Pytest/Jest docs)

**Serena patterns:**
- [ ] Test structure matches 23 existing test files
- [ ] Fixture usage consistent with project

## Output Format

### 🔴 Critical Issues (Must Fix)
[Issues violating Archon security/quality standards or breaking Serena patterns]

**Example:**
```
1. SQL Injection Risk - auth.py:45
   Violates: Archon security guidelines (chunk 234)
   Project pattern: All 12 database files use parameterized queries (Serena)
   Fix: Use parameterized query like src/db/users.py:67
```

### 🟡 Warnings (Should Fix)
[Deviations from Archon best practices or inconsistent with Serena patterns]

### 🟢 Suggestions (Consider)
[Improvements based on Archon docs or better Serena patterns]

### 📊 Summary
```
Files reviewed: X
Archon validations: Y passed, Z failed
Serena pattern matches: A/B files consistent
Overall: [Excellent/Good/Needs Work]

Context used:
- Archon docs: [list retrieved]
- Serena patterns: [list found]
```

## When to Use
- After implementation, before commit
- During PR review
- When ensuring code quality matches YOUR standards
