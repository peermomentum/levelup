# Telegram gateway + Nous Portal setup notes

Session-derived operational notes for future Hermes gateway setup work.

## Sequence that worked

1. Ensure `hermes` resolves on PATH, or use the absolute binary while fixing PATH separately.
   - Example PATH line: `export PATH="/opt/hermes/bin:$PATH"`
2. Run `hermes gateway setup` in a PTY and select `Telegram` explicitly.
3. If Telegram is already configured and the user wants a new token, answer `y` to `Reconfigure Telegram?`.
4. Enter the bot token from `@BotFather` without echoing it back in summaries.
5. At `Allowed user IDs`, prefer a numeric Telegram ID allowlist. Leaving it blank can lead to gateway warnings/denials depending on policy.
6. At `Home channel ID`, enter the same numeric Telegram DM user ID when appropriate, or set it later from Telegram.
7. When setup says service install is unsupported, start with `hermes gateway run` instead of treating setup as failed.
8. If gateway startup warns `No user allowlists configured`, add `TELEGRAM_ALLOWED_USERS=<numeric_id>` to the active Hermes `.env` and restart the gateway.
9. If the user asks for `tmux new -s hermes-gateway`, first check whether `tmux` exists. If it is missing, do not claim a tmux session exists; offer package installation or use a tracked background process instead.
10. If moving an already-running gateway into tmux/supervision, avoid duplicate pollers: stop the tracked gateway process before starting the supervised one, then verify the replacement is running.

## User-facing prompts to remember

- Telegram ID must be numeric; `@username` is not accepted for home channel/allowlist prompts.
- To find the numeric ID, tell the user to message `@userinfobot`.
- If a bot token was pasted into chat, advise rotating it in `@BotFather` if the transcript may be stored or shared.

## Verification

- Run `hermes doctor` after setup; verify `python-telegram-bot` is installed and config parses.
- Start gateway and poll output; absence of the allowlist warning is a useful sign, but end-to-end verification requires the user to DM the bot.
