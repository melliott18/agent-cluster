#!/usr/bin/env bash
# Owner-only local access through Homelab's pinned VM SSH helper.
set -euo pipefail
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
homelab=${HOMELAB_ROOT:-"$repo/../homelab"}
helper="$homelab/scripts/virtualization/agent-cluster-ssh.sh"
if [[ ! -f $helper && -z ${HOMELAB_ROOT:-} ]]; then
  homelab="$repo/../homelab-agent-cluster-vm"
  helper="$homelab/scripts/virtualization/agent-cluster-ssh.sh"
fi
[[ -f $helper ]] || { echo 'Set HOMELAB_ROOT to the authorized Homelab checkout with VM access configured.' >&2; exit 1; }
install -d -m 0700 "$repo/local/open-webui"
socket="$repo/local/open-webui/ssh-control"
case "${1:-start}" in
  start)
    if bash "$helper" -S "$socket" -O check 2>/dev/null; then exit 0; fi
    bash "$helper" -M -S "$socket" -f -N \
      -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
      -L 127.0.0.1:8088:127.0.0.1:3000
    echo 'Open WebUI: http://127.0.0.1:8088'
    ;;
  status) bash "$helper" -S "$socket" -O check ;;
  stop) bash "$helper" -S "$socket" -O exit ;;
  *) echo 'Usage: open-webui-tunnel.sh [start|status|stop]' >&2; exit 1 ;;
esac
