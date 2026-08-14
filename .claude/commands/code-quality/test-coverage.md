# /test-coverage

**Description**: Run tests with coverage report

**Category**: code-quality

**Usage**: `/test-coverage [--html]`

---

## What This Does

Runs pytest with coverage analysis:
- Shows coverage percentage
- Identifies untested code
- Optional HTML report

---

## Prompt

Run pytest with coverage analysis and show detailed report.

**Steps:**

1. **Run tests with coverage**:
   ```bash
   pytest tests/ \
     --cov=framework \
     --cov-report=term-missing \
     --cov-report=html \
     -v
   ```

2. **Parse coverage results**:
   Extract coverage percentage and missing lines

3. **Format output**:
   ```
   📊 TEST COVERAGE REPORT
   ━━━━━━━━━━━━━━━━━━━━━

   Overall Coverage: 87%
   Threshold: 80%
   Status: ✅ PASS

   📁 MODULE BREAKDOWN
   ━━━━━━━━━━━━━━━━━━
   framework/config.py          95%  ✅
   framework/maestro_runner.py  82%  ✅
   framework/suite_runner.py    74%  ⚠️

   🔴 MISSING COVERAGE
   ━━━━━━━━━━━━━━━━━━
   framework/suite_runner.py:
     - Lines 45-52 (error handling)
     - Lines 78-80 (edge case)

   💡 SUGGESTIONS
   ━━━━━━━━━━━━
   - Add test for error handling in suite_runner.py
   - Cover edge case in parse_yaml()

   📂 HTML Report: htmlcov/index.html
      Run: open htmlcov/index.html
   ```

4. **If --html flag, open report**:
   ```bash
   open htmlcov/index.html
   ```

**Thresholds:**
- ✅ >= 80% - Good
- ⚠️ 60-80% - Needs improvement
- ❌ < 60% - Insufficient

**Remember**: Highlight specific untested areas with line numbers.
