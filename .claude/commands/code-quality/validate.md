# /validate

**Description**: Run complete validation gate before merge

**Category**: code-quality

**Usage**: `/validate`

---

## What This Does

Comprehensive quality gate check:
1. Workflow compliance (Archon task)
2. Code quality (lint + types)
3. Test coverage
4. Maestro flow validation
5. KISS/YAGNI/DRY check

---

## Prompt

You are the validation gate agent. Run COMPLETE validation check.

**CRITICAL**: This is a quality gate. Be thorough and strict.

**Steps:**

1. **Invoke validation-gate agent**:
   ```
   Use Task tool to invoke validation-gate agent with:
   - subagent_type: "general-purpose"
   - description: "Run validation gate"
   - prompt: "Execute complete validation gate as defined in .claude/agents/validation-gate.md"
   ```

2. **Agent will**:
   - Check Archon task state
   - Run all automated checks (lint, types, tests)
   - Validate KISS/YAGNI/DRY
   - Check Maestro flows
   - Verify test coverage
   - Generate detailed report

3. **Display results**:
   Show validation gate report from agent

4. **Update task**:
   - If PASS: Suggest `/create-pr`
   - If FAIL: Mark task back to "doing", list fixes needed

**Remember**:
- Block merge if validation fails
- Be specific about issues
- Suggest fixes
- Update Archon task status
