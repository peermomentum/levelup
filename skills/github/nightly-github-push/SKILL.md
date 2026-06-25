---
name: nightly-github-push
description: Use when setting up or operating a scheduled job that commits and pushes local changes from a Git repository to GitHub every night, including repo/auth checks, safe commit behavior, and verification.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [github, git, cron, automation, backup]
    related_skills: [github-operations]
---

# Nightly GitHub Push

## Overview

Use this skill to create or troubleshoot a recurring Hermes cron job that snapshots a local Git working tree and pushes it to its configured GitHub remote once per night. The workflow is intentionally conservative: it verifies the target is a Git repository, confirms a remote exists, stages ordinary file changes, avoids destructive commands, commits only when there are changes, pushes the current branch, and reports real command output.

This is best for personal configuration repos, notes, generated artifacts, or other low-risk repositories where an automated nightly commit is desired. It is not a replacement for a reviewed pull-request workflow on production code.

## When to Use

- The user asks to push changes to a GitHub repository on a nightly schedule.
- The user wants a recurring backup/snapshot of a local repository.
- A Hermes cron job needs a self-contained prompt for `git add`, `git commit`, and `git push`.
- Troubleshooting a scheduled push job that reports missing remotes, auth failures, or non-fast-forward errors.

Do not use this workflow for repositories where every commit must be human-reviewed, where generated secrets may appear in the working tree, or where force-push/rebase would be required. Stop and ask the user before adding broad ignore rules, rewriting history, or pushing to a different remote/branch than the repository is already configured to use.

## Prerequisite Checks

Run these checks before creating the cron job and again inside the job prompt:

```bash
pwd
git rev-parse --show-toplevel
git status --short --branch
git remote -v
git branch --show-current
```

Optional but useful when GitHub CLI is installed:

```bash
gh auth status
```

If `gh` is not installed, plain `git push` can still work as long as the repository's credential helper, HTTPS token, or SSH key is already configured.

## Recommended Hermes Cron Schedule

Use standard cron syntax for midnight Central Time. Hermes cron interprets cron expressions in the scheduler host timezone unless configured otherwise, so if the host is UTC, midnight Central must be converted:

- Central Daylight Time (UTC-5): `0 5 * * *`
- Central Standard Time (UTC-6): `0 6 * * *`

If the scheduler supports an explicit timezone in the deployment, prefer `0 0 * * *` with `America/Chicago`. If timezone support is not explicit, use the current Central offset and revisit after daylight-saving changes.

## Cron Prompt Template

Use a self-contained prompt like this when creating the Hermes cron job. Replace `/absolute/path/to/repo` with the actual repository path.

```text
You are running the nightly GitHub push job for /absolute/path/to/repo.

Work only in /absolute/path/to/repo. Do not modify files except through normal git staging/commit operations. Run these commands and base your final report only on real output:

1. Verify the repository:
   - pwd
   - git rev-parse --show-toplevel
   - git status --short --branch
   - git remote -v
   - git branch --show-current
2. If this is not a Git repository, or no remote is configured, stop and report the blocker.
3. Stage changes with `git add -A`.
4. Check `git status --short`.
5. If there are no staged or unstaged changes after staging, report `No changes to push` and do not create a commit.
6. If there are changes, create a commit with message `chore: nightly automated snapshot YYYY-MM-DD` using the current date from the system.
7. Push the current branch to its upstream with `git push`. If no upstream exists, push to `origin <current-branch>` and set upstream only if the remote named `origin` exists.
8. Verify with `git status --short --branch` and report the commit hash if a commit was created.

Never force-push. Never create a new branch unless explicitly instructed. Never fabricate success if authentication, network, or non-fast-forward errors occur.
```

## Safe Shell Implementation

For script-only jobs, use this pattern from inside the target repo:

```bash
set -euo pipefail
repo="/absolute/path/to/repo"
cd "$repo"

git rev-parse --show-toplevel >/dev/null
branch="$(git branch --show-current)"
if [ -z "$branch" ]; then
  echo "Blocked: detached HEAD; refusing automated push."
  exit 1
fi
if ! git remote | grep -qx origin; then
  echo "Blocked: no origin remote configured."
  exit 1
fi

git add -A
if git diff --cached --quiet && git diff --quiet; then
  echo "No changes to push for $repo on $branch."
  exit 0
fi

git commit -m "chore: nightly automated snapshot $(date +%F)"
if git rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1; then
  git push
else
  git push -u origin "$branch"
fi

echo "Pushed $(git rev-parse --short HEAD) on $branch."
git status --short --branch
```

## Common Pitfalls

1. **Wrong directory.** Always use an absolute repo path. A cron run starts in a fresh session and may not inherit the interactive working directory.
2. **Host timezone mismatch.** Check `date` and convert Central Time if cron has no timezone field. If the user simply says "midnight," use the scheduler host timezone and state it explicitly in the final response.
3. **No Git repository.** If `git rev-parse --show-toplevel` fails, do not guess a repo path; ask the user.
4. **Missing credentials.** `gh` may be unavailable, but `git push` can still work. If push fails due to auth, report the exact error and ask the user to configure SSH or HTTPS credentials.
5. **Cron script path constraints.** Hermes `cronjob(no_agent=True, script=...)` expects the script path relative to `~/.hermes/scripts/` (usually `$HERMES_HOME/scripts`, e.g. `/opt/data/scripts` in the default profile), not an absolute path. Put reusable backup scripts there and pass only the filename.
6. **Cron shell environment.** Script-only jobs may not inherit the same `HOME` or git config as the interactive session. For GitHub push jobs that rely on `~/.gitconfig` or credential helpers, set `HOME` explicitly inside the script when needed, then verify with a dry/manual script run before scheduling.
7. **Silent no-change runs.** In `no_agent=True` jobs, empty stdout means no delivery. This is desirable for watchdog-style backups: keep the script quiet when there are no changes and print a concise message only when a commit was pushed or an error occurs.
8. **Non-fast-forward push.** Do not force-push. Stop and report that the branch needs manual pull/rebase/merge.
9. **Secrets.** Automated `git add -A` can stage accidental secrets. Ensure `.gitignore` is appropriate before enabling this on sensitive directories. For Hermes setup backups, prefer a sanitized scaffold instead of committing live runtime files.
10. **Detached HEAD.** Refuse to commit when no current branch exists.

9. **Cron HOME / git credentials.** Script-only cron runs may not inherit the interactive shell's `HOME`; if git credentials/config live under a specific home, export `HOME` inside the backup script before `git push`.
10. **Detached HEAD.** Refuse to commit when no current branch exists.

## Verification Checklist

- [ ] Target repository path is absolute and `git rev-parse --show-toplevel` succeeds.
- [ ] `git remote -v` shows the intended GitHub remote.
- [ ] The current branch is the intended branch and is not detached.
- [ ] Authentication is available for `git push` or the first run reports auth errors clearly.
- [ ] Cron schedule corresponds to midnight Central Time for the current daylight-saving offset.
- [ ] Job prompt is self-contained and does not rely on current chat context.
- [ ] The job reports either `No changes to push` or the real commit hash pushed.
