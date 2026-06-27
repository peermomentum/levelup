# Buddy Concierge 24h watchdog and restart notes

Use this reference for Success Circles / `buddy-concierge` profile uptime work.

## Goals

- Keep the member-facing Concierge gateway running continuously.
- Never stop/restart the main/default Hermes gateway by accident.
- Be explicit about what a watchdog can and cannot do.

## Safe process target

Only target the profile-specific command:

```bash
hermes --profile buddy-concierge gateway run
```

Avoid broad patterns such as `pkill -f "hermes.*gateway"` because they may stop the owner's main assistant gateway.

## Watchdog pattern

A script-only cron watchdog can run every few minutes and:

1. Search `/proc/*/cmdline` for the exact buddy-concierge gateway command.
2. If found, print nothing and exit 0.
3. If missing, start only:
   ```bash
   /opt/hermes/.venv/bin/hermes --profile buddy-concierge gateway run
   ```
   with stdout/stderr redirected to the buddy profile log directory.
4. Print a short alert only when it had to restart the bot.

This provides recovery after accidental Ctrl+C, terminal close, or process exit, as long as the VPS/container and Hermes cron scheduler are running.

## Hostinger Docker Projects limitation

In Hostinger's Docker Projects UI, the project/container menu may expose only a manual `Restart` action and no visible auto-restart/restart-policy control. If the user's terminal says `Cannot connect to the Docker daemon at unix:///var/run/docker.sock` and `sudo` is unavailable, do not keep steering them through host Docker commands from that terminal. Treat it as a managed/containerized project where:

- The Concierge watchdog can restart the `buddy-concierge` gateway process while the Hermes project/container is alive.
- The watchdog cannot run if the entire Hostinger project/container is stopped.
- The visible `3 dots → Restart` action is a manual recovery button for the whole project/container, not proof of automatic 24/7 restart policy.
- For full container auto-start after VPS reboot/crash, the user may need a Hostinger setting not exposed in the current UI or Hostinger support.

## Watchdog log permission hardening

If a prior root-owned watchdog run created `/opt/data/profiles/buddy-concierge/logs/gateway-watchdog.log`, later watchdog runs as the `hermes` user may fail on `PermissionError`. Prefer either fixing ownership:

```bash
chown hermes:hermes /opt/data/profiles/buddy-concierge/logs/gateway-watchdog.log
```

or hardening the watchdog script to fall back to a hermes-owned log path such as `gateway-watchdog-hermes.log` or `/tmp/buddy-concierge-gateway-watchdog.log` when the preferred log path is not writable.

## Important limitation

If `hermes --profile buddy-concierge gateway install --system` replies:

```text
Service installation is not needed inside a Docker container.
The container runtime is your service manager — use Docker restart policies instead
```

then stop trying systemd/service install from inside the container. Use a two-layer uptime plan:

1. **Inside the container:** run or watchdog only the profile-specific gateway command:
   ```bash
   /opt/hermes/.venv/bin/hermes --profile buddy-concierge gateway run
   ```
2. **Outside the container / Hostinger hPanel:** set the Docker container restart policy to `unless-stopped` (or enable the UI auto-restart toggle). If host Docker CLI is available, the host-side command is:
   ```bash
   docker update --restart unless-stopped CONTAINER_NAME_OR_ID
   ```

For Hostinger users, say plainly that Docker restart policy is configured in **hPanel → VPS → Docker Manager / Docker Profiles**, not inside the container Terminal.

If the Buddy Concierge watchdog job shows `last_status=error`, check profile log ownership before changing code. A common post-root-run issue is a root-owned watchdog log:

```bash
chown hermes:hermes /opt/data/profiles/buddy-concierge/logs/gateway-watchdog.log
```

Then rerun/check the watchdog and `hermes --profile buddy-concierge gateway status`.

## Important limitation

A watchdog only starts the bot when no matching process exists. It does not reload changed code, config, skills, or `.env` while an old gateway process is still running.

Before telling the user to press Ctrl+C, inspect whether the process is attached to their terminal and who owns it:

```bash
ps aux | grep "hermes --profile buddy-concierge gateway run" | grep -v grep
```

If the process is already detached/backgrounded, Ctrl+C in the current terminal will not affect it. If the process is owned by `root` and the agent runs as an unprivileged user, the agent/watchdog may not be able to stop it (`PermissionError: Operation not permitted`). In that case, tell the user plainly that a root/admin-level restart is needed, or use an application-level `/restart` only if verified for that specific bot/profile.

## Access-rule reload lesson

For Buddy Concierge access changes such as `Membership = Current` vs `Current,Reserve`, update both:

- `/opt/data/profiles/buddy-concierge/plugins/buddy_concierge_gate/__init__.py`
- `/opt/data/profiles/buddy-concierge/.env` (`BUDDY_CONCIERGE_ACTIVE_MEMBERSHIP_VALUES`)
- profile instructions/skill text if member-facing wording changed

Then restart the running `buddy-concierge` gateway so the new environment and plugin code are loaded.

## Current access policy reminder

As of the correction captured from the user, Concierge bot access should require:

- Telegram member/admin/creator of `@mombud`
- Airtable roster match by Telegram account
- `Membership = Current`
- `Team Roster = Yes`

Do not treat `Reserve` as having bot access unless the user explicitly changes the access policy again. Candidate recommendation rules may be different from bot-access rules; keep those separate.
