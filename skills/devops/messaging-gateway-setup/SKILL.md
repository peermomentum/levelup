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

0. When guiding a non-expert through Hostinger/Docker gateway setup, be explicit but not overwhelming:
   - Start with a short **plain-English status**: what is working, what is broken, and the single next step. Avoid long architecture summaries unless the user asks.
   - Refer to the browser dashboard as **Hostinger hPanel**.
   - Refer to command-entry surfaces as **VPS Terminal**, **Browser Terminal**, **Web Terminal**, or the Docker/container **Terminal** button.
   - Refer to the Docker app launcher as **Docker Manager / Docker Profiles**; **Open** usually opens the app/web UI, while **Terminal** is where setup commands are typed.
   - Give copy/paste commands in small batches and explain what success looks like before moving on.
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
   - If `tmux` is unavailable, use a simple `nohup ... &` background run with profile-specific log redirection before suggesting package installation, unless the user explicitly wants a more robust supervisor.
   - Before moving a foreground gateway to the background, stop it cleanly with Ctrl+C, then restart one background copy; avoid duplicate gateway processes.
   - Verify the background run with both `ps` and a log tail, then ask the user to send a real message to the bot for end-to-end confirmation.
   - Avoid starting duplicate gateway processes; stop or reuse the existing one before moving it to another supervisor.
8. For member-facing concierge bots, prefer one dedicated Telegram bot + one dedicated Hermes profile for the community workflow, not a separate Hostinger bot/server per member. Keep the owner's private/admin Hermes bot separate, first test with the owner's numeric Telegram ID allowlisted, then deliberately broaden access to member IDs, open/public access, channel-membership gating, or an approval/intake workflow. Put `/start` welcome/intake behavior in the concierge profile's active `SOUL.md` and/or an installed class-level concierge skill under that profile. If using channel-membership gating, do **not** simply remove/relax the gateway hard allowlist first; install and verify the replacement gate first (for example a `pre_gateway_dispatch` hook or equivalent intake guard that checks Telegram `getChatMember` and the roster/CRM), then broaden the gateway allowlist so member messages reach the bot. Treat Telegram statuses `member`, `administrator`, and `creator` as verified membership. See `references/member-facing-telegram-concierge-bot.md`.
8. For member-facing concierge bots, prefer one dedicated Telegram bot + one dedicated Hermes profile for the community workflow, not a separate Hostinger bot/server per member. Keep the owner's private/admin Hermes bot separate, first test with the owner's numeric Telegram ID allowlisted, then deliberately broaden access to member IDs, open/public access, channel-membership gating, or an approval/intake workflow. Put `/start` welcome/intake behavior in the concierge profile's active `SOUL.md` and/or an installed class-level concierge skill under that profile. If using channel-membership gating, remove/relax the gateway hard allowlist so member messages reach the bot, then verify the sender with Telegram metadata before asking intake questions. See `references/member-facing-telegram-concierge-bot.md`.
9. For Success Circles Buddy Concierge specifically, treat “limited” as two constraints: member-limited (`@mombud` + Airtable roster) and purpose-limited (pairing only, no admin/system actions). Implement the real membership/roster check before opening `TELEGRAM_ALLOWED_USERS` beyond the owner. A robust pattern is a profile-local plugin with `pre_gateway_dispatch` for Telegram `getChatMember` + Airtable `Team Roster` lookup, and `pre_tool_call` blocks for terminal/file/cron/memory/admin tools. See `references/buddy-concierge-membership-gate.md`.
- For Success Circles Buddy Concierge post-intake matching, keep design decisions one point at a time and verify with the user before implementation. Separate the Concierge access gate from recommendation candidate eligibility: access stays `Membership = Current` + `Team Roster = Yes`, while candidate recommendations may include `Reserve` members only under approved availability/backup rules. Store workflow events in a new Airtable table inside the existing base (not a new base), e.g. `Buddy Pairing Requests`, and notify `@successcircles` when a request reaches `Pending Admin Review`. If the member-facing profile blocks broad tools such as terminal/memory/skill editing, expose only a narrowly scoped profile-local plugin tool for the allowed Airtable workflow instead of enabling general admin tools. See `references/buddy-concierge-post-intake-workflow.md`.
11. When the user is confused or says the explanation was too much, switch to a short plain-English status first: what is true now, what is broken, and the next single action. Avoid long architecture explanations until they ask for detail.
11. Before editing a profile's gateway config, skills, memories, or instructions, ask Hermes for the active profile paths and use those exact paths:
   - `hermes --profile PROFILE config path`
   - `hermes --profile PROFILE config env-path`
   Do not assume `~/.hermes/profiles/PROFILE`; Hostinger/container installs may use paths such as `/opt/data/profiles/PROFILE`.

