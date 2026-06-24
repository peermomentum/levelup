---
name: interactive-cli-wizards
description: Safely operate interactive terminal setup wizards and menu-driven CLIs through PTY/background process tools without submitting the wrong default choice.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cli, terminal, pty, interactive, setup, wizard, gateway]
    created_by: agent
---

# Interactive CLI Wizards

Use this skill when asked to run an interactive setup/configuration wizard, menu-driven CLI, curses prompt, or TUI-like flow from tools. Examples: `hermes gateway setup`, provider/model setup, OAuth/device-code prompts, `npm init`, cloud CLIs, or any command where the next action depends on a prompt shown in a PTY.

## Core rule

Do not press Enter on a default selection unless the user explicitly chose that default or the prompt text proves it is safe. Many wizards default to `Done`, `Cancel`, or `Skip`, and blindly submitting can exit while preserving old config.

## Workflow

1. Start the wizard in a PTY/background process when it needs interactive input.
2. Immediately poll/capture enough output to identify:
   - current prompt/menu title,
   - highlighted/default selection,
   - whether the process is still running,
   - what input mode is expected: arrows, typed text, token, yes/no, or device URL.
3. If the user has already named the desired option, navigate to that option before submitting. Prefer deterministic navigation if possible:
   - send the exact text only if the UI supports search/filter input,
   - otherwise use arrow keys only after verifying current cursor position,
   - avoid assuming option ordering unless the captured menu confirms it.
4. If the user responds while the process is running, poll the process first, then act on the current prompt. Do not reuse stale menu state.
5. After each input, poll again and verify the prompt advanced as intended.
6. When the wizard exits, report the actual exit output and any follow-up command it printed.

## Pitfalls

- A user message like `Telegram` during a gateway setup means select the Telegram menu item, not submit the currently highlighted default.
- `Done`, `Cancel`, and `Skip` are common defaults; treat them as dangerous-to-submit until verified.
- Watch patterns are hints, not state. Always poll/capture before sending keys.
- Background-process watch notifications are not fresh user intent and may be delayed or duplicated. Before answering or sending more input after a notification, reconcile the live prompt/state; avoid repeatedly asking the same question from stale notification text.
- If the process already exited before the user's choice arrives, say exactly what happened and provide the command to rerun; do not claim the choice was applied.
- Do not persist environment-specific path failures as rules. If the binary is not on PATH in one environment, resolve it for the current run, but do not encode that path as a universal fact.
- Secret/token prompts need two separate behaviors: never echo the secret back to the user or logs, but when submitting to the PTY, submit the exact user-provided value. Do not replace part of the actual input with `***`; masking is only for display. If secret redaction prevents access to the exact value, ask the user to paste it directly into their terminal or rerun the wizard locally rather than submitting a masked placeholder.
- Validate field type before submitting user replies. Some gateway prompts require numeric IDs, not usernames/handles (e.g. Telegram home channel / allowed user IDs expect numeric Telegram IDs). If the user provides `@handle` where a numeric ID is required, explain how to retrieve the ID instead of submitting the handle.
- Treat security-sensitive defaults as unsafe until the user explicitly chooses them. In gateway setup, prompts like `Allowed user IDs (leave empty for open access)` should not be auto-submitted blank just to keep the wizard moving; ask for the numeric ID(s) or confirm that open access is acceptable.
- If the user sends ordinary shell commands (`pwd`, `ls`, `which hermes`, etc.) while a wizard is still waiting for input, handle the shell command separately and keep track of the wizard's pending prompt. Do not interpret shell-like messages as wizard answers, and remind the user what the wizard still needs.

## Verification checklist

Before finalizing:

- Did the wizard remain running long enough to receive the intended input?
- Did the captured output show the desired option was selected or configured?
- If configuration was skipped/kept, did you say so clearly?
- Did you avoid turning transient PATH/setup quirks into durable constraints?

## References

- `references/hermes-gateway-setup-menu.md` — session note on avoiding accidental `Done` submission in Hermes gateway setup menus.
