# Telegram gateway setup notes

Session-derived troubleshooting notes for configuring Hermes Gateway with Telegram in containerized/default-profile installs.

- If `hermes` is not on PATH but the repo/install is under `/opt/hermes`, verify `/opt/hermes/bin/hermes` and add it with `export PATH="/opt/hermes/bin:$PATH"`; persist in `~/.bashrc` if the user wants command-style usage.
- `hermes gateway setup` may report `Service install not supported on this platform`; run the gateway in foreground or a managed background process instead: `hermes gateway run`.
- Telegram setup prompts for:
  1. Bot token from `@BotFather`.
  2. Allowed user IDs — use numeric Telegram IDs, not usernames; get them from `@userinfobot`.
  3. Home channel ID — for DMs, use the same numeric Telegram user ID, or set later from Telegram.
- If the gateway warns `No user allowlists configured`, set `TELEGRAM_ALLOWED_USERS=<numeric_id>` in the active Hermes `.env` and restart the gateway. Do not set open access unless the user explicitly wants it.
- If a user pastes a Telegram bot token into chat, warn that it should be rotated in `@BotFather` if the transcript may be stored or shared.
- A Telegram `httpx.ReadError` during long polling can be transient. First verify the process is still running and basic connectivity to `https://api.telegram.org`; if reachable, wait for reconnect before restarting.
- Permission errors reading files under `HERMES_HOME` (for example `config.yaml`, `memories/USER.md`, or `skills/.../SKILL.md`) can occur after commands ran as root. Fix ownership back to the Hermes runtime user, then rerun `hermes doctor` or restart the gateway.
- In minimal containers, `tmux` may not be installed; use Hermes' tracked background process or install `tmux` before recommending a tmux workflow.
