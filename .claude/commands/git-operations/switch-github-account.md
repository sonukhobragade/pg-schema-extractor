# Switch GitHub Account

Switch between multiple GitHub accounts for this project.

## Usage
/switch-github-account

## What This Does

1. **Shows current account configuration**
   - Display current git user.name
   - Display current git user.email
   - Display current gh CLI authentication

2. **Lists available accounts**
   - Show configured accounts (if stored)
   - Or prompt for account selection

3. **Switches git config for this repo**
   - Sets user.name for this repository only
   - Sets user.email for this repository only
   - Does NOT affect global git config

4. **Switches gh CLI authentication**
   - Prompts to switch gh auth if needed
   - Verifies authentication status

## Process

### Step 1: Show Current Configuration
```bash
echo "Current Git Config:"
git config user.name
git config user.email

echo "\nGitHub CLI Status:"
gh auth status
```

### Step 2: Prompt for Account Selection
```
Available accounts:
1. Personal (your-personal@email.com)
2. Work/Organization (your-work@email.com)

Which account to use? [1/2]:
```

### Step 3: Apply Configuration
```bash
# Set for THIS repo only (not global)
git config user.name "Account Name"
git config user.email "account@email.com"

# Verify
echo "✓ Git configured for this repo:"
git config user.name
git config user.email
```

### Step 4: Check gh CLI
```bash
# Prompt if gh auth needs switching
gh auth status

# If wrong account:
echo "Run: gh auth login"
echo "Then select the account you want to use"
```

## Configuration File

Store your accounts in `.claude/github-accounts.json`:

```json
{
  "accounts": [
    {
      "name": "Personal",
      "user": "Your Name",
      "email": "personal@example.com"
    },
    {
      "name": "Work",
      "user": "Your Name", 
      "email": "you@company.com"
    }
  ]
}
```

## Example Output

```
Current Configuration:
---------------------
Git User: Your Name
Git Email: personal@example.com
GitHub CLI: Authenticated as personal-account

Available Accounts:
---------------------
1. Personal (personal@example.com)
2. Work (you@company.com)

Select account [1/2]: 2

✓ Switched to: Work
  User: Your Name
  Email: you@company.com

GitHub CLI Status:
✓ Authenticated as work-account

Ready for commits!
```

## After Switching

You can now use:
```bash
/smart-commit      # Uses the selected account
/create-pr         # Uses the selected account
```

## Manual Override

If you need to switch gh CLI manually:
```bash
gh auth login
# Select the account you want
# Follow browser authentication
```

## Notes

- Account switch is **per-repository** (not global)
- Switch before committing to ensure correct author
- gh CLI needs separate authentication per account
- If no accounts configured, prompts for manual entry

## When to Use

Use this command:
- Before starting work on a project
- When switching between personal/work projects  
- Before making commits to ensure correct attribution
- Before creating PRs to use correct GitHub account

## Security

- Passwords/tokens are never stored
- Uses git's standard config mechanism
- gh CLI handles authentication securely
- Account info stored in project only (not global)
