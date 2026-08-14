# Code Quality Commands

Commands for maintaining code quality and enforcing standards.

## Available Commands

### `/lint [--fix]`
Run all linters (ruff + mypy). Use `--fix` to auto-fix issues.

**When to use**: Before committing code, during development

### `/format`
Auto-format all Python code with ruff formatter.

**When to use**: Before committing, after writing new code

### `/test-coverage [--html]`
Run tests with coverage report. Use `--html` to open interactive report.

**When to use**: After adding new code, checking test quality

### `/validate`
Complete validation gate check before merge. Runs ALL quality checks.

**When to use**: Before creating PR, before marking task "done"

---

## Workflow Integration

```bash
# During development
/lint              # Quick check
/format            # Auto-fix formatting

# Before commit
/lint --fix        # Fix linting issues
/test-coverage     # Check coverage

# Before merge
/validate          # Full quality gate
/create-pr         # Create PR (runs validation first)
```

---

## Quality Standards

All commands enforce:
- **KISS** - Keep code simple
- **YAGNI** - No speculative features
- **DRY** - No duplication
- **Type Hints** - All functions typed
- **Test Coverage** - Minimum 80%
- **Maestro Patterns** - Centralized locators, reusable helpers

---

## Examples

```bash
# Quick lint check
/lint

# Fix and format
/lint --fix
/format

# Check coverage
/test-coverage

# Full validation before PR
/validate
```
