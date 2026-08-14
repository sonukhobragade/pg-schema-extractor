# /lint

**Description**: Run all linters and formatters to validate code quality

**Category**: code-quality

**Usage**: `/lint [--fix]`

---

## What This Does

Runs comprehensive code quality checks:
1. **ruff check** - Linting (replaces flake8, isort, black)
2. **mypy** - Type checking
3. **pytest** - Quick smoke test
4. Optional: **--fix** flag auto-fixes issues

---

## Prompt

You are the code quality enforcement agent. Run all linters and report results.

**Steps:**

1. **Check Current Directory**:
   ```bash
   pwd
   ls -la framework/ tests/
   ```

2. **Run ruff (linting)**:
   ```bash
   ruff check framework/ tests/ --output-format=concise
   ```

3. **Run mypy (type checking)**:
   ```bash
   mypy framework/ tests/ --pretty --show-error-codes
   ```

4. **Quick test check**:
   ```bash
   pytest tests/ -v --tb=short -x
   ```

5. **If --fix flag provided**:
   ```bash
   ruff check framework/ tests/ --fix
   ruff format framework/ tests/
   ```

**Output Format:**

```
🔍 CODE QUALITY CHECK
━━━━━━━━━━━━━━━━━━━━

📝 RUFF (Linting)
   Status: [✅ PASS | ❌ FAIL]
   Issues: [count]
   [List specific issues if any]

🎯 MYPY (Type Checking)
   Status: [✅ PASS | ❌ FAIL]
   Errors: [count]
   [List type errors if any]

🧪 PYTEST (Quick Smoke)
   Status: [✅ PASS | ❌ FAIL]
   Tests: [passed/total]

━━━━━━━━━━━━━━━━━━━━

[✅ ALL CHECKS PASSED | ❌ ISSUES FOUND]

[If issues found, show how to fix]
```

**Remember**: Be specific about what's wrong and how to fix it.
