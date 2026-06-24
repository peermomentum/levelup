# levelup

Sanitized backup of the Hermes Agent setup for `peermomentum/levelup`.

This repository is generated from `/opt/data` by `scripts/backup-hermes-setup.py`.
It stores reproducible setup artifacts, not live runtime state.

Included:
- Redacted Hermes config example
- Environment variable names with blank values
- Skills, excluding hidden curator/runtime metadata
- Sanitized cron job metadata
- Backup/bootstrap scripts

Excluded:
- `.env` values and tokens
- `auth.json` and OAuth credentials
- `state.db*`, sessions, logs, process files, locks, caches, and runtime output
