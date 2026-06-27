# Telegram “update Telegram” placeholder / blocked-looking replies

Use when a user reports that Hermes replies are being replaced by an “update Telegram”/unsupported-message placeholder, or that the response appears blocked/replaced on Telegram even though logs show a normal send.

## Triage pattern

1. Check the active gateway logs before changing prompts:
   - `tail -200 $HERMES_HOME/logs/gateway.log`
   - Look for `response ready`, `Sending response`, `Suppressing normal final send`, `streamed=True`, `MarkdownV2 parse failed`, Telegram `BadRequest`, or repeated restarts.
2. Distinguish two causes:
   - Streaming/edit-message path: logs may show `streamed=True` and final normal send suppressed. Disable Telegram streaming and restart the gateway.
   - MarkdownV2/client rendering path: logs show a normal `Sending response` with no parse failure, but the user’s Telegram client displays an update/unsupported placeholder. Force plain text delivery.
3. Keep user-facing replies short and plain while diagnosing so the user can confirm delivery.

## Config fix for streaming path

Use Hermes config, not direct file patching, for the main profile:

```bash
hermes config set display.platforms.telegram.streaming false
```

Then restart the gateway from outside the running gateway process. If the user sends `/restart`, expect a short interruption and verify it came back with logs such as `Connected to Telegram` and `Gateway running`.

## Plain-text compatibility workaround

If disabling streaming is not enough and the Bot API accepts the send but the Telegram client still shows the update placeholder, force plain-text Telegram sends for that environment. A practical implementation is an env flag such as:

```bash
HERMES_TELEGRAM_PLAIN_TEXT=1
```

and a Telegram adapter branch that sends `parse_mode=None` after converting MarkdownV2-formatted text back to readable plain text. This avoids MarkdownV2/rich-message client compatibility issues. Restart the gateway after enabling the flag.

## Pitfalls

- Do not assume the bot prompt is wrong when the user says the visible Telegram message is wrong; first check whether the gateway delivered a different formatted/streamed message than expected.
- Do not restart the gateway from inside the gateway process with a shell command; Hermes blocks this because the child command would die with the gateway. Ask the user to use `/restart` or restart from an external shell/service manager.
- A restart can make the assistant appear temporarily “bugged.” Verify process/log state before continuing.