## Pitfalls and fixes

- For Hostinger/container profiles, never assume profile files live under `~/.hermes/profiles/PROFILE`. First run `hermes --profile PROFILE config path` and `hermes --profile PROFILE config env-path`, then edit files under the returned profile root. If instructions were written to the wrong profile path, the running bot will keep using old behavior even after restart.
- When managing multiple Hermes gateways on the same VPS, do not use broad kill patterns like `pkill -f "hermes.*gateway"`; this can stop the user's active/admin assistant gateway too. Kill only the target profile, for example `pkill -f "hermes --profile buddy-concierge gateway run"`, or use profile-scoped `gateway run --replace` if supported.
- If a member-facing bot responds to a phrase like “I want a buddy” but `/start` appears silent, the Telegram gateway is connected; treat it as a command-handling/instruction issue rather than a token or model outage. Inspect the active profile instructions and session logs before re-running setup. For profile-specific `/start` intake, a narrow adapter rewrite from `/start` to the natural-language trigger can work, but keep it scoped to that profile only.
- If a user says a Telegram reply is being replaced by an “update Telegram”/unsupported-message placeholder, do not keep rewriting prompts. First inspect gateway logs for `streamed=True`, normal-send suppression, MarkdownV2 parse failures, and actual `Sending response` lines. Disable Telegram streaming with `hermes config set display.platforms.telegram.streaming false` and restart; if normal sends still render as the placeholder, force Telegram plain-text compatibility mode (for example `HERMES_TELEGRAM_PLAIN_TEXT=1` plus `parse_mode=None`) and restart. While validating the fix, keep replies short and plain-text so the user can confirm whether Telegram displays them normally. See `references/telegram-update-placeholder.md`.
- If `hermes --profile buddy-concierge gateway install --system` says service installation is not needed inside a Docker container, do not keep trying systemd. Explain that Docker is the outer service manager: keep the profile gateway running inside the container with the narrow Buddy Concierge watchdog, and set the Hostinger/Docker restart policy to `unless-stopped` from hPanel/Docker Manager or host-side `docker update --restart unless-stopped CONTAINER`. If the watchdog cron job errors after root-side runs, check for root-owned logs such as `/opt/data/profiles/buddy-concierge/logs/gateway-watchdog.log` and fix with `chown hermes:hermes ...` before changing code.
- If the user asks whether the Concierge bot will keep running after Ctrl+C or terminal close, first inspect whether the profile gateway is foreground-attached or already detached/backgrounded, and check the process owner. Foreground `hermes --profile buddy-concierge gateway run` stops on Ctrl+C, but a detached/root-owned process cannot be stopped from the user's current terminal or by a non-root agent. Prefer a narrow profile-specific watchdog instead of broad process management: a script-only cron job can check only `hermes --profile buddy-concierge gateway run` every few minutes, stay silent when healthy, and restart only that profile if missing. Be clear that a watchdog restarts missing processes; it does not reload changed code/config while an old process is still running. In Hostinger Docker Projects, the visible `Restart` action may be only a manual project/container restart; if no auto-restart policy is exposed and `docker ps` cannot reach `/var/run/docker.sock` or `sudo` is absent, stop chasing Docker commands from that terminal and document the limitation: watchdog covers the gateway process while the project is running, but full project/container recovery depends on Hostinger's project restart behavior or support. See `references/buddy-concierge-24h-watchdog.md`.
- For member-facing community bots, distinguish two meanings of “limited”: (1) access-limited to verified members, and (2) scope-limited to the workflow. Do both. Use a pre-dispatch gate for access, then block/disable broad admin tools so the member bot cannot act as the owner’s general Hermes assistant.
- For Telegram channel-gated concierge access, `TELEGRAM_ALLOWED_USERS=*` / `GATEWAY_ALLOW_ALL_USERS=true` may be necessary so members can reach the bot at all, but only after a profile-specific pre-dispatch gate is installed. The gate should check `getChatMember(@channel, user_id)` and then check the backing CRM/Airtable roster before agent dispatch.
- If implementing a Hermes `pre_gateway_dispatch` plugin hook, accept `**kwargs` in the hook signature. Gateway versions may pass extra metadata such as `telemetry_schema_version`; a strict signature causes the gate to fail open into the old agent script.
- When gating against an Airtable roster, matching “has a record” is often not enough. Also check the active-membership/status field (for Success Circles, `Team Roster.Membership = Current`; `Past` and `Reserve` should not pass unless the user explicitly changes policy). Treat `Availability` as cycle availability, not membership status.
- When a member-facing bot still gives an old verification/intake response after a gate update, inspect logs for `pre_gateway_dispatch` hook errors before changing prompts; the prompt may be fine and the gate may be failing before it rewrites the message.
- If a bot replies with an internal notice such as model context/auto-compaction details, check display/interim settings and profile instructions; keep member-facing responses free of system/runtime notices where possible.
- If the concierge gives an old template response (for example `Pair [your name] with a Success Circles buddy`) after instruction changes, search the active profile root and verify that a class-level concierge skill is actually installed/enabled. If no concierge skill appears in `hermes --profile PROFILE skills list`, create/update an installed skill under the active profile and/or update the active profile `SOUL.md`, then restart only that profile's gateway.
- If a member-facing bot replies `I’m having trouble verifying your Momentum Buddy Reminders membership` even for the owner/admin, distinguish policy text from executable verification. First test Telegram `getChatMember('@mombud', user_id)` directly; if that succeeds, add/repair the real gate (plugin/webhook/tool) that performs membership + roster checks before the agent sees the message, then update `SOUL.md` so the agent trusts the injected verified-access block instead of trying to verify again.
- For member-facing community bots, do not equate “open to all members” with “open public access.” Relax gateway allowlists only after the pre-dispatch gate is installed. The gateway may need `TELEGRAM_ALLOWED_USERS=*` / `GATEWAY_ALLOW_ALL_USERS=true` so messages reach the gate, but the gate must fail closed for non-members and non-roster senders.
- Profile-specific logs may be under the active profile root (for example `/opt/data/profiles/PROFILE/logs/agent.log`) rather than `~/.hermes/profiles/PROFILE/logs/`. Use the active profile path to choose log paths.
- Profile clone syntax varies by Hermes version. If `hermes profile create NAME --clone default` fails with `unrecognized arguments: default`, use `hermes profile create NAME --clone` first; if that does not work, try `hermes profile create NAME --clone-from default`. Verify with `hermes profile list` and `hermes profile show NAME` before continuing.
- Avoid using `hermes --profile NAME chat -q ...` as the only verification step for first-time users on unknown installs; if it appears to restart into the interactive Hermes welcome/chat screen, have them exit with `/exit`, `/quit`, or Ctrl+C, then verify with `hermes profile show NAME` and proceed to `hermes --profile NAME gateway setup`.
- Telegram home channel and allowlist prompts require numeric IDs, not handles. If the user supplies `@name`, tell them to message `@userinfobot` and paste the numeric ID.
- Do not submit the default `Done` selection accidentally when the user asked for a specific platform. In interactive multi-select lists, first move focus to the platform, submit, then handle that platform's prompts.
- If the user pastes a bot token into chat, avoid repeating it. Mention token rotation as a safety recommendation if the transcript may be stored or shared.
- In Telegram setup, if the wizard asks whether to use the current user ID as the home channel, tell the user to choose `y` when they are the bot owner/admin. Explain that this sets the admin/home DM for notifications and does not by itself block members from using the bot.
- When a non-expert is stepping through `hermes --profile NAME gateway setup`, keep answers tightly tied to the current prompt rather than jumping ahead. Common prompt sequence: select `Telegram` → answer `y` to reconfigure for the new profile/bot token → paste BotFather token privately → enter allowed user IDs. For a first test, use only the owner/admin's numeric Telegram ID, then broaden access after end-to-end verification.
- If `hermes` is not on PATH but the binary is known, use the absolute binary for the task and separately help the user add it to their shell profile. Treat PATH issues as environment setup, not as a durable limitation of Hermes.
- If `hermes doctor` or gateway commands fail due file ownership/permissions in the active Hermes home, fix ownership/permissions when safe, then rerun the command to verify. Capture the fix and verification, not the transient error.
- Permission warnings can also come from agent-created skills under the active Hermes home (for example a `SKILL.md` owned by root and mode `600`). Fix the owning skill directory/file permissions, then rerun `hermes doctor` or restart the gateway to reload cleanly.
- After running config/auth flows such as `hermes model` as root, check `$HERMES_HOME/config.yaml` and `$HERMES_HOME/auth.json` ownership before restarting the gateway as `hermes`; root-owned files can make the gateway fall back to stale `.env` values or fail to read config.
- If a platform conflict reports a PID that is defunct/zombie, do not keep killing it (zombies cannot be killed). Inspect the scoped lock under `$HERMES_HOME/.local/state/hermes/gateway-locks/`; if the lock points to the confirmed zombie/gone PID, move the lock aside and restart the gateway. See `references/gateway-zombie-scoped-locks.md` for a safe recovery recipe.
- Gateway setup may finish with `Service install not supported on this platform`. This is not fatal; run the gateway in foreground or under an external supervisor.
- `hermes gateway run` normally does not return to the shell prompt while healthy. Non-fatal warnings can remain on screen (for example optional plugin warnings such as `raft CLI not found in path`) and make the terminal look stuck; if there is no `/opt/hermes#` prompt, treat it as likely still running and verify by messaging the bot before troubleshooting a crash.
- If foreground mode works but a durable service is unsupported, and `tmux -V` returns command-not-found, a lightweight fallback is:
  ```bash
  mkdir -p ~/.hermes/profiles/PROFILE/logs
  nohup hermes --profile PROFILE gateway run >> ~/.hermes/profiles/PROFILE/logs/gateway-background.log 2>&1 &
  ps aux | grep "PROFILE gateway run" | grep -v grep
  tail -40 ~/.hermes/profiles/PROFILE/logs/gateway-background.log
  ```
  Replace `PROFILE` with the target profile and then verify with a real Telegram message.
