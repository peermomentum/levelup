# Profile-scoped Telegram gateway troubleshooting

Use this reference when a Hermes Telegram bot/profile is running but replies incorrectly, ignores `/start`, or user access behaves unexpectedly.

## Safety first: profile-scoped restarts only

On hosts with multiple Hermes gateway profiles, never use broad kill patterns such as:

```bash
pkill -f "hermes.*gateway"
```

That can stop the user's main assistant gateway along with the target bot. Stop only the target profile:

```bash
pkill -f "hermes --profile <profile-name> gateway run"
```

Then restart that one profile:

```bash
nohup hermes --profile <profile-name> gateway run >> /path/to/profile/logs/gateway-background.log 2>&1 &
```

## Confirm the active profile paths before editing

Do not assume the active profile lives under `~/.hermes/profiles/<name>`. In containerized installs it may live somewhere else, e.g. `/opt/data/profiles/<name>`.

Before editing skills, memories, SOUL.md, config, or `.env`, ask the CLI for the actual paths:

```bash
hermes --profile <profile-name> config path
hermes --profile <profile-name> config env-path
```

Use those paths for all subsequent edits and log checks.

## When a bot is running but behavior ignores new instructions

1. Verify the profile path with `config path` / `env-path`.
2. Check `hermes --profile <profile-name> skills list` to confirm the intended custom skill is actually installed/enabled.
3. Search the active profile, not the default profile, for old templates or instructions.
4. For profile-personality behavior, update the active profile's `SOUL.md` as well as the relevant skill.
5. Restart only the target profile gateway.

## Telegram `/start` gotcha

Hermes Gateway may treat `/start` as a Telegram platform ping and ignore it before it reaches the agent. Logs may show:

```text
Ignoring /start platform ping for session ...
```

If a product bot needs `/start` as a real intake trigger, configure or implement a profile-specific command/hook/route that rewrites `/start` to the natural-language trigger (for example `I want a buddy`) rather than globally changing `/start` behavior for all Hermes gateways.

## Allowlist gotcha

If logs show:

```text
Unauthorized user: <id> (<name>) on telegram
```

then Telegram messages are reaching the gateway but are blocked before the agent sees them. Check both config and `.env` in the active profile for allowed-user settings, and restart the target profile after clearing or changing them.
