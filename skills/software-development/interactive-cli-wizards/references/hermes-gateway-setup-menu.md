# Hermes gateway setup menu pitfall

Session-specific lesson: while running `hermes gateway setup` in a PTY, the menu showed many platforms and the current highlighted item was `Done`. The user then replied `Telegram`, but Enter had already been sent, causing the wizard to exit with "Skipped (keeping current)" rather than opening the Telegram configuration.

Reusable lesson:

- Poll the live PTY after each user reply before sending input.
- Treat `Done` as a potentially destructive/default-exit selection.
- If the user names an option, navigate to that option first; do not submit the highlighted default.
- If the process exits before the choice can be applied, report the actual result and provide the rerun command.

Do not preserve the session's local binary path as a general rule; PATH and install location are environment-dependent.