- If Telegram reports `bot token already in use (PID NNNN)`, inspect the PID before killing it: `ps -p NNNN -o user,pid,ppid,stat,cmd`. A `Z`/`<defunct>` zombie cannot be killed even with `kill -9`; its parent must reap it. If only a stale gateway/platform lock references that zombie, inspect and remove the stale lock/state file with user approval rather than repeatedly killing the PID.
- Gateway setup may finish with `Service install not supported on this platform`. This is not fatal; run the gateway in foreground or under an external supervisor.
- Telegram long-polling can emit transient `httpx.ReadError` warnings and schedule reconnects. Do not treat the first read error as fatal if the gateway process remains running. Check basic reachability to `https://api.telegram.org`, poll the gateway output for repeated attempts or exit, and ask the user to test `/start` in Telegram. Restart only if reconnect attempts keep repeating or the process exits.
- If the user says Telegram `/start` does nothing but `ps` shows the gateway is running, do not start another gateway copy. First triage the active profile logs and filter for platform-specific evidence:
  ```bash
  tail -120 ~/.hermes/profiles/PROFILE/logs/gateway-background.log | grep -i "telegram\|error\|failed\|conflict\|allowed\|unauthorized\|polling\|bot"
  tail -120 ~/.hermes/profiles/PROFILE/logs/gateway-background.log
  ```
  Also verify they are messaging the intended bot handle and that the tester's numeric Telegram ID is in the allowlist. Optional plugin warnings such as `hermes_plugin.raft_platform.adapter: [raft] raft CLI not found in PATH` are usually unrelated to Telegram delivery; keep looking for Telegram/bot/polling/allowlist/error lines before changing configuration.
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

