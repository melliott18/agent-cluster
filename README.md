# Local AI Agent Cluster

A private, locally hosted chatbot and autonomous task system for the Homelab.
The core environment must work without paid model APIs, subscriptions, or cloud
compute. Status: authenticated Open WebUI is deployed on the agent VM; shared
inference and the custom agent worker are the next stages.
[Open WebUI access and operations](docs/runbooks/open-webui.md).

## Start here

- [Shared registry](https://github.com/melliott18/homelab/blob/main/docs/reference/projects.md) and
  [workflow](https://github.com/melliott18/homelab/blob/main/docs/reference/project-workflow.md): project ownership,
  context lookup and handoffs (private Homelab checkout required).
- [Project state](PROJECT_STATE.md): requirements, constraints, and next decisions.
- [Homelab integration](docs/homelab-integration.md): shared context and ownership.
- [Agent guide](AGENTS.md): startup reading and maintenance rules.
- [Decisions](docs/decisions/README.md) and [results](docs/logs/README.md).

## Related projects

[Homelab](https://github.com/melliott18/homelab), normally checked out at
`../homelab`, owns the hosts, VMs, networking, physical storage, capacity, and
independent recovery. Its private project state and inventory are authoritative
for infrastructure. This project owns the chatbot, agent runtime, model serving
configuration, task lifecycle, tools, project memory, and application recovery.

[Git Mirror](https://github.com/melliott18/git-mirror), normally at
`../git-mirror`, owns mirroring and CI services. Agent builds may eventually use
those services; this project does not provision competing runners or mirror systems.

Keep these as independent sibling repositories with reciprocal documentation.
A future Homelab deployment may pin this repository as a submodule when an exact
service revision is useful. A submodule is not required to share project context.
