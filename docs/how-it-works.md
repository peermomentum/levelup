# How this backup works

`scripts/backup-hermes-setup.py` reads the local Hermes home at `/opt/data`, writes sanitized files into this repository, and avoids runtime/secret-bearing files.

The scheduled job runs the script, commits any resulting changes, and pushes to GitHub.
