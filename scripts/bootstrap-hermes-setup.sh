#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "This repo contains a sanitized Hermes setup backup: $repo_dir"
echo "Copy config/config.example.yaml to your Hermes config path and fill secrets from config/env.example locally."
