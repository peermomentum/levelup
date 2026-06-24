---
name: messaging-gateway-setup
description: "Configure and troubleshoot Hermes messaging gateway platforms such as Telegram, including PTY setup wizards, allowlists, home channels, foreground runs, and Portal auth checks."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, gateway, messaging, telegram, setup, troubleshooting]
    created_by: agent
---

# Messaging Gateway Setup

Use this skill when the user asks to configure, run, verify, or troubleshoot Hermes gateway messaging platforms such as Telegram, Discord, Slack, or the gateway service itself. If the task is specifically about Hermes Agent, also load `hermes-agent`; if that skill is protected, use this skill for user-environment operational lessons.

## Core workflow

1. Check whether a setup or gateway process is already running before starting another one.
   - If a prior `hermes gateway setup` is waiting for input, continue that process instead of spawning duplicate wizards.
   - Use the tracked process session ID when available.
2. Prefer a PTY for interactive setup wizards:
   - `hermes gateway setup` uses interactive terminal UI prompts.
   - Run with PTY when driving it via tools, and poll after each submitted answer.
3. For Telegram setup:
   - Create/retrieve the bot token from `@BotFather`.
   - Select `Telegram` in the platform list, choose reconfigure only if the user intends to replace existing config, then enter the token.
   - For security, configure an allowlist using the user's numeric Telegram ID, not their `@username`.
   - The home channel for a Telegram DM is also the numeric Telegram user ID. It can be set during setup or later from Telegram with `/set-home` or the current slash command shown by Hermes.
4. If the gateway warns that no allowlists are configured, add a platform allowlist rather than enabling open access by default:
   - Prefer `TELEGRAM_ALLOWED_USERS=<numeric_id>` for Telegram.
   - Only use `GATEWAY_ALLOW_ALL_USERS=true` if the user explicitly wants open access.
5. Start the gateway:
   - Foreground: `hermes gateway run`
   - If service install is unsupported in the environment, do not keep retrying service install; run foreground or a managed background process.
6. Verify actual runtime output:
   - Confirm the process remains running.
   - Poll logs/output for startup errors and authorization warnings.
   - Have the user message the bot to complete end-to-end verification.
7. If the user wants a long-running foreground gateway without a service:
   - Use `tmux` only after checking it is installed.
   - If `tmux` is unavailable, either install it with user approval or keep the gateway as a tracked background process and give the process/session ID.
   - Avoid starting duplicate gateway processes; stop or reuse the existing one before moving it to another supervisor.

## Pitfalls and fixes

- Telegram home channel and allowlist prompts require numeric IDs, not handles. If the user supplies `@name`, tell them to message `@userinfobot` and paste the numeric ID.
- Do not submit the default `Done` selection accidentally when the user asked for a specific platform. In interactive multi-select lists, first move focus to the platform, submit, then handle that platform's prompts.
- If the user pastes a bot token into chat, avoid repeating it. Mention token rotation as a safety recommendation if the transcript may be stored or shared.
- If `hermes` is not on PATH but the binary is known, use the absolute binary for the task and separately help the user add it to their shell profile. Treat PATH issues as environment setup, not as a durable limitation of Hermes.
- If `hermes doctor` or gateway commands fail due file ownership/permissions in the active Hermes home, fix ownership/permissions when safe, then rerun the command to verify. Capture the fix and verification, not the transient error.
- Permission warnings can also come from agent-created skills under the active Hermes home (for example a `SKILL.md` owned by root and mode `600`). Fix the owning skill directory/file permissions, then rerun `hermes doctor` or restart the gateway to reload cleanly.
- After running config/auth flows such as `hermes model` as root, check `$HERMES_HOME/config.yaml` and `$HERMES_HOME/auth.json` ownership before restarting the gateway as `hermes`; root-owned files can make the gateway fall back to stale `.env` values or fail to read config.
- If a platform conflict reports a PID that is defunct/zombie, do not keep killing it (zombies cannot be killed). Inspect the scoped lock under `$HERMES_HOME/.local/state/hermes/gateway-locks/`; if the lock points to the confirmed zombie/gone PID, move the lock aside and restart the gateway. See `references/gateway-zombie-scoped-locks.md` for a safe recovery recipe.
- Gateway setup may finish with `Service install not supported on this platform`. This is not fatal; run the gateway in foreground or under an external supervisor.
- If Telegram reports `bot token already in use (PID NNNN)`, inspect the PID before killing it: `ps -p NNNN -o user,pid,ppid,stat,cmd`. A `Z`/`<defunct>` zombie cannot be killed even with `kill -9`; its parent must reap it. If only a stale gateway/platform lock references that zombie, inspect and remove the stale lock/state file with user approval rather than repeatedly killing the PID.
- Gateway setup may finish with `Service install not supported on this platform`. This is not fatal; run the gateway in foreground or under an external supervisor.
- Telegram long-polling can emit transient `httpx.ReadError` warnings and schedule reconnects. Do not treat the first read error as fatal if the gateway process remains running. Check basic reachability to `https://api.telegram.org`, poll the gateway output for repeated attempts or exit, and ask the user to test `/start` in Telegram. Restart only if reconnect attempts keep repeating or the process exits.
- If Telegram startup says the bot token is already in use by a PID that `ps` shows as `[hermes] <defunct>` / zombie, `kill` and `kill -9` will not clear it. Inspect the scoped lock under `$XDG_STATE_HOME/hermes/gateway-locks` or `/opt/data/.local/state/hermes/gateway-locks`; if the lock record points to the zombie PID, move the `telegram-bot-token-*.lock` file aside with a `.stale-<timestamp>` suffix, then restart the gateway as the `hermes` user. See `references/stale-telegram-token-lock-zombie.md`.
- If gateway startup says `Telegram bot token already in use (PID N)` but `ps` shows that PID is `[hermes] <defunct>` / zombie, `kill` and `kill -9` will not clear it. Inspect the token-scoped lock under `$XDG_STATE_HOME/hermes/gateway-locks/` (often `$HERMES_HOME/.local/state/hermes/gateway-locks/` in containers). If the lock JSON points at the zombie PID and `/proc/<pid>/status` confirms `State: Z`, move the stale lock aside, then restart the gateway as the non-root `hermes` user. See `references/telegram-stale-scoped-lock-zombie.md`.

## Verification commands

```bash
hermes --version
hermes doctor
hermes gateway setup
hermes gateway run
```

For a process-driven run, confirm the gateway process is still running after startup and inspect the latest output for warnings or errors.

## References

- `references/telegram-portal-setup-session.md` — concise transcript-derived notes for Telegram + Nous Portal setup, including numeric-ID prompts and foreground gateway startup.
- `references/telegram-gateway-reconnect-and-permissions.md` — Telegram reconnect warnings, numeric-ID env entries, and permission-fix patterns for gateway skill-loading warnings.
- `references/gateway-root-and-stale-telegram-pid.md` — root-guard-safe foreground gateway runs in containers and Telegram token conflicts caused by stale/zombie PIDs.
