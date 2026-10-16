# Agent Cluster guide

## Startup context

Read `../homelab/docs/reference/projects.md` and
`../homelab/docs/reference/project-workflow.md` at the start of linked-project
work. Use the registry to resolve project references and follow its pointers
to authoritative records. After material changes, update the owning record,
link affected projects, qualify issue references, and commit only reviewed task
changes. Preserve concurrent edits and identify any local-only dependencies.

Read `PROJECT_STATE.md` and `docs/homelab-integration.md` before planning or
implementation. Then read `../homelab/AGENTS.md` and
`../homelab/PROJECT_STATE.md` for the shared infrastructure baseline. For sizing
or placement, also read its `docs/inventory/hosts.md`,
`docs/architecture/overview.md`, and accepted decisions 0007 and 0008.

Homelab's older `docs/architecture/agents.md` and
`docs/architecture/workload-platform.md` supply design context. Their proposed
software, illustrative budgets, and historical observations are not deployed
state. Prefer newer dated results and accepted decisions when they differ.

If the sibling checkout is unavailable, use an authorized checkout of
https://github.com/melliott18/homelab or report the missing dependency. Do not
invent current host state or assume private source links are publicly readable.

## Ownership and evidence

- Homelab owns host inventory, VM lifecycle, network/storage boundaries, shared
  capacity, power policy, and independent recovery. Follow its operational
  instructions before inspecting or changing servers. The local Mac is a client.
- Agent Cluster owns chatbot and agent software, model serving configuration,
  durable tasks, tool integrations, application data, and application recovery.
- Git Mirror owns GitLab, mirroring, runner configuration, and CI migration.
  Read its project state before proposing integration with those services.
- Keep infrastructure facts and operational issue status authoritative in
  Homelab. Link to them here; do not maintain a competing host inventory/backlog.
- Keep owner requirements, proposals, dated observations, and verified deployment
  separate. An available model API does not establish successful GPU inference.
- Persist decisions and concise handoffs in project documents. Repository links
  do not synchronize raw chat histories. Do not message or change another chat
  merely because its project is referenced here.
- Preserve unrelated local changes in all repositories. Keep reciprocal links
  current when responsibility changes; do not move checkouts or add submodules
  incidentally.

## Local operation and data

The core system must run locally without cloud inference or subscription
dependencies. Model/runtime/UI choices remain open. Internet tools, if selected,
are separate from where inference and private task data run.

Keep credentials, raw transcripts, private host addresses, private repository
identities, and raw host output out of tracked files here. This repository is
public, verified October 15, 2026; use public-safe summaries. Detailed host evidence belongs
in private Homelab records; raw project evidence may use ignored `local/`.

## Git conventions

Use `<type>/<short-description>`, with a lowercase, hyphenated description and
type `feature`, `fix`, `docs`, `refactor`, `test`, or `chore`. Do not use `codex/`
or other tool/agent names as prefixes. Honor an exact user-requested branch name.
