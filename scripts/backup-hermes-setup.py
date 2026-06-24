#!/usr/bin/env python3
"""Create a sanitized backup of this Hermes setup.

This script intentionally backs up reproducible setup artifacts only.
It excludes live runtime state, logs, sessions, databases, OAuth files,
credential stores, and secret values.
"""
from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

SOURCE = Path(os.environ.get("HERMES_BACKUP_SOURCE", "/opt/data")).resolve()
DEST = Path(os.environ.get("HERMES_BACKUP_DEST", "/opt/data/levelup")).resolve()

SECRET_KEY_RE = re.compile(r"(api[_-]?key|token|secret|password|credential|auth|bearer|private[_-]?key)", re.I)
GENERATED_DIRS = ["config", "skills", "cron", "docs"]


def reset_generated_dirs() -> None:
    for rel in GENERATED_DIRS:
        path = DEST / rel
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)


def redact_yamlish(text: str) -> str:
    out: list[str] = []
    for line in text.splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key = line.split(":", 1)[0]
            if SECRET_KEY_RE.search(key):
                prefix = line.split(":", 1)[0] + ":"
                out.append(prefix + " \"\"")
                continue
        out.append(line)
    return "\n".join(out).rstrip() + "\n"


def write_config_examples() -> None:
    cfg = SOURCE / "config.yaml"
    if cfg.exists():
        (DEST / "config" / "config.example.yaml").write_text(redact_yamlish(cfg.read_text(errors="replace")))
    env = SOURCE / ".env"
    keys: list[str] = []
    if env.exists():
        for raw in env.read_text(errors="replace").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key = line.split("=", 1)[0].strip()
            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", key):
                keys.append(key)
    env_example = "# Secret values intentionally omitted. Fill these locally.\n" + "\n".join(f"{k}=" for k in sorted(set(keys))) + "\n"
    (DEST / "config" / "env.example").write_text(env_example)


def ignore_skill(path: str, names: list[str]) -> set[str]:
    ignored = set()
    for name in names:
        p = Path(path) / name
        if name.startswith("."):
            ignored.add(name)
        elif name in {"__pycache__", "node_modules", ".venv", "venv"}:
            ignored.add(name)
        elif p.is_file() and p.suffix.lower() in {".pyc", ".log", ".db", ".sqlite"}:
            ignored.add(name)
    return ignored


def copy_skills() -> None:
    src = SOURCE / "skills"
    dst = DEST / "skills"
    if src.exists():
        shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore_skill)


def summarize_cron() -> None:
    jobs_path = SOURCE / "cron" / "jobs.json"
    summary = []
    if jobs_path.exists():
        try:
            data = json.loads(jobs_path.read_text(errors="replace"))
            jobs = data.get("jobs", data if isinstance(data, list) else [])
            for job in jobs:
                if not isinstance(job, dict):
                    continue
                summary.append({
                    "id": job.get("id") or job.get("job_id"),
                    "name": job.get("name"),
                    "schedule": job.get("schedule"),
                    "enabled": job.get("enabled"),
                    "deliver": job.get("deliver"),
                    "skills": job.get("skills"),
                    "workdir": job.get("workdir"),
                })
        except Exception as exc:
            summary = [{"error": f"Could not parse cron/jobs.json: {exc}"}]
    (DEST / "cron" / "jobs.example.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")


def write_docs() -> None:
    (DEST / "README.md").write_text("""# levelup

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
""")
    (DEST / "SECURITY.md").write_text("""# Security

Do not commit secrets to this repository.

This backup intentionally excludes secret values and live runtime state. Before making this repository public or sharing it, review changes with:

```bash
git status --short
git diff --cached
```

If a token was ever pasted into chat or committed by mistake, revoke it immediately in GitHub and generate a new fine-grained token scoped only to this repository.
""")
    (DEST / "docs" / "how-it-works.md").write_text("""# How this backup works

`scripts/backup-hermes-setup.py` reads the local Hermes home at `/opt/data`, writes sanitized files into this repository, and avoids runtime/secret-bearing files.

The scheduled job runs the script, commits any resulting changes, and pushes to GitHub.
""")
    (DEST / ".gitignore").write_text("""# Local/runtime files
.env
*.log
*.db
*.db-shm
*.db-wal
__pycache__/
.venv/
venv/
node_modules/

# Hermes runtime state that should not be backed up
state.db*
auth.json
sessions/
logs/
processes.json
gateway*.json
gateway*.pid
gateway*.lock
cron/output/
.local/
.config/git/
.hermes_history
""")
    bootstrap = DEST / "scripts" / "bootstrap-hermes-setup.sh"
    bootstrap.write_text("""#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "This repo contains a sanitized Hermes setup backup: $repo_dir"
echo "Copy config/config.example.yaml to your Hermes config path and fill secrets from config/env.example locally."
""")
    bootstrap.chmod(0o755)


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    reset_generated_dirs()
    write_config_examples()
    copy_skills()
    summarize_cron()
    write_docs()
    print(f"Sanitized backup written to {DEST}")


if __name__ == "__main__":
    main()
