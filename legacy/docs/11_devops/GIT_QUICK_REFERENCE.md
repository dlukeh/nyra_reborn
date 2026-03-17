# Git Quick Reference

## .gitignore Example
```gitignore
# Python
venv/
__pycache__/
*.pyc
*.pyo

# Environment
.env

# OS/Editor
.DS_Store
.vscode/

# Logs
*.log

# Misc
*.swp
*.bak
```

## Essential Git Commands

**Initialize a repo**
```sh
git init
```

**Check status**
```sh
git status
```

**Add files**
```sh
git add .
```

**Commit changes**
```sh
git commit -m "Your message"
```

**View history**
```sh
git log
```

**Create a branch**
```sh
git branch feature-xyz
git checkout feature-xyz
```

**Merge branches**
```sh
git checkout master
git merge feature-xyz
```

**Connect to remote (GitHub)**
```sh
git remote add origin https://github.com/your/repo.git
git push -u origin master
```

**Pull latest changes**
```sh
git pull
```

## Key Concepts
- **Commit:** Saved snapshot of your project
- **Branch:** Independent line of development
- **Merge:** Combine changes from one branch into another
- **Remote:** Repo copy on a server (e.g., GitHub)
- **Staging:** Preparing changes for commit

---
For more, see the official [Git documentation](https://git-scm.com/doc).
