---
name: autonomous-coding-agents
description: "Use when delegating implementation, review, or refactoring work to external autonomous coding CLIs such as Claude Code, Codex, OpenCode, or Kanban lanes."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [autonomous-agents, coding-agents, claude-code, codex, opencode, kanban, delegation]
    related_skills: [subagent-driven-development]
---

# Autonomous Coding Agents

## Overview

This umbrella covers the class of workflows where Hermes delegates coding work to an external autonomous coding agent CLI, monitors it, and verifies the result before reporting success. It replaces tool-specific micro-skills for Claude Code, OpenAI Codex CLI, OpenCode, and Kanban/Codex lane handoffs.

## When to Use

- A coding task can be delegated to an installed agent CLI with project filesystem access.
- You need parallel implementation or review lanes while Hermes remains the accountable orchestrator.
- The user explicitly asks to use Claude Code, Codex, OpenCode, or a Kanban worker lane.
- You need a PR review/fix/refactor from an external coding agent, followed by independent verification.

Do not use for simple edits that Hermes can safely make and test directly faster than launching another agent.

## Orchestration Principles

1. **Hermes owns the outcome.** External agents are workers, not proof. Always inspect diffs and run tests yourself.
2. **Set scope tightly.** Give exact files, acceptance criteria, commands to run, and forbidden actions.
3. **Prefer non-interactive/print mode for bounded work.** Use interactive tmux/PTY only when multi-turn steering is needed.
4. **Isolate when possible.** Use git branches/worktrees or Kanban lanes for concurrent work.
5. **Capture verifiable handles.** Require final diffs, command outputs, branch names, or PR URLs—not vague self-reports.
6. **Clean up sessions.** Kill tmux/background processes and note remaining work explicitly.

## Agent-Specific Playbooks

### Claude Code

Best for broad coding/refactoring and deep PR review. Prefer `claude -p` for one-shot tasks with `--max-turns`, `--allowedTools`, and a project `workdir`. Use tmux only for interactive sessions requiring follow-up prompts, slash commands, or live monitoring. Watch for first-run trust and permission dialogs in interactive mode.

### Codex CLI

Best for OpenAI-backed code changes, alternative implementation lanes, and isolated reviews. Run from the repository root, pass a self-contained prompt, and require a final summary plus tests run. Treat the Codex result as a patch proposal until Hermes verifies it.

### OpenCode

Best for coding or review tasks where OpenCode is the configured local agent. Use the same bounded prompt pattern: repo context, precise objective, constraints, test command, and final evidence requirements.

### Kanban Codex Lanes

Use when a Hermes Kanban worker wants Codex as an isolated implementation lane while the Kanban orchestrator keeps lifecycle ownership. The lane prompt should include the card goal, branch/worktree strategy, acceptance criteria, status reporting format, and exact handoff evidence.

## Standard Prompt Template

```markdown
You are an autonomous coding worker inside this repository.
Goal: <specific change>
Scope: <allowed files/areas>
Constraints: <do not touch / style / safety>
Verification: run <commands> and report exact output.
Handoff: summarize changed files, tests run, failures, and any follow-up needed.
Do not claim completion unless the verification command actually ran.
```

## Monitoring Patterns

- For bounded CLI runs, use foreground `terminal(..., timeout=...)` or background with `notify_on_complete=true` for long tasks.
- For TUIs, launch under tmux, send prompts with `tmux send-keys`, and inspect with `tmux capture-pane`.
- Detect waiting vs working states from prompt/status indicators; do not kill a slow session without checking logs.

## Package Notes

The previous Claude Code, Codex, OpenCode, and Kanban-Codex-lane skills were absorbed here. Source package snapshots and lane templates live under `references/absorbed-*` / `templates/absorbed-*` when needed for exact CLI flags.

## Common Pitfalls

- Treating an agent's final message as verification.
- Launching interactive TUIs without tmux capture/cleanup.
- Giving agents broad write access when a read-only review would suffice.
- Forgetting `workdir`, causing the agent to operate in the wrong repository.
- Letting multiple lanes write to the same branch without coordination.

## Verification Checklist

- [ ] External agent was given a bounded, self-contained task.
- [ ] Work ran in the intended repository/worktree.
- [ ] Hermes inspected changes after the agent finished.
- [ ] Tests/build/lint were run by Hermes or independently verified from real output.
- [ ] Background/tmux sessions were cleaned up or intentionally left running with IDs.
