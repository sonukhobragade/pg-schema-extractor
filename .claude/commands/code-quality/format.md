# /format

**Description**: Auto-format all Python code with ruff

**Category**: code-quality

**Usage**: `/format`

---

## What This Does

Automatically formats all Python code:
- Consistent indentation
- Import sorting
- Line length enforcement
- PEP 8 compliance

---

## Prompt

Format all Python code using ruff formatter.

**Steps:**

1. **Check what will change**:
   ```bash
   ruff format framework/ tests/ --check --diff
   ```

2. **Show preview**:
   Show user what files will be formatted

3. **Ask confirmation**:
   "Format [X] files? (y/n)"

4. **If yes, format**:
   ```bash
   ruff format framework/ tests/
   ```

5. **Show results**:
   ```
   ✅ FORMATTED FILES
   ━━━━━━━━━━━━━━━━━

   📝 Modified:
   - framework/config.py
   - framework/maestro_runner.py
   - tests/test_suite.py

   Total: 3 files formatted

   Next: git add . && git commit -m "style: format code with ruff"
   ```

**Remember**: Always show preview before formatting.
