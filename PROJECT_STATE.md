# Agent Cluster project state

Updated October 15, 2026. Planning only; this repository has no application,
selected model, or deployed agent runtime.

## Owner requirements

- A private local environment on the existing Homelab, independent of cloud
  compute, paid model APIs, and subscriptions.
- Both conversational chatbot use and autonomous execution of assigned tasks.
- A focused project/repository and chat history, with shared Homelab context,
  following the Git Mirror project's organization.

## Shared foundation

[Homelab project state](../homelab/PROJECT_STATE.md) owns the current recorded
infrastructure facts. Its September 29 hardware baseline records a Ryzen 7
3700X, 32 GB installed RAM, RTX 3090, and 2 TB SSD in the GPU server. The Pi 5
is reserved for NAS under accepted decision 0008. Ubuntu Server hosts workload
VMs, with optional containers inside guests, under decision 0007.

The October 14 capacity assessment records roughly 30.28 GiB usable host RAM,
12 GiB of guest allocations, a container capped at 18.63 GiB, and another
uncapped container. Sampled available memory is not a guaranteed deployment
budget. Existing workloads and planned GitLab compete for the same capacity.
The detailed source is private, local uncommitted Homelab evidence at
`docs/logs/2026-10-14-gitlab-sizing.md`; it is not yet available in a fresh clone.
Use Homelab's committed [project state](../homelab/PROJECT_STATE.md) as the
portable baseline and recheck live capacity before allocation.

Agent control, worker, and inference guests remain planned. An October 13
inspection found an existing Ollama API in a retained workload, but successful
GPU inference and its availability for this project are unvalidated. NAS and
independent recovery are also unfinished. These are dated repository findings;
no live host inspection accompanied this project's setup.

## Architecture direction

Retain Homelab's accepted placement: agent controls and compute on the GPU
server, Pi for NAS. Build on its proposed separation of controller, workers,
and an inference API. Logical roles do not require allocating every proposed
VM immediately. The controller's live task state belongs on guest-local storage
and should remain accessible when NAS is unavailable.

The earlier brainstorming suggested Open WebUI, Ollama or llama.cpp, a Python
agent service potentially using LangGraph, and PostgreSQL. These remain
candidates; no stack, model, VM sizing, or GPU assignment has been selected.
Historical cloud-provider options in Homelab are optional broader context;
this project's required core is local.

## Next design decisions

1. Select one useful initial task alongside chat, such as local document search
   or a coding task that produces a tested diff.
2. Recheck host capacity and existing GPU ownership through Homelab before
   proposing allocations. Resolve shared workload budgets and inference placement.
3. Compare suitable local models on the chosen task, including tool execution,
   memory use, context length, and interactive latency.
4. Select a minimal runtime with durable jobs, bounded retries, cancellation,
   restart recovery, scoped tools, and verifiable task completion.
5. Define a bounded pilot and link application work to Homelab infrastructure
   issues. Existing Homelab issues retain their own status and evidence.

## Context handoff

October 15: the owner accepted the shared organization recorded in Homelab
[decision 0012](../homelab/docs/decisions/0012-linked-project-context.md).
All three projects now route through its
[registry](../homelab/docs/reference/projects.md) and
[workflow](../homelab/docs/reference/project-workflow.md). This changes the
documentation workflow; runtime/model selection remains open.

Use [the integration guide](docs/homelab-integration.md) for ownership and
reading order. Keep dated outcomes here as implementation progresses and link
host changes to Homelab's records. No submodule, host change, or deployment
was performed during the October 15 context setup.
