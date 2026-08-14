---
name: create-pr
description: Generate PR with automatic Archon task completion
---

# Create Pull Request with Task Completion

Generate comprehensive PR description and mark Archon task as done.

## Usage
/create-pr

## Process

### Step 1: Analyze Changes
```bash
git diff main...HEAD
git log main..HEAD --oneline
```

### Step 2: Find Linked Tasks

```
Search commits for:
- "Relates-to: TASK-123"
- "TASK-" references
- Check branch name

Extract all linked task IDs
```

### Step 3: Query Archon for Task Details

```
For each TASK-ID found:
- Get task title and description
- Get implementation notes
- Get files modified
- Get time spent
```

### Step 4: Generate PR Description

```markdown
## Summary
[Feature description from task]

## Related Tasks
- Closes TASK-123: [Task title]
- Closes TASK-124: [Task title]

## Changes
- [List from commits and task notes]

## Implementation Notes
[From Archon task notes]

## Testing
- [Tests added/modified]
- All validation gates passed

## Type of Change
- [x] New feature
- [ ] Bug fix
- [ ] Breaking change

## Checklist
- [x] Code follows project conventions
- [x] Tests added and passing
- [x] Documentation updated
- [x] Linked to Archon tasks
```

### Step 5: Update Tasks to "done"

```
For each linked task:

Use Archon MCP to update:
- Status: "review" → "done"
- Add PR link
- Add completion timestamp
- Add final notes
```

### Step 6: Create PR (if gh CLI available)

```bash
gh pr create \
  --title "[Generated title]" \
  --body "[Generated description]" \
  --base main
```

Or provide description to paste manually.

## Output

```
✓ PR Description Generated

Related Archon Tasks:
- TASK-123: Add JWT authentication
- TASK-124: Add user model

✓ Tasks marked as DONE in Archon
  TASK-123: Status updated to done
  TASK-124: Status updated to done
  
View tasks: 
- http://localhost:3737/tasks/TASK-123
- http://localhost:3737/tasks/TASK-124

Creating PR...
✓ PR created: https://github.com/your-org/your-repo/pull/42

Tasks completed and linked to PR!
```

## Auto-Completion

Tasks automatically marked "done" when:
- PR created with `/create-pr`
- Commit references task with "Closes TASK-123"
- All validation complete

## Manual Completion

Or mark done manually:
```bash
/complete-task TASK-123
```

## Without gh CLI

If `gh` not installed:
- Still generates PR description
- Still updates tasks to done
- Shows description to paste manually

## Without Archon

If Archon not available:
- Still generates PR description
- Skips task updates
- Works normally otherwise
