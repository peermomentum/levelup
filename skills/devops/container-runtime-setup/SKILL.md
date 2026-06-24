---
name: container-runtime-setup
description: "Install, verify, and troubleshoot Docker/container runtimes across Linux hosts, rootless setups, and managed/containerized environments."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [devops, docker, containers, linux, setup, troubleshooting]
    created_by: agent
---

# Container Runtime Setup

Use this when the user asks to install, enable, verify, or troubleshoot Docker or another local container runtime on a Linux machine.

## Core principle

Do not treat `docker --version` as proof that Docker is installed and working. A working Docker setup needs:

1. A client CLI (`docker`).
2. A container engine/daemon or rootless engine (`dockerd`, `containerd`, etc.).
3. A reachable socket (`/var/run/docker.sock` for rootful Docker, `$XDG_RUNTIME_DIR/docker.sock` for rootless Docker).
4. User permissions to access the socket or a rootless context.
5. A successful runtime verification such as `docker run hello-world`.

## Workflow

### 1. Discover the current state first

Run checks before installing or declaring success:

```bash
id
. /etc/os-release && printf '%s %s (%s)\n' "$NAME" "$VERSION_ID" "$VERSION_CODENAME"
docker --version || true
docker compose version 2>/dev/null || docker-compose --version 2>/dev/null || true
docker info 2>&1 || true
ls -l /var/run/docker.sock 2>&1 || true
command -v dockerd containerd rootlesskit dockerd-rootless-setuptool.sh newuidmap slirp4netns fuse-overlayfs 2>/dev/null || true
```

If `systemctl` or `service` exists, check daemon state:

```bash
systemctl is-active docker 2>&1 || true
service docker status 2>&1 || true
```

### 2. Classify the environment

Pick the install path based on what discovery shows:

- Root/admin available: install rootful Docker through the OS package manager or Docker's official repo.
- No root/admin but user namespaces are available: attempt rootless Docker after verifying prerequisites.
- Running inside a managed container/CI/agent sandbox: the user may need the host/admin to install Docker or mount a Docker socket.
- CLI exists but daemon/socket is missing: report "Docker CLI only" and install/start the engine, not the client again.

### 3. Rootful Docker: Debian/Ubuntu quick path

For Debian/Ubuntu hosts where distro packages are acceptable:

```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
```

Then start a new login session and verify:

```bash
docker run --rm hello-world
docker compose version
```

If `sudo` is unavailable but the session is root, omit `sudo`. If neither root nor sudo is available, do not claim installation succeeded; provide the admin commands the user must run.

### 4. Rootless Docker path

Rootless Docker is useful when the user lacks root for day-to-day container use, but initial prerequisites often still require root/admin installation.

Check prerequisites:

```bash
grep "^$USER:" /etc/subuid /etc/subgid 2>/dev/null || true
command -v newuidmap newgidmap rootlesskit slirp4netns fuse-overlayfs 2>/dev/null || true
```

Typical Debian/Ubuntu prerequisites:

```bash
sudo apt-get install -y uidmap dbus-user-session slirp4netns fuse-overlayfs iptables
```

Then run the installer:

```bash
curl -fsSL https://get.docker.com/rootless -o /tmp/get-docker-rootless.sh
sh /tmp/get-docker-rootless.sh
```

After installation, export the environment printed by the installer, commonly:

```bash
export PATH="$HOME/bin:$PATH"
export DOCKER_HOST="unix://$XDG_RUNTIME_DIR/docker.sock"
```

Verify with:

```bash
docker info
docker run --rm hello-world
```

### 5. Managed/containerized environments

If the current session is inside a container or restricted VM and cannot install packages/start daemons, the host/admin can either install Docker on the host or mount the host socket into the environment:

```bash
-v /var/run/docker.sock:/var/run/docker.sock
```

Make clear that socket mounting gives the container broad control over the host Docker daemon; it is a trust boundary decision.

## Pitfalls

- `docker --version` only proves the CLI exists; always run `docker info` or `docker run hello-world` before saying Docker works.
- Missing `systemctl`/`service` means the environment may not have a normal init system; do not assume daemon management commands are available.
- If package installation fails for permissions, capture the fix as root/admin commands, not as a durable claim that Docker cannot work on the machine.
- Rootless install scripts may suggest installing `uidmap`, `iptables`, or related packages. Those are prerequisites, not proof that rootless Docker is impossible.
- Docker group membership requires a new login session before non-root access works.
- Do not silently switch to Podman unless the user agrees; Docker compatibility is close but not identical.

## Verification checklist

A setup is complete only after real command output confirms:

```bash
docker info
docker run --rm hello-world
docker compose version
```

If any of these cannot be run because of permissions or environment restrictions, state the blocker and give the exact admin-side command sequence.

## References

- `references/docker-cli-without-daemon.md` — example diagnosis pattern for a host with Docker CLI installed but no reachable daemon/socket.