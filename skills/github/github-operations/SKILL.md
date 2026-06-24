---
name: github-operations
description: "Use when operating GitHub repositories end-to-end: authentication, repository management, issues, pull requests, code review, CI checks, and releases."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, gh-cli, git, pull-requests, issues, code-review, ci]
    related_skills: []
---

# GitHub Operations

## Overview

This umbrella covers the full GitHub work class: auth setup, repo cloning/creation/forking, issue management, PR lifecycle, code review, CI monitoring, and release/repo administration. Prefer this class-level skill over separate GitHub micro-skills unless a task is already inside a loaded archived reference.

## When to Use

- The user asks for GitHub authentication or token/SSH/`gh` setup.
- Creating, cloning, forking, or managing repository settings/remotes/releases.
- Creating, triaging, labeling, assigning, or closing issues.
- Creating, reviewing, commenting on, updating, monitoring, or merging PRs.
- Diagnosing GitHub Actions / CI failures and pushing fixes.

## Operating Standard

1. Start from the repository state: `git status`, `git remote -v`, current branch, and `gh auth status` when relevant.
2. Prefer `gh` CLI when authenticated; fall back to git + REST/GraphQL with `GITHUB_TOKEN` only when needed.
3. Extract `owner/repo` from the remote before API calls.
4. For write operations, make scope explicit: target repo, branch, issue/PR number, labels/reviewers, merge method.
5. Verify side effects by reading back GitHub state (`gh pr view`, `gh issue view`, API response, CI status).
6. Never invent PR numbers, CI statuses, review comments, or merge outcomes.

## Workflow Sections

### Authentication

Check `gh auth status` first. If unauthenticated, choose between browser login, token login, or SSH based on the user's environment. Avoid printing tokens. Prefer storing credentials through `gh auth login` or existing secure helpers.

### Repository Management

Use for clone/create/fork/remotes/releases. Verify the origin URL, default branch, permissions, and whether the local working tree is clean before destructive operations.

When the repo is for backing up Hermes Agent setup, use the sanitized-private-repo workflow in `references/hermes-setup-backup-private-repo.md`: commit templates and skills, exclude secrets/runtime state, and verify the GitHub repo is private after creation.

### Issues

Use GitHub issues for bug reports, feature requests, triage, labels, assignment, and project linkage. Keep issue bodies actionable: summary, reproduction/acceptance criteria, environment, and links.

### Pull Requests

Use branch → commit → push → PR create → CI monitor → review/fix → merge lifecycle. Require a clean diff and test plan before creating or merging. Prefer squash merge unless project conventions say otherwise.

### Code Review

Review diffs for correctness, regressions, security, race conditions, and missing tests. If posting comments, use precise file/line context and avoid noisy style-only comments unless requested.

### CI and Auto-Fix

When CI fails: fetch failed logs, identify root cause, patch, commit, push, and re-check. Repeat only while failures are actionable; stop and report blockers instead of guessing.

## Package Notes

The old GitHub auth, code-review, issues, PR workflow, repo-management, and codebase-inspection skills were absorbed into this umbrella. Their source snapshots, templates, and references are stored under `references/absorbed-*` / `templates/absorbed-*` for exact command details.

## Common Pitfalls

- Running GitHub commands outside the intended repository.
- Confusing commit statuses with GitHub Actions check runs.
- Posting review comments without verifying line positions against the current diff.
- Merging before CI and requested reviews are satisfied.
- Leaking tokens in logs or final answers.

## Verification Checklist

- [ ] Auth and target owner/repo were confirmed.
- [ ] Local git branch/status matched the intended operation.
- [ ] API/CLI write operations returned success and were read back.
- [ ] CI/review/merge claims are backed by real command output.
