# Gateway root guard and stale Telegram PID conflicts

Session-derived troubleshooting notes for running `hermes gateway run` inside the official Docker/container image.

## Root guard

If `hermes gateway run` is executed as root inside the official Docker image, Hermes may refuse to start:

```text
Refusing to run the Hermes gateway as root inside the official Docker image.
The image entrypoint normally drops privileges to the 'hermes' user.
Set HERMES_ALLOW_ROOT_GATEWAY=1 only if you intentionally accept this risk.
```

Preferred fix: run the gateway as the `hermes` user rather than bypassing the guard:

```bash
su -s /bin/bash hermes -c 'cd /opt/hermes && /opt/hermes/.venv/bin/hermes gateway run'
```

Use `HERMES_ALLOW_ROOT_GATEWAY=1` only after explicit user approval, because root-owned files in `$HERMES_HOME` can break later non-root runs.

## Telegram token already in use with a defunct PID

Gateway startup can fail with:

```text
Telegram bot token already in use (PID NNNN). Stop the other gateway first.
```

Before killing anything, inspect the PID:

```bash
ps -p NNNN -o user,pid,ppid,stat,cmd
```

If it shows `STAT` containing `Z` and `CMD` like `[hermes] <defunct>`, it is a zombie process. `kill` and `kill -9` will not remove a zombie; only its parent can reap it. If `PPID` is `1` and PID 1 does not reap it, restarting the container/init process may be needed.

Do not repeatedly retry `kill -9` on a zombie. Instead, treat the gateway's token-in-use record as potentially stale and inspect gateway/platform lock or state files before starting another gateway. If a stale lock/state file only references the zombie PID and no live process owns the token, remove the stale record with user approval, then rerun the gateway.

## Related permission hygiene

If earlier commands were run as root, verify `$HERMES_HOME` files used by config/memory/gateway are owned by `hermes` and readable by the gateway user, for example:

```bash
chown hermes:hermes /opt/data/config.yaml /opt/data/memories/USER.md
chmod 600 /opt/data/config.yaml /opt/data/memories/USER.md
```

Then rerun `hermes doctor` as a verification step before restarting the gateway when practical.
