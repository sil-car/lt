# Git Basics
### Preparations
1. Create GitHub account.
2. Configure git on your system.
3. Clone git repo to your system.

### Git Command Examples
```bash
# Clone "lt" repo via https.
~$ git clone https://github.com/n8marti/lt.git
Cloning into 'lt'...
remote: Enumerating objects: 10, done.
remote: Counting objects: 100% (10/10), done.
remote: Compressing objects: 100% (9/9), done.
remote: Total 10 (delta 1), reused 6 (delta 0), pack-reused 0
Unpacking objects: 100% (10/10), 13.54 KiB | 1.50 MiB/s, done.

# Change directory into repo root.
~$ cd lt
~/lt$

# Check repo status.
~/lt$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
~/lt$

# Make changes to files, e.g.:
#   - create "GIT BASICS.md" and save to ~/lt
#   - open "GIT BASICS.md"
#   - add text
#   - save file

# Check repo status.
~/lt$ git status
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	GIT BASICS.md

nothing added to commit but untracked files present (use "git add" to track)

# If a new file has been created, add it to git tracking.
~/lt$ git add "GIT BASICS.md"

# Commit changes to make them "official" in the repo.
~/lt$ git commit -am "added GIT BASICS.md"
```
