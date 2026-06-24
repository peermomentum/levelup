# Telegram stale scoped lock held by zombie PID

## When this applies

Gateway startup exits with an error like:

```text
Telegram bot token already in use (PID 1006). Stop the other gateway first.
```

but process inspection shows the referenced PID is a zombie/defunct Hermes process:

```bash
ps -p 1006 -o user,pid,ppid,stat,cmd
# hermes  1006  1  Zs  [hermes] <defunct>
```

A zombie cannot be removed with `kill` or `kill -9`; only its parent can reap it. Hermes may still see the token-scoped gateway lock as occupied because the lock file points at that PID.

## Diagnostic steps

1. Confirm the PID state:

```bash
ps -p <PID> -o user,pid,ppid,stat,cmd
cat /proc/<PID>/status | grep '^State:'
```

`State:\tZ (zombie)` confirms it is a stale owner candidate.

2. Find gateway scoped locks:

```bash
find "$HERMES_HOME" -maxdepth 5 \
  \( -path '*/gateway-locks/*' -o -name 'gateway.lock' -o -name 'gateway_state.json' \) \
  -printf '%M %u:%g %p\n' 2>/dev/null | sort
```

Common path in the official container:

```text
$HERMES_HOME/.local/state/hermes/gateway-locks/telegram-bot-token-<hash>.lock
```

3. Read the candidate lock JSON and verify it references the same zombie PID and scope:

```bash
python3 - <<'PY'
import json
from pathlib import Path
for p in Path('/opt/data/.local/state/hermes/gateway-locks').glob('telegram-bot-token-*.lock'):
    print(p)
    print(json.dumps(json.loads(p.read_text()), indent=2))
PY
```

## Safe stale-lock removal pattern

Only move the lock aside after both conditions are true:

- the lock JSON `pid` matches the conflict PID;
- `/proc/<pid>/status` reports `State: Z`.

Example:

```bash
python3 - <<'PY'
import json, shutil, time
from pathlib import Path

lock = Path('/opt/data/.local/state/hermes/gateway-locks/telegram-bot-token-<hash>.lock')
rec = json.loads(lock.read_text())
pid = int(rec['pid'])
state_line = ''
for line in Path(f'/proc/{pid}/status').read_text().splitlines():
    if line.startswith('State:'):
        state_line = line
        break
print(f'lock={lock}')
print(f'pid={pid}')
print(state_line)
if '\tZ' not in state_line:
    raise SystemExit('refusing: PID is not confirmed zombie')
backup = lock.with_suffix(lock.suffix + f'.stale-{int(time.time())}')
shutil.move(str(lock), str(backup))
print(f'moved stale lock to {backup}')
PY
```

Then restart the gateway as the non-root Hermes user:

```bash
su -s /bin/bash hermes -c 'cd /opt/hermes && /opt/hermes/.venv/bin/hermes gateway run'
```

Verify that the new gateway process remains running and no longer reports the token conflict.

## Notes

- Do not record this as "Telegram gateway is broken"; the durable lesson is the stale scoped-lock cleanup pattern.
- `kill`/`kill -9` not clearing a zombie is expected Linux behavior.
- Prefer moving the lock to a `.stale-<timestamp>` backup over deleting it outright, so the previous record remains available for diagnosis.
