# Git Basics
### Preparations
1. Create GitHub account and add your local system's ssh key. Follow this [guide](https://wastalinux.org/home/customizing/github-setup/) from the wasta devs. (But don't worry about step 4, "Contact the Wasta-Linux team".)
2. Configure git on your system.
```bash
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```
3. Clone git repo to your system. See the first command given below.

### Git Command Examples
```bash
# Clone remote repo "lt" locally via https.
~$ git clone https://github.com/n8marti/lt.git
Cloning into 'lt'...
remote: Enumerating objects: 10, done.
remote: Counting objects: 100% (10/10), done.
remote: Compressing objects: 100% (9/9), done.
remote: Total 10 (delta 1), reused 6 (delta 0), pack-reused 0
Unpacking objects: 100% (10/10), 13.54 KiB | 1.50 MiB/s, done.

# Change directory into local repo root.
~$ cd lt
~/lt$

# Check local repo status.
~/lt$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
~/lt$

# Add a file, e.g.:
#   - create "GIT BASICS.md" and save to ~/lt
#   - open "GIT BASICS.md"
#   - add text
#   - save file

# Check local repo status.
~/lt$ git status
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	GIT BASICS.md

nothing added to commit but untracked files present (use "git add" to track)
~/lt$

# If a new file has been created or modified, add (or "stage") it in preparation for a commit.
~/lt$ git add "GIT BASICS.md"
~/lt$

# Check status again (new file added).
~/lt$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   GIT BASICS.md

~/lt$

# Check status again (existing file modified).
~/lt$ git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   GIT BASICS.md

~/lt$

# Commit changes to make them "official" in the local repo.
~/lt$ git commit -m "added GIT BASICS.md"
[main 2d693bf] added GIT BASICS.md
 1 file changed, 52 insertions(+)
 create mode 100644 GIT BASICS.md
~/lt$

# Periodically "push" the changes in your local repo to the remote repo.
~/lt$ git push
Username for 'https://github.com': n8marti
Password for 'https://n8marti@github.com':
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 512 bytes | 512.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0)
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/n8marti/lt.git
   0a1890f..79e6b3b  main -> main
```
