---
name: software-development-workflow
description: "Use when running a software change from plan to verification: plan-only mode, implementation plans, spikes, TDD, root-cause debugging, language debugger sessions, and pre-commit review."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [software-development, planning, debugging, testing, tdd, code-review, workflow]
    related_skills: [subagent-driven-development, github-operations, hermes-agent-skill-authoring]
---

# Software development workflow

## Overview

This is the umbrella skill for day-to-day software engineering work. It collects the class-level workflow that used to be split across narrow process skills: planning, exploratory spikes, test-first implementation, root-cause debugging, debugger use, and pre-commit review.

Use it as the routing layer first, then apply the relevant subsection. If a task is large enough to delegate, combine this skill with `subagent-driven-development`.

Detailed source playbooks from the absorbed narrow skills are retained under `references/absorbed-*.md` for maintainers who need the full original recipes.

## When to use

Load this skill when the user asks to:

- plan a software change without implementing it
- write a concrete implementation plan
- spike or prototype a technical idea before committing
- implement a feature or bug fix
- debug a technical failure
- use Python or Node breakpoints / inspector tooling
- verify code before commit, push, or merge

Do not use this for GitHub issue/PR operations themselves; use `github-operations` for remote GitHub workflows.

## Routing map

| Situation | Section to apply |
|---|---|
| User asks for `/plan`, "make a plan", or "don't implement" | Plan-only mode |
| Multi-step feature needs design before coding | Implementation plans |
| Feasibility is unknown | Spike / proof-of-concept |
| Writing production code | Test-driven implementation |
| Something is failing | Systematic debugging |
| Tracebacks/logging are not enough | Interactive debuggers |
| Work is ready to commit/push | Pre-commit verification |

## Plan-only mode

When the user explicitly wants a plan instead of execution:

- Do not implement code.
- Do not mutate project files except the plan markdown file.
- Read repository context with read-only tools as needed.
- Save the plan under `.hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md` unless the user gave another path.
- Include goal, context, assumptions, proposed approach, steps, files likely to change, validation, risks, and open questions.
- Reply briefly with the saved path.

## Implementation plans

A good implementation plan should let another agent execute without guessing.

Required ingredients:

- exact file paths and line ranges when known
- bite-sized tasks, roughly 2-5 minutes each
- test-first steps for code behavior
- commands to run and expected results
- verification and rollback notes
- commits after meaningful tasks when the repo workflow expects commits

For handoff plans, start with:

```markdown
# <Feature> implementation plan

> For Hermes: use subagent-driven-development to execute this plan task-by-task when delegation is appropriate.

**Goal:** ...
**Architecture:** ...
**Tech stack:** ...
```

## Spike / proof-of-concept

Use a spike when the important question is feasibility, not polish.

Method:

1. Decompose the idea into 2-5 observable feasibility questions.
2. Order by risk; test the idea-killer first.
3. Research just enough to choose credible approaches.
4. Build standalone throwaway artifacts under `spikes/NNN-topic/`.
5. Run the spike and capture evidence.
6. End each spike README with `VALIDATED`, `PARTIAL`, or `INVALIDATED`, plus recommendation for the real build.

Keep spikes disposable. If the prototype becomes production code, rewrite it cleanly using TDD.

## Test-driven implementation

For production behavior changes, use RED-GREEN-REFACTOR:

1. Write one failing test for the desired behavior.
2. Run it and verify it fails for the expected reason.
3. Write the smallest implementation that passes.
4. Run the focused test and then the relevant suite.
5. Refactor only while tests stay green.

Iron law: if you did not watch the test fail, you do not know whether the test proves the behavior.

Exceptions need explicit user approval or must be clearly throwaway work.

## Systematic debugging

Do not guess. Find the root cause before fixing.

Four phases:

1. **Root cause investigation:** read the full error, reproduce reliably, inspect recent changes, trace data flow, and gather evidence at component boundaries.
2. **Pattern analysis:** find working examples, compare broken vs working paths, and list differences.
3. **Hypothesis testing:** state one hypothesis and test it with the smallest possible change or probe.
4. **Implementation:** write a regression test, fix the source cause, run focused and broad verification.

Rule of three: after three failed fixes, stop and question the architecture instead of layering another patch.

## Interactive debuggers

Use breakpoint-driven debugging when logs or tracebacks do not reveal state.

### Python

Start simple:

```bash
python -m pdb path/to/script.py arg1
python -m pytest tests/path/test_file.py::test_name --pdb -p no:xdist
```

For headless or long-running processes, prefer `remote-pdb` for terminal agents or `debugpy` when IDE/DAP integration is needed. Always remove `breakpoint()`, `set_trace()`, and `debugpy.listen()` before committing.

### Node.js

Use built-in inspector first:

```bash
node inspect path/to/script.js
node --inspect-brk script.js
node inspect -p <pid>
```

Inside `debug>` use `sb('file.js', 42)`, `cont`, `next`, `step`, `bt`, and `repl`. Bind inspector to `127.0.0.1`; exposing `--inspect=0.0.0.0` is remote code execution.

## Pre-commit verification

Before committing or pushing code changes:

1. Inspect the diff with `git diff` / `git diff --cached`.
2. Scan added lines for secrets, shell injection, eval/exec, unsafe deserialization, and SQL injection.
3. Run the project’s focused tests, then broader tests/lint/type checks if available.
4. Use an independent reviewer subagent for non-trivial diffs when available.
5. Fix only reported issues; avoid opportunistic refactors.
6. Re-run verification before declaring the work done.

No agent should be the sole reviewer of its own non-trivial code.

## Common pitfalls

- Treating a plan as permission to implement when the user asked for plan-only mode.
- Writing tests after code and calling it TDD.
- Fixing symptoms before tracing the source cause.
- Keeping spike code because it "already works" instead of rebuilding it intentionally.
- Running `pdb` under pytest-xdist and wondering why the prompt hangs.
- Attaching Node inspector too late; use `--inspect-brk` when you need early breakpoints.
- Claiming verification without real command output.

## Verification checklist

- [ ] Correct route chosen from the routing map.
- [ ] If planning, plan saved under the requested path.
- [ ] If implementing, tests were run and results observed.
- [ ] If debugging, root cause evidence is documented.
- [ ] If using breakpoints, no debugger hooks remain in the final diff.
- [ ] If committing/pushing, diff and quality gates were reviewed.
