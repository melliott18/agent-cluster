# Open WebUI foundation

Deployed on `agent-cluster-01` under
[agent-cluster#1](https://github.com/melliott18/agent-cluster/issues/1).
[Verification record](../logs/2026-10-15-open-webui.md).
This authenticated interface now answers through local Qwen3.5 9B inference.
See [shared inference](shared-inference.md) for limits and availability. The custom
autonomous worker remains pending.

## Access

From this repository on the owner's Mac, with the existing Homelab SSH access:

```bash
bash scripts/open-webui-tunnel.sh start
```

Open <http://127.0.0.1:8088>. The login name is `owner@agent-cluster.local`
(a local identifier; no mailbox or email service is required). The generated
initial password is stored in ignored `local/open-webui/admin-credentials.txt`,
mode 0600. It is not present in Git or the deployed runtime environment.
Change it through the account settings when desired. Do not print it in logs.

The helper uses Homelab's pinned SSH path; `HOMELAB_ROOT` can select an authorized
checkout. It checks the usual sibling Homelab checkout and then the isolated
`../homelab-agent-cluster-vm` worktree. A fresh checkout needs keys and pinned VM
access configured through the private Homelab VM runbook. A background tunnel
started inside a tool-managed shell may end when that shell is cleaned up;
run the command in a normal terminal for a persistent local session.

```bash
bash scripts/open-webui-tunnel.sh status
bash scripts/open-webui-tunnel.sh stop
```

Only one listener may own local port 8088. A separately running foreground
tunnel will not have the helper's control socket; close that session before
starting the background helper. Tailscale access to the hypervisor is required.
No public hostname, new host listener, or public firewall rule was added.

## Service and storage

The reviewed [Compose definition](../../deploy/open-webui/compose.yaml) pins
Open WebUI `v0.12.2-slim` and its image digest. On the VM it is installed at
`/opt/agent-cluster/open-webui/compose.yaml`, with an empty mode-0600 `runtime.env`.
Docker Engine 29.9.1 and Compose plugin 5.6.0 were installed from Docker's signed
Ubuntu repository. Operations require a guest administrator:

```bash
sudo sh -c 'cd /opt/agent-cluster/open-webui && docker compose ps'
sudo sh -c 'cd /opt/agent-cluster/open-webui && docker compose logs --tail 50'
sudo sh -c 'cd /opt/agent-cluster/open-webui && docker compose up -d'
sudo docker stats --no-stream agent-cluster-open-webui-1
```

- Only guest loopback `127.0.0.1:3000` is published; the tunnel provides Mac access.
- Container UID 10001, group 0; no Linux capabilities or privilege escalation.
  No Docker socket or hypervisor credential is mounted. The guest `agent` account
  remains outside the Docker group and has no sudo rights.
- Limit: 1.5 GiB memory, no additional swap, two CPU equivalents, 512 processes;
  one application worker. The guest now targets 2.5 GiB (4 GiB maximum retained).
  Reassess capacity before adding other services.
- External named volume `agent-cluster-webui-data` holds SQLite, uploaded data,
  and the generated signing key. `nocopy` preserves its initialized ownership.
  Compose `down` does not remove this external volume.
- `restart: unless-stopped` plus enabled Docker provides service startup inside
  the guest. VM autostart remains off under Homelab policy.
- Authentication is enabled and signup disabled. Shared local Ollama is enabled; direct provider connections,
  cloud APIs, web search, community sharing and code execution remain disabled. Offline mode suppresses model/update downloads. The normal Docker
  bridge still permits outbound networking; this is not an air gap.

## Reproduction

For a fresh authorized guest, install Docker with Homelab's reviewed
`scripts/virtualization/install-agent-docker.sh`. Copy the tracked Compose file
into a root-only `/opt/agent-cluster/open-webui` directory. Pull its exact pinned
image, create the external data volume, and initialize that volume's root to
UID 10001 / GID 0 with a one-shot container using the same image and `chown`.
Keep `volume.nocopy: true` so Docker does not reset empty-volume ownership.

Create root-only `runtime.env` containing `WEBUI_ADMIN_EMAIL`,
`WEBUI_ADMIN_PASSWORD` (a newly generated unique secret), and `WEBUI_ADMIN_NAME`.
Keep the owner's initial credential in a private password store or ignored
mode-0600 file. Run `docker compose config --quiet` (plain `config` can print
secrets) and `docker compose up -d`. After authenticating successfully, empty
`runtime.env` and force-recreate the container. Confirm login and stored data
still work. The account hash and signing key persist in the data volume.
Do not overwrite an existing installation or volume as a fresh bootstrap.

## Shared inference connection

Local Ollama is connected through the authenticated bounded gateway described in
[shared inference](shared-inference.md). The default is Qwen3.5 9B Q4_K_M; the
private URL/token and selected model persist in the database. Settings persisted
there can supersede Compose defaults. Do not point the UI at Soren's benchmark
container. Embeddings/voice and autonomous tools remain unconfigured.

## Recovery and rollback

Stop this application with `docker compose stop`, or remove only its container
and network with `docker compose down`. Preserve the external volume and signing
key. Do not run `docker volume rm`, broad Docker prune, or overwrite the database.
For an application-consistent backup, stop the service, archive the data volume
and deployment configuration into a root-only destination, then restart and
verify health. Store a protected copy off this physical disk before treating it
as independent recovery. No independent backup/restore has been validated.

To roll back a future image upgrade, retain a pre-upgrade data backup because
schema migrations may prevent an older image from reading the new database.
Container replacement with the current image was tested; guest/host reboot and
an independent restore were not performed during this task.

Sources: [Docker Ubuntu installation](https://docs.docker.com/engine/install/ubuntu/),
[Open WebUI release](https://github.com/open-webui/open-webui/releases/tag/v0.12.2),
[setup](https://docs.openwebui.com/getting-started/quick-start/),
[configuration](https://docs.openwebui.com/reference/env-configuration/).
