---
name: start-feature
description: Create feature branch and Archon task in one command
---

# Start Feature

Create feature branch and Archon task automatically to begin work.

## Usage
/start-feature "feature description"

## What This Does

1. **Creates Archon Task**
   - Title: [feature description]
   - Status: todo → in-progress
   - Project: your-project
   - Returns TASK-ID

2. **Creates Git Branch**
   - Format: `feature/TASK-ID-description`
   - Example: `feature/TASK-123-add-login-flows`
   - Checks out new branch

3. **Links Branch to Task**
   - Stores branch name in Archon task
   - Ready for tracking

## Output Example

```
✓ Created Archon Task: TASK-123
  Title: Add login flows for new and existing users
  Status: in-progress
  Project: your-project
  View: http://localhost:3737/tasks/TASK-123

✓ Created Branch: feature/TASK-123-add-login-flows
✓ Checked out branch

Ready to code!

When done:
1. /review-general
2. /smart-commit → auto-links to TASK-123
3. /create-pr → marks TASK-123 complete
```

## Complete Workflow

```bash
# Start
/start-feature "add login flows for new and existing users"
# ✓ TASK-123 created (in-progress)
# ✓ Branch: feature/TASK-123-add-login-flows

# Code your feature
# ... create maestro flows, tests ...

# Commit (auto-links to TASK-123)
/smart-commit

# Push
git push origin feature/TASK-123-add-login-flows

# Complete (marks TASK-123 done)
/create-pr
```

## Benefits

- **One command** - Branch + Task creation
- **Auto-linking** - Task linked to branch
- **Auto-tracking** - Commits reference TASK-123
- **Clean workflow** - Everything connected
