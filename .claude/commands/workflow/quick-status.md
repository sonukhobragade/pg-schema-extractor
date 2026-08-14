# /quick-status

**Description**: Quick overview of current workflow state

**Category**: workflow

**Usage**: `/quick-status`

---

## What This Does

Provides instant visibility into:
- Current Archon tasks (doing/review/todo)
- Git branch and status
- Last commit info
- Available next actions

---

## Prompt

Show a concise status dashboard:

1. **Query Archon**:
   ```
   mcp__archon__find_tasks with project_id and filter status:doing
   mcp__archon__find_tasks with project_id and filter status:review
   mcp__archon__find_tasks with project_id and filter status:todo (limit 3)
   ```

2. **Check Git**:
   ```bash
   git status --short
   git log -1 --oneline
   git branch --show-current
   ```

3. **Format Output**:

```
📊 QUICK STATUS
━━━━━━━━━━━━━━━━

🔄 Active Work:
   ${doing_task ? `✅ ${task_title}` : '❌ No active task'}

🔍 Review Queue:
   ${review_count} task(s) awaiting review

📋 Todo Queue:
   ${todo_count} task(s) pending
   ${show first 3 task titles}

🌿 Git:
   Branch: ${current_branch}
   Status: ${clean ? 'Clean' : 'Uncommitted changes'}
   Last commit: ${last_commit}

⚡ Quick Actions:
   ${suggest_next_action}
```

Keep it concise - max 20 lines total.
