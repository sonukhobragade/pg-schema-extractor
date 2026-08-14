# Workflow Commands

Commands for managing and enforcing the Archon workflow.

## Available Commands

### `/enforce-workflow`
Validates current workflow state against CLAUDE.md rules. Use before making any code changes.

**When to use**: Before starting work, before commits, when unsure about workflow compliance

### `/quick-status`
Quick dashboard showing current tasks, git state, and suggested next actions.

**When to use**: Start of work session, checking progress, planning next steps

---

## Workflow Integration

These commands work with:
- **CLAUDE.md** - Central rules file
- **Git hooks** - pre-commit, commit-msg, pre-push
- **Archon MCP** - Task management
- **Agents** - Specialized workers

## Examples

```bash
# Start of day
/quick-status

# Before making changes
/enforce-workflow

# Check progress
/quick-status

# Before commit
/enforce-workflow
```
