#!/usr/bin/env bash
# Run inside the newly admitted LXD container with reviewed bootstrap files.
set -euo pipefail
[[ $EUID -eq 0 && $(hostname) == agent-inference-01 ]] || exit 1
[[ ! -e /etc/systemd/system/ollama.service ]]
base=/root/agent-inference-bootstrap
archive="$base/ollama-linux-amd64-0.40.5.tar.zst"
printf '%s  %s\n' dc5eabc292f9949546c90a97c820f924b035e05243b0de13c7f366182562169c "$archive" | sha256sum -c -
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends ca-certificates curl zstd python3
# Official binary archive includes runtime libraries; no GPU driver installation.
tar --zstd -xf "$archive" -C /usr
useradd --system --user-group --home-dir /var/lib/ollama --create-home --shell /usr/sbin/nologin ollama
usermod -a -G video ollama
useradd --system --user-group --no-create-home --shell /usr/sbin/nologin inference-gateway
install -d -m 0700 -o ollama -g ollama /var/lib/ollama/models
install -d -m 0755 /opt/agent-inference
install -d -m 0750 -o root -g inference-gateway /etc/agent-inference
install -m 0644 "$base/gateway.py" /opt/agent-inference/gateway.py
install -m 0640 -o root -g inference-gateway "$base/token" /etc/agent-inference/token
install -m 0640 -o root -g inference-gateway "$base/gateway.env" /etc/agent-inference/gateway.env
install -m 0644 "$base/ollama.service" "$base/inference-gateway.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now ollama.service inference-gateway.service
nvidia-smi --query-gpu=name,driver_version --format=csv
curl --fail --silent --show-error --retry 5 --retry-connrefused --retry-delay 1 \
  http://127.0.0.1:11434/api/version
