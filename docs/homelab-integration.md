# Homelab integration

Agent Cluster is an independent application project that uses Homelab
infrastructure. Keep the existing sibling checkout layout, matching Git Mirror:

```text
Projects/
  homelab/        # Infrastructure and operational evidence
  git-mirror/     # Mirroring and CI services
  agent-cluster/  # Local chatbot and autonomous agents
```

## Shared context

The shared [registry](../../homelab/docs/reference/projects.md) owns project
identities and entry points. Follow the
[workflow](../../homelab/docs/reference/project-workflow.md) for context lookup,
authoritative records, completion, commits and concurrent edits. These are the
canonical rules; this guide describes Agent Cluster's integration specifically.

Start in this project's [state](../PROJECT_STATE.md) and [agent guide](../AGENTS.md).
Read Homelab's [agent guide](../../homelab/AGENTS.md) and
[project state](../../homelab/PROJECT_STATE.md) before planning work that uses
the lab. For hardware and placement, continue with its
[inventory](../../homelab/docs/inventory/hosts.md),
[architecture](../../homelab/docs/architecture/overview.md), and decisions
[0007](../../homelab/docs/decisions/0007-ubuntu-vm-foundation.md) and
[0008](../../homelab/docs/decisions/0008-gpu-agent-control.md).

Existing [agent design](../../homelab/docs/architecture/agents.md) and
[workload platform](../../homelab/docs/architecture/workload-platform.md)
cover identity, task leases, isolation, shared artifacts, and recovery. Preserve
those requirements while choosing this project's implementation. Older proposals
include K3s and cloud providers; current Homelab records establish an existing
MicroK8s VM, and this project's core must run locally. A historical proposal
does not authorize migration or add a cloud dependency.

Local links assume the sibling layout. For another workstation, clone the private
[Homelab repository](https://github.com/melliott18/homelab) beside this one and
use the same paths. The
[Homelab integration entry](../../homelab/docs/architecture/agent-cluster.md)
provides the reciprocal reference. Some October 14 infrastructure records were
uncommitted in the Homelab checkout when reviewed on October 15; a fresh clone
may not contain them until that project's ongoing work is committed.

## Responsibilities

| Homelab | Agent Cluster |
| --- | --- |
| Host inventory, shared capacity and GPU assignment | Model selection, serving configuration and inference admission |
| VM provisioning, networks, access and lifecycle | Chat UI, coordinator, worker runtime and tools |
| Physical storage, NAS and backup destination | Application data layout, retention and restore procedure |
| Host monitoring, power and recovery | Task health, application metrics and result verification |

Git Mirror separately owns mirrors and CI runners. Consult its
[state](../../git-mirror/PROJECT_STATE.md) for future CI integration.

Record host outcomes in Homelab and application outcomes here, linking across
both when needed. Homelab GitHub issues own infrastructure task status; reference
them rather than creating duplicate status lists. Keep host identifiers, raw
evidence, and private access details in Homelab or ignored local storage.

Shared context consists of maintained project documents and explicit startup
reading. It does not merge or automatically synchronize conversation histories.
Each chat can remain focused while contributing concise decisions and outcomes
to the appropriate repository.

## When a submodule would help

Reciprocal links are sufficient during design. A submodule becomes useful when
Homelab deployment configuration needs to pin an exact Agent Cluster revision,
potentially under `services/agent-cluster`. Keep Homelab as the parent and retain
this repository's independent history; avoid circular submodules.

Adopting that layout would require deliberate revision updates and documentation
of deployment checkout paths. It would not provide shared chat memory. No
submodule or directory move is needed for the current context relationship.
