# Agent Cluster project state

Updated October 15, 2026. The dedicated `agent-cluster-01` VM foundation is
deployed and tested under [homelab#48](https://github.com/melliott18/homelab/issues/48).
Open WebUI is now deployed under [agent-cluster#1](https://github.com/melliott18/agent-cluster/issues/1).
[Access/runbook](docs/runbooks/open-webui.md) · [Result](docs/logs/2026-10-15-open-webui.md).
The interface has no model connection yet; inference and the custom worker remain pending.

## Owner requirements

- A private local environment on the existing Homelab, independent of cloud
  compute, paid model APIs, and subscriptions.
- Both conversational chatbot use and autonomous execution of assigned tasks.
- A focused project/repository and chat history, with shared Homelab context,
  following the Git Mirror project's organization.

## Shared foundation

[Homelab project state](https://github.com/melliott18/homelab/blob/main/PROJECT_STATE.md) owns the current recorded
infrastructure facts. Its September 29 hardware baseline records a Ryzen 7
3700X, 32 GB installed RAM, RTX 3090, and 2 TB SSD in the GPU server. The Pi 5
is reserved for NAS under accepted decision 0008. Ubuntu Server hosts workload
VMs, with optional containers inside guests, under decision 0007.

Homelab provisioned the initial guest with 4 vCPUs, **4 GiB RAM** and a 100 GiB
disk. This supports OS setup and light development; the proposed 12 GiB model
allocation requires a new capacity decision. Autostart is disabled and a
VM-specific host memory guard is enabled. Key-only owner/maintenance access,
a non-sudo runtime account, guest reboot, disk persistence and managed save/resume
were verified. No model software or GPU passthrough was installed.

The October 15 live inspection found existing workloads competing for RAM and
GPU access already configured for a retained workload. Available memory samples
do not establish a sustained inference budget. GPU ownership and capacity remain
Homelab's responsibility; independent backup/recovery remains unfinished.

Detailed evidence and access instructions are maintained on Homelab's `main`:
[deployment result](https://github.com/melliott18/homelab/blob/main/docs/logs/2026-10-15-agent-cluster-vm.md)
and [VM runbook](https://github.com/melliott18/homelab/blob/main/docs/runbooks/agent-cluster-vm.md).
These private records require Homelab access. The VM changes and this handoff
are published on both projects' default branches. When an existing Homelab
checkout has unrelated work on another branch, read the committed `main` records
or use its isolated VM worktree; preserve that checkout's edits.

## Architecture direction

Retain Homelab's accepted placement: agent controls and compute on the GPU
server, Pi for NAS. Build on its proposed separation of controller, workers,
and an inference API. Logical roles do not require allocating every proposed
VM immediately. The controller's live task state belongs on guest-local storage
and should remain accessible when NAS is unavailable.

The owner accepted Open WebUI, shared Ollama/Qwen3.5 9B and a lightweight
Python/LangGraph/SQLite agent direction, with UI installation first. Open WebUI
v0.12.2-slim now runs in the existing 4 GiB VM with a persistent volume and
1.5 GiB container memory ceiling. Owner authentication, disabled signup,
loopback access and persistence after container replacement passed. Docker
Engine 29.9.1 and Compose 5.6.0 are installed. No model or custom agent worker
is running yet; inference loading and tool quality remain untested.

## Shared inference direction — October 15

Owner decision: preserve the existing benchmark workload's direct GPU access
and plan a shared local inference service. Do not pass the GPU exclusively to
this VM. The VM remains the home for chat, agent tools and durable task state.

Accepted first stack: Open WebUI in the existing 4 GiB VM; one Python/LangGraph
worker with SQLite for durable tasks; one shared Ollama endpoint targeting
`qwen3.5:9b-q4_K_M`, initially 8K context, one loaded model and one inference
request at a time. The first bounded document-search/report task remains a
proposed pilot. UI installation is complete; the other stages remain pending.

The owner accepted the shared service direction while preserving benchmark GPU
access. A dedicated GPU-enabled LXD inference container is a scoped exception
to the older inference-in-a-VM direction; agent tools/state stay in the VM.
GPU sharing does not reserve VRAM or schedule arbitrary benchmark jobs. Use
cooperative workload windows and unload the model before benchmark runs.

Homelab's initial budget is **8 GiB inference system RAM**, **10 GiB host reserve**
and **2 GiB margin**: require at least 20 GiB host MemAvailable before starting.
Stop inference first below 12 GiB available, ahead of the existing agent VM's
10 GiB save threshold. These proposed controls are not installed, and the model's
actual loading footprint must be measured. Current headroom is insufficient;
no existing guest/container was stopped or resized to manufacture capacity.

Homelab owns the detailed
[budget evidence](https://github.com/melliott18/homelab/blob/main/docs/logs/2026-10-15-agent-webui-budget.md)
and [placement decision](https://github.com/melliott18/homelab/blob/main/docs/decisions/0013-shared-gpu-inference.md).
These private records require Homelab access. The installation and budget records
are published on both projects' `main` branches, alongside this project's
[Compose definition](deploy/open-webui/compose.yaml),
[runbook](docs/runbooks/open-webui.md) and [result](docs/logs/2026-10-15-open-webui.md).
Preserve unrelated work in older checkouts; read committed `main` or use the
isolated Homelab worktree at `../homelab-agent-cluster-vm`.

References: [model package](https://ollama.com/library/qwen3.5:9b-q4_K_M),
[Ollama concurrency/local-only controls](https://docs.ollama.com/faq),
[Open WebUI setup](https://docs.openwebui.com/getting-started/quick-start/),
[LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence).

## Next design decisions

1. Select one useful initial task alongside chat, such as local document search
   or a coding task that produces a tested diff.
2. Resolve shared workload budgets and GPU ownership through Homelab before
   increasing the VM allocation or adding inference.
3. Compare suitable local models on the chosen task, including tool execution,
   memory use, context length, and interactive latency.
4. Select a minimal runtime with durable jobs, bounded retries, cancellation,
   restart recovery, scoped tools, and verifiable task completion.
5. Define a bounded pilot and link application work to Homelab infrastructure
   issues. Existing Homelab issues retain their own status and evidence.

## Context handoff

October 15: the owner accepted the shared organization recorded in Homelab
[decision 0012](https://github.com/melliott18/homelab/blob/main/docs/decisions/0012-linked-project-context.md).
All three projects now route through its
[registry](https://github.com/melliott18/homelab/blob/main/docs/reference/projects.md) and
[workflow](https://github.com/melliott18/homelab/blob/main/docs/reference/project-workflow.md). This changes the
documentation workflow. The later accepted application direction and current
deployment stage are recorded above.

Use [the integration guide](docs/homelab-integration.md) for ownership and
reading order. Keep dated outcomes here as implementation progresses and link
host changes to Homelab's records. No submodule, host change, or deployment
was performed during the October 15 context setup.
