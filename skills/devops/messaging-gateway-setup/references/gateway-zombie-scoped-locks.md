# Gateway zombie scoped locks and ownership recovery

Use when `hermes gateway run` reports a platform identity conflict such as:

```text
Telegram bot token already in use (PID <pid>). Stop the other gateway first.
```

but `ps` shows that PID is defunct/zombie (`STAT` contains `Z`, cmd is `[hermes] <defunct>`).

## Diagnosis

1. Check the reported PID:

```bash
ps -p <pid> -o user,pid,ppid,stat,cmd
```

2. Inspect gateway scoped locks:

```bash
find "$HERMES_HOME/.local/state/hermes/gateway-locks" -maxdepth 1 -type f -name '*.lock' -printf '%M %u:%g %p\n'
```

For Telegram token conflicts, expect a file like:

```text
$HERMES_HOME/.local/state/hermes/gateway-locks/telegram-bot-token-<hash>.lock
```

3. Read the lock JSON and verify it points to the zombie PID. The lock file contains fields like `pid`, `scope`, `identity_hash`, and `start_time`.

## Safe recovery

Only move/remove the scoped lock if the referenced PID is confirmed zombie or gone. Prefer moving it aside instead of deleting it:

```bash
python3 - <<'PY'
import json, shutil, time
from pathlib import Path

locks = Path('/opt/data/.local/state/hermes/gateway-locks')
for lock in locks.glob('telegram-bot-token-*.lock'):
    rec = json.loads(lock.read_text())
    pid = int(rec.get('pid', -1))
    state = None
    status = Path(f'/proc/{pid}/status')
    if status.exists():
        for line in status.read_text().splitlines():
            if line.startswith('State:'):
                state = line
                break
    print(f'{lock}: pid={pid} {state}')
    if state and '\tZ' in state:
        backup = lock.with_suffix(lock.suffix + f'.stale-{int(time.time())}')
        shutil.move(str(lock), str(backup))
        print(f'moved stale zombie-owned lock to {backup}')
PY
```

Then restart the gateway as the non-root `hermes` user:

```bash
su -s /bin/bash hermes -c 'cd /opt/hermes && /opt/hermes/.venv/bin/hermes gateway run'
```

## Ownership pitfall after running setup/model commands as root

Interactive commands such as `hermes model` may rewrite files in `$HERMES_HOME`. If they were run as root, later gateway runs as `hermes` can fail with config/auth permission errors.

Check and repair:

```bash
stat -c '%A %U:%G %n' /opt/data/config.yaml /opt/data/auth.json
chown hermes:hermes /opt/data/config.yaml /opt/data/auth.json
chmod 600 /opt/data/config.yaml /opt/data/auth.json
```

Avoid recording this as "gateway is broken". The durable lesson is: verify ownership after root-run configuration commands, repair it, clear stale zombie-owned scoped locks only after proving the PID is zombie/gone, then restart as `hermes`.
