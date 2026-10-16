# Agent Cluster project state

Updated October 15, 2026. The dedicated `agent-cluster-01` VM foundation is
deployed and tested under [homelab#48](https://github.com/melliott18/homelab/issues/48).
Open WebUI is now deployed under [agent-cluster#1](https://github.com/melliott18/agent-cluster/issues/1).
[Access/runbook](docs/runbooks/open-webui.md) · [Result](docs/logs/2026-10-15-open-webui.md).
Qwen3.5 9B now responds through Open WebUI, including streaming.
[Inference runbook](docs/runbooks/shared-inference.md) ·
[Verification](docs/logs/2026-10-15-shared-inference.md).
The custom autonomous worker remains pending.

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

Homelab provisioned the initial guest with 4 vCPUs, 4 GiB RAM and a 100 GiB
disk. For the shared inference window, its current/boot memory target is now
**2.5 GiB**, with the **4 GiB maximum** retained. The UI container retains its
1.5 GiB cap; adding a worker or increasing allocation requires a capacity check. Autostart is disabled and a
VM-specific host memory guard is enabled. Key-only owner/maintenance access,
a non-sudo runtime account, guest reboot, disk persistence and managed save/resume
were verified. Model serving runs in the separate shared LXD service; no GPU
passthrough is assigned to the UI VM.

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
v0.12.2-slim runs in the agent VM with a persistent volume and
1.5 GiB container memory ceiling. Owner authentication, disabled signup,
loopback access and persistence after container replacement passed. Docker
Engine 29.9.1 and Compose 5.6.0 are installed. Shared Ollama 0.40.5 now serves
Qwen3.5 9B; cold load, full GPU residency, long prompts and streamed UI replies
passed. The custom worker and autonomous tool quality remain untested.

## Shared inference direction — October 15

Owner decision: preserve the existing benchmark workload's direct GPU access
and plan a shared local inference service. Do not pass the GPU exclusively to
this VM. The VM remains the home for chat, agent tools and durable task state.

Accepted first stack: Open WebUI in the agent VM; one Python/LangGraph
worker with SQLite for durable tasks; one shared Ollama endpoint targeting
`qwen3.5:9b-q4_K_M`, initially 8K context, one loaded model and one inference
request at a time. The first bounded document-search/report task remains a
proposed pilot. UI and model serving are working; the worker remains pending.

The owner accepted the shared service direction while preserving benchmark GPU
access. A dedicated GPU-enabled LXD inference container is a scoped exception
to the older inference-in-a-VM direction; agent tools/state stay in the VM.
GPU sharing does not reserve VRAM or schedule arbitrary benchmark jobs. Use
cooperative workload windows and unload the model before benchmark runs.

The deployed inference container has an **8 GiB hard RAM cap**, **zero swap**,
one loaded model/request and a 60-second idle unload. The gateway enforces the
selected text model, 8K context and bounded output. A host guard requires
**20 GiB MemAvailable** and **12 GiB free VRAM** before starting, and stops only
inference below **12 GiB host available** or on competing GPU compute. It does
not automatically restart; GPU polling cannot prevent every allocation race.

The owner selected saving the desktop session and pausing idle CI for inference.
Those guests remain unavailable until resumed; new CI jobs wait. The smaller
2.5 GiB UI guest target provided the remaining admission headroom. Soren's GPU
access, other retained containers and Kubernetes remain intact. The long-prompt
trial caused cache reclaim at the inference cap but no OOM or inference swap.

Homelab owns the [current capacity result](https://github.com/melliott18/homelab/blob/main/docs/logs/2026-10-15-shared-inference.md)
and [window switching](https://github.com/melliott18/homelab/blob/main/docs/runbooks/shared-inference.md).
These private records require Homelab access. New inference code/results are
**local on `feature/shared-inference` in both projects**, not yet on main; use
`../homelab-agent-cluster-vm` for that handoff. The earlier UI foundation and
[placement decision](https://github.com/melliott18/homelab/blob/main/docs/decisions/0013-shared-gpu-inference.md)
are already published. Preserve unrelated work in the original checkouts.

References: [model package](https://ollama.com/library/qwen3.5:9b-q4_K_M),
[Ollama concurrency/local-only controls](https://docs.ollama.com/faq),
[Open WebUI setup](https://docs.openwebui.com/getting-started/quick-start/),
[LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence).

## Next design decisions

1. Select one useful initial task alongside chat, such as local document search
   or a coding task that produces a tested diff.
2. Reassess shared workload budgets through Homelab before adding workers or
   expecting desktop, CI and inference to remain continuously available together.
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
