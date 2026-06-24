# Stale Telegram token lock held by zombie PID

When `hermes gateway run` exits with:

```text
Telegram bot token already in use (PID <pid>). Stop the other gateway first.
```

but `ps -p <pid> -o user,pid,ppid,stat,cmd` shows the PID is defunct/zombie (`STAT` contains `Z`, command like `[hermes] <defunct>`), killing the PID will not help. The scoped Telegram token lock can remain on disk and block startup.

Useful diagnosis:

```bash
ps -p <pid> -o user,pid,ppid,stat,cmd
find /opt/data/.local/state/hermes/gateway-locks -maxdepth 1 -type f -name 'telegram-bot-token-*.lock*' -printf '%M %u:%g %p\n'
python3 - <<'PY'
import json
from pathlib import Path
lock_dir = Path('/opt/data/.local/state/hermes/gateway-locks')
for lock in lock_dir.glob('telegram-bot-token-*.lock'):
    rec = json.loads(lock.read_text())
    pid = int(rec.get('pid', -1))
    state = None
    status = Path(f'/proc/{pid}/status')
    if status.exists():
        for line in status.read_text().splitlines():
            if line.startswith('State:'):
                state = line
                break
    print(lock, 'pid=', pid, state)
PY
```

If the lock PID is confirmed zombie, move the lock aside rather than repeatedly killing the PID:

```bash
lock=/opt/data/.local/state/hermes/gateway-locks/telegram-bot-token-<hash>.lock
mv "$lock" "$lock.stale-$(date +%s)"
```

Then restart the gateway as the `hermes` user inside the official Docker image:

```bash
su -s /bin/bash hermes -c 'cd /opt/hermes && /opt/hermes/.venv/bin/hermes gateway run'
```

Why: zombie processes still satisfy simple PID-exists checks, but cannot own a useful running gateway. The gateway's scoped lock file is a separate on-disk guard keyed by Telegram bot-token hash; once verified stale, removing/moving it clears the false conflict.