- `references/profile-scoped-telegram-gateway-troubleshooting.md` — profile-scoped troubleshooting for multi-gateway Telegram bots: verify active `config path`/`env-path`, avoid broad `pkill` patterns that stop other gateways, diagnose allowlists, stale instructions, and `/start` being intercepted as a platform ping.
- `references/telegram-portal-setup-session.md` — concise transcript-derived notes for Telegram + Nous Portal setup, including numeric-ID prompts and foreground gateway startup.
- `references/telegram-gateway-reconnect-and-permissions.md` — Telegram reconnect warnings, numeric-ID env entries, and permission-fix patterns for gateway skill-loading warnings.
- `references/gateway-root-and-stale-telegram-pid.md` — root-guard-safe foreground gateway runs in containers and Telegram token conflicts caused by stale/zombie PIDs.
- `references/telegram-update-placeholder.md` — triage and fixes when Telegram clients show an “update Telegram”/unsupported-message placeholder despite Hermes generating a normal response; covers streaming disablement and plain-text compatibility mode.
- `references/member-facing-telegram-concierge-bot.md` — pattern for connecting members to a community concierge through one dedicated Telegram bot/profile, access broadening, and `/start` intake behavior.
- `references/buddy-concierge-gated-member-access.md` — concrete gated-access pattern for Success Circles Buddy Concierge: @mombud `getChatMember`, Airtable `Telegram Account`, `Membership = Current`, `Team Roster = Yes`, profile-local `pre_gateway_dispatch`/`pre_tool_call` plugin, and concise nontechnical status style.
- `references/buddy-concierge-24h-watchdog.md` — profile-specific watchdog pattern for keeping the Buddy Concierge gateway running after Ctrl+C/terminal close without touching the main Hermes gateway.
- `references/buddy-concierge-post-intake-workflow.md` — approved Success Circles Buddy Concierge v1 post-intake workflow: Airtable `Buddy Pairing Requests` table fields, access vs candidate eligibility, Joseph's scoring weights, member response flows, and admin backup alerts.
- `references/buddy-concierge-access-vs-recommendation-rules.md` — Success Circles distinction between strict Concierge bot access (Current-only) and broader recommendation candidate eligibility/scoring, including Reserve fallback, 10x compatibility, and Joseph’s pairing weights.
