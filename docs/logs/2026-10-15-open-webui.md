# October 15 — Open WebUI foundation

- **Task:** [agent-cluster#1](https://github.com/melliott18/agent-cluster/issues/1).
- **Authorization:** Owner accepted the initial setup, specifically Docker,
  Compose and Open WebUI first, followed by shared inference memory budgeting
  while preserving the existing GPU workload's access.
- **Time:** October 15, 2026, approximately 19:47–20:00 PDT.
- **Result:** Authenticated Open WebUI deployed and verified. Inference and the
  custom agent worker remain uninstalled; no model response is claimed.

## Applied configuration

[Compose](../../deploy/open-webui/compose.yaml) installs `v0.12.2-slim`, immutable
image digest `sha256:34db70a8e8f305dc996c4b459db0949b715400a489ca8a2d1a2a31ae5ddc67bb`.
This is the upstream stable release published October 14. The non-root container
has a persistent external volume, 1.5 GiB RAM/two-CPU limits, loopback-only
publishing, authenticated access, no public signup and no model providers.
Offline mode and disabled code execution avoid fetching optional ML/browser
execution dependencies for this initial interface.

Docker Engine 29.9.1, Compose 5.6.0 and their prerequisites were installed only
in the guest. Docker's hello-world check passed. No Docker group access was
granted to the future agent worker. The initial owner account was generated with
a strong random password; bootstrap secrets were removed from the VM runtime
environment after successful login. Credentials remain local, ignored and mode
0600; no credential values are included here.

## Verification

- `/health` returns true and Docker reports healthy; frontend HTML returns 200.
  Browser inspection rendered the email/password sign-in form without a signup link.
- Owner password login returns the admin role; public signup is disabled.
- Anonymous model listing returns 401. Authenticated model list is empty as
  expected before inference installation.
- Created a temporary chat; replaced the container after removing bootstrap
  credentials; authenticated again and verified identical owner identity and
  retained chat. Deleted only that test chat afterward.
- Docker reports UID 10001, 1,610,612,736-byte memory/swap ceiling and two CPUs;
  runtime environment file is empty/mode 0600. Idle usage sampled at 284.7 MiB.
  Guest had approximately 3 GiB available and no failed systemd units.
- Only guest loopback port 3000 is published; the hypervisor could not connect
  through the guest's network address. The owner's SSH tunnel serves local 8088.
- Existing host VM/container configurations, running states and shared networks
  matched the pre-change snapshot. Existing GPU access and driver were preserved.

The first start failed because Docker repopulated an empty volume's root
ownership. Added `nocopy`, restored its intended owner and verified non-root
startup. A proposed internal Docker network prevented published-port access;
replaced it with a normal bridge while retaining loopback publishing and disabled
providers. No preexisting application data existed or was deleted in either repair.

## Handoff and limitations

[Runbook](../runbooks/open-webui.md) contains access, reproduction and rollback.
Homelab owns guest package installation, current host evidence, and the memory
budget in `docs/logs/2026-10-15-agent-webui-budget.md` on its matching local
`feature/open-webui` branch. These new commits are not yet published; the earlier
VM foundation remains on main. Raw host data stays in private Homelab local
storage; public application credentials and optional upstream source inspection
copies stay in this repository's ignored `local/open-webui/`.

The owner's acceptance of shared inference permits a scoped LXD inference
exception to the prior VM-only placement direction; application state and tools
remain in the agent VM. Memory thresholds are a proposed initial admission
policy, not a benchmarked capacity guarantee. No existing workload was stopped,
no model downloaded, no GPU assignment changed, and no independent backup or
physical-host reboot test was performed.
