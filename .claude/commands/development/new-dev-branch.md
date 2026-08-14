# New Dev Branch

Create properly named development branch following project conventions.

## Usage
/new-dev-branch "description"

## Process

1. **Check current state:** `git status`
2. **Update main:** `git checkout main && git pull`
3. **Determine type:** feature/, bugfix/, hotfix/, chore/
4. **Create branch:** `git checkout -b type/kebab-case-description`

## Examples
- `/new-dev-branch "Add user authentication"` → `feature/add-user-authentication`
- `/new-dev-branch "Fix login bug"` → `bugfix/fix-login-bug`
- `/new-dev-branch "Update dependencies"` → `chore/update-dependencies`

## When to Use
Start of any new work to ensure clean branch naming.
