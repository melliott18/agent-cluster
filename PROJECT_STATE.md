# Agent Cluster project state

Updated October 15, 2026. The dedicated `agent-cluster-01` VM foundation is
deployed and tested under [homelab#48](https://github.com/melliott18/homelab/issues/48).
This repository still has no application, selected model, or deployed agent runtime.

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

The earlier brainstorming suggested Open WebUI, Ollama or llama.cpp, a Python
agent service potentially using LangGraph, and PostgreSQL. These remain
candidates; no application stack, model, or GPU assignment has been selected.
The initial VM allocation is implemented as described above.
Historical cloud-provider options in Homelab are optional broader context;
this project's required core is local.

## Shared inference direction — October 15

Owner decision: preserve the existing benchmark workload's direct GPU access
and plan a shared local inference service. Do not pass the GPU exclusively to
this VM. The VM remains the home for chat, agent tools and durable task state.

Proposed first stack: Docker Engine/Compose and Open WebUI in the existing
4 GiB VM; one Python/LangGraph worker with SQLite for durable tasks; one shared
Ollama endpoint running `qwen3.5:9b-q4_K_M`, initially 8K context, one loaded model
and one inference request at a time. Start with a bounded document-search/report
task and restricted project files. These software choices remain recommendations,
not accepted deployment or performance claims.

Proposed inference placement is a dedicated GPU-enabled LXD container, separate
from the benchmark workload. This needs an explicit scoped exception to the
older inference-in-a-VM direction, along with Homelab capacity and access design.
GPU sharing does not reserve VRAM or schedule arbitrary benchmark jobs. Use
cooperative benchmark/inference windows and unload the model before benchmark
runs; retain existing GPU access. Do not infer exclusivity from an idle sample.

The latest read-only Homelab inspection found an idle GPU and an existing Ollama
service with no models. Memory admission is still unresolved: retain the current
VM allocation and host reserve, and budget inference loading before deployment.
No software, resource allocation, driver, network or workload state was changed.
This planning update is local on `docs/shared-inference-plan` in both projects;
the deployed VM records remain published on main.

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
documentation workflow; runtime/model selection remains open.

Use [the integration guide](docs/homelab-integration.md) for ownership and
reading order. Keep dated outcomes here as implementation progresses and link
host changes to Homelab's records. No submodule, host change, or deployment
was performed during the October 15 context setup.
