# Telegram gateway reconnect and permissions notes

Session-derived operational notes for Hermes Telegram gateway setup and runtime checks.

## Numeric Telegram IDs

Telegram allowlist and home-channel prompts expect numeric user IDs, not `@username` handles. If the user provides a handle, ask them to message `@userinfobot` and paste the numeric `Id` value.

Common env entries after setup:

```env
TELEGRAM_BOT_TOKEN=<redacted>
TELEGRAM_HOME_CHANNEL=<numeric_user_id>
TELEGRAM_ALLOWED_USERS=<numeric_user_id>
```

Prefer `TELEGRAM_ALLOWED_USERS` over `GATEWAY_ALLOW_ALL_USERS=true` unless the user explicitly wants open access.

## Runtime reconnect warnings

A running gateway may log:

```text
WARNING gateway.platforms.telegram: [Telegram] Telegram network error, scheduling reconnect: httpx.ReadError
WARNING gateway.platforms.telegram: [Telegram] Telegram network error (attempt 1/10), reconnecting in 5s.
```

Treat this as a reconnect condition, not immediate failure, when the process remains running. Verify:

1. Gateway process is still alive.
2. Telegram API is reachable, e.g. `https://api.telegram.org` returns HTTP 200.
3. Reconnect attempts do not keep climbing to the limit or terminate the process.
4. User can message `/start` and then a normal message to the bot.

Restart the gateway only after repeated reconnect failures or process exit.

## Permission warnings from skill files

Gateway startup may warn that it cannot parse an agent-created skill file due `Permission denied`, often because a prior root-run command created a skill directory or `SKILL.md` owned by root with restrictive mode.

Fix pattern:

```bash
stat -c '%A %U:%G %n' /opt/data/skills/<category>/<skill>/SKILL.md
chown -R hermes:hermes /opt/data/skills/<category>/<skill>
hermes doctor
# restart gateway if it was already running so skill loading is clean
```

Capture the verification result, not the transient permission failure, as the durable lesson.
