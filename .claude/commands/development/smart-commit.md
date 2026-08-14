---
name: smart-commit  
description: Generate conventional commit with automatic Archon task updates
---

# Smart Commit with Task Tracking

Generate commit message and auto-update linked Archon tasks.

## Usage
/smart-commit

## Process

### Step 1: Analyze Changes
```bash
git diff --staged
# Analyze all staged changes
```

### Step 2: Check for Linked Tasks

```
Search staged files for:
- PRP files with task_id in frontmatter
- Previous commits with "TASK-" references
- Current branch name (if contains TASK-)

If found: Extract TASK-123 for linking
```

### Step 3: Generate Commit Message

```
Type: feat/fix/docs/test/refactor
Scope: Affected module
Description: What changed

If task found, append:
Relates-to: TASK-123
```

### Step 4: Show for Approval

```
Proposed commit message:
---
feat(auth): add JWT authentication with refresh tokens

- Implement User model with Pydantic validation
- Add login/logout endpoints
- Include comprehensive test coverage

Relates-to: TASK-123
---

Commit? (y/n)
```

### Step 5: Commit and Update Task

```
If approved:

1. git commit -m "[message]"

2. Use Archon MCP to update TASK-123:
   - Add commit SHA
   - Add commit message
   - Add files modified
   - Keep status: "review"
   - Add timestamp
```

## Output

```
✓ Committed: abc123d
  feat(auth): add JWT authentication

✓ Updated Archon Task: TASK-123
  Added commit: abc123d
  Files: src/models/user.py, tests/test_auth.py
  Status: review (ready for code review)

View in Archon: http://localhost:3737/tasks/TASK-123

Next: /review-general or /create-pr
```

## Auto-Linking

Commits are automatically linked to tasks when:
- Working on PRP with task_id
- Branch name contains TASK-123
- Previous commit mentioned TASK-123

## Manual Task Reference

You can manually specify:
```
/smart-commit TASK-456
# Forces link to specific task
```

## Without Archon

If Archon not available:
- Still generates good commit message
- Just skips task updating
- Warns: "Archon not connected"
