# Connect to GitHub Repository

Connect local repository to GitHub and push all code.

## Usage
/connect-github-repo

## What This Does

1. **Checks current git status**
   - Verifies git is initialized
   - Shows current remote connections

2. **Prompts for GitHub repo URL**
   - Asks for the repository URL
   - Example: https://github.com/your-org/your-repo.git

3. **Connects local to remote**
   - Adds remote origin (or updates if exists)
   - Pulls any existing content from GitHub
   - Merges histories if needed

4. **Pushes all local code**
   - Stages all files
   - Creates commit if needed
   - Pushes to main branch
   - Sets upstream tracking

## Process

### Step 1: Verify Git Initialized
```bash
if [ ! -d .git ]; then
  echo "Initializing git repository..."
  git init
fi

echo "Current status:"
git status
```

### Step 2: Check Existing Remote
```bash
CURRENT_REMOTE=$(git remote -v)

if [ -n "$CURRENT_REMOTE" ]; then
  echo "Current remote:"
  echo "$CURRENT_REMOTE"
  echo ""
  echo "Update remote? (y/n)"
else
  echo "No remote configured."
fi
```

### Step 3: Prompt for Repository URL
```
Enter GitHub repository URL:
Example: https://github.com/your-org/your-repo.git

URL: ___________
```

### Step 4: Connect Remote
```bash
# If remote exists, update it
if git remote | grep -q origin; then
  git remote set-url origin $REPO_URL
  echo "✓ Updated remote origin"
else
  git remote add origin $REPO_URL
  echo "✓ Added remote origin"
fi

# Verify
git remote -v
```

### Step 5: Pull Existing Content (If Any)
```bash
# Fetch to see what's on remote
git fetch origin

# If remote has commits, pull them
if git ls-remote --heads origin main | grep -q main; then
  echo "Remote has content. Pulling..."
  git pull origin main --allow-unrelated-histories --no-rebase
  
  # Resolve any conflicts if needed
  if [ $? -ne 0 ]; then
    echo "⚠ Merge conflicts detected."
    echo "Resolve conflicts, then run:"
    echo "  git add ."
    echo "  git commit -m 'Merge remote content'"
    echo "  git push origin main"
    exit 1
  fi
fi
```

### Step 6: Stage and Commit All Changes
```bash
# Stage all files
git add -A

# Check if there are changes to commit
if git diff --staged --quiet; then
  echo "No changes to commit."
else
  echo "Committing all changes..."
  git commit -m "Add complete project structure to GitHub"
fi
```

### Step 7: Push to GitHub
```bash
echo "Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
  echo ""
  echo "✓ Successfully pushed to GitHub!"
  echo ""
  echo "Your repository is now at:"
  git remote get-url origin
else
  echo ""
  echo "✗ Push failed. Possible issues:"
  echo "  - Authentication required (run: gh auth login)"
  echo "  - Wrong repository URL"
  echo "  - No push permissions"
fi
```

## Example Output

```
Connect to GitHub Repository
============================

Current status:
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  
  modified:   README.md
  
Untracked files:
  .claude/
  maestro/
  tests/

Current remote: None configured

Enter GitHub repository URL:
> https://github.com/your-org/your-repo.git

✓ Added remote origin

Remote has content. Pulling...
✓ Merged remote content

Committing all changes...
[main 7a8f3d2] Add complete project structure to GitHub
 42 files changed, 2847 insertions(+)
 create mode 100644 .claude/agents/codebase-analyst.md
 create mode 100644 maestro/flows/login.yaml
 ...

Pushing to GitHub...
Enumerating objects: 52, done.
Counting objects: 100% (52/52), done.
Writing objects: 100% (52/52), 45.23 KiB | 5.65 MiB/s, done.
Total 52 (delta 8), reused 0 (delta 0)

✓ Successfully pushed to GitHub!

Your repository is now at:
https://github.com/your-org/your-repo.git
```

## Prerequisites

### Authentication Required
Before pushing, ensure you're authenticated:

```bash
# Check authentication
gh auth status

# If not authenticated:
gh auth login
# Select your account (work or personal)
```

### Or use SSH
If using SSH keys:
```
URL format: git@github.com:your-org/your-repo.git
```

## Common Scenarios

### Scenario 1: New Empty GitHub Repo
```bash
# Create repo on GitHub (empty, no README)
# Run command
/connect-github-repo
# Enter: https://github.com/your-org/your-repo.git
# All local code pushed
```

### Scenario 2: GitHub Repo with README
```bash
# GitHub has initial commit with README
# Run command
/connect-github-repo
# Automatically pulls README
# Merges with local code
# Pushes everything
```

### Scenario 3: Updating Existing Remote
```bash
# Already connected to different remote
# Run command
/connect-github-repo
# Choose to update remote URL
# Enter new URL
# Pushes to new remote
```

## After Running

Verify on GitHub:
- Go to your repository URL
- Refresh the page
- All folders should be visible: .claude/, maestro/, tests/, etc.

## Troubleshooting

### "Authentication failed"
```bash
# Authenticate with gh CLI
gh auth login

# Or setup SSH keys
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### "Merge conflicts"
```bash
# Resolve conflicts manually
git status  # See conflicting files
# Edit files to resolve
git add .
git commit -m "Resolve merge conflicts"
git push origin main
```

### "Permission denied"
```bash
# Check you have push access to organization
# Must be member of your-org organization
# Check repository permissions in Settings
```

## Security Notes

- Repository URL is not stored (enter each time)
- Uses git's credential helper for passwords
- gh CLI manages authentication tokens securely
- Private repos require authentication

## When to Use

Use this command:
- After creating a new GitHub repository
- When moving project to different organization
- When initial local development is ready to push
- To fix broken remote connections
