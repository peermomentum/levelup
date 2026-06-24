# Docker CLI present but daemon/socket missing

This reference captures a reusable diagnostic pattern for restricted Linux environments where `docker --version` succeeds but containers cannot run.

## Symptom

```text
Docker version 26.1.5+dfsg1, build ...
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
ls: cannot access '/var/run/docker.sock': No such file or directory
```

Additional signals:

```text
uid=10000(non-root-user) ...
sudo: command not found
systemctl: command not found
service: command not found
```

## Interpretation

This is not a complete Docker installation. It usually means:

- the Docker CLI package is installed;
- the engine/daemon is absent or not running;
- the rootful socket `/var/run/docker.sock` is absent; and
- the current user cannot install packages or start services.

## Good response pattern

1. State the distinction clearly: "Docker CLI exists, Docker engine/daemon is not available."
2. If root/sudo is unavailable, do not keep retrying privileged package installs.
3. Provide exact admin commands for the detected distro.
4. Offer managed-environment options such as mounting the host Docker socket, with a security caveat.
5. Mark the task incomplete unless `docker info` and `docker run hello-world` succeed.

## Example admin commands for Debian/Ubuntu

```bash
apt-get update
apt-get install -y docker.io docker-compose-plugin
systemctl enable --now docker
usermod -aG docker <user>
```

Then verify after a new login session:

```bash
docker info
docker run --rm hello-world
docker compose version
```

## Rootless note

Rootless Docker can be a fallback, but it still needs prerequisites such as `uidmap` / `newuidmap` and often `slirp4netns`, `fuse-overlayfs`, and `iptables`. If those are missing and the user lacks root/sudo, rootless install cannot complete from inside the restricted session; give prerequisite install commands rather than recording a negative rule.