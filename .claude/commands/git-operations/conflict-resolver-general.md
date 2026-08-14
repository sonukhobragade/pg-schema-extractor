# Conflict Resolver

Systematic merge conflict resolution with context understanding.

## Usage
/conflict-resolver-general

## Process with RAG

1. **Analyze conflicts:** `git diff --name-only --diff-filter=U`

2. **Query Archon:** Get coding standards and patterns

3. **Use Serena:** Find how similar code is written in project

4. **For each conflict:**
   - Understand both sides
   - Check against Archon best practices
   - Validate against Serena patterns
   - Propose resolution

5. **Validate resolution:**
   - Syntax check
   - Pattern consistency
   - Test execution

## Output
Resolved conflicts with explanation of choices made.
