# Hermes setup backup in a private GitHub repo

Use this when the user asks to connect Hermes to GitHub to save or back up the agent setup.

## Target model

Create a private repository that stores reproducible setup artifacts, not live runtime state.

Recommended repo layout:

```text
README.md
SECURITY.md
.gitignore
config/
  config.example.yaml
  env.example
skills/
scripts/
  backup-hermes-setup.py
  bootstrap-hermes-setup.sh
docs/
  how-it-works.md
cron/
```

## GitHub authentication options

Prefer `gh auth login` when available. If `gh` is not installed, use GitHub REST API with a fine-grained token from the host environment, never pasted into chat.

Repo creation endpoints:

- `POST /user/repos` — create under authenticated user.
- `POST /orgs/{org}/repos` — create under an organization.

Minimum fine-grained PAT permissions for backup pushes:

- `Contents: Read and Write`
- `Metadata: Read-only` (automatic)

Optional permissions only when needed:

- `Issues: Read and Write`
- `Pull requests: Read and Write`
- `Actions: Read`
- `Workflows: Write` only if Hermes should edit GitHub Actions workflows.

## What to commit

Usually safe after review/sanitization:

- `config.yaml` as `config/config.example.yaml`
- variable names from `.env` as `config/env.example` with blank values
- `skills/` excluding hidden curator/runtime metadata
- non-secret cron definitions
- setup docs and bootstrap/backup scripts

## What not to commit

Never commit:

- `.env` values, API keys, provider keys, Telegram bot tokens
- `auth.json`, `shared/nous_auth.json`, OAuth credential pools
- `state.db*`, `sessions/`, logs, transcripts, process files, locks
- npm/uv/cache directories and generated runtime artifacts

## Workflow

1. Load `github-operations` and `hermes-agent` if configuring Hermes itself.
2. Check auth and tools: `gh auth status`, `command -v gh`, `git --version`.
3. Confirm target owner/repo before creating a remote if not obvious.
4. Build a local sanitized scaffold first.
5. Initialize git, commit, then create/push to the private repo.
6. Verify the repo exists and is private by reading it back (`gh repo view` or REST API).

## Pitfalls

- Do not treat missing `gh`, missing token, or missing CLI binaries as durable tool limitations; give the install/auth step and continue when credentials are available.
- Do not read secret-bearing `.env` contents into the conversation. If variable names are needed, extract only keys and write blank values.
- If command approval blocks scaffold creation, report that nothing was written and ask the user to approve or provide a safer auth/setup path.
