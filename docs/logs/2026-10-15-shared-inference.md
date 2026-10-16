# October 15 — Local model connected to Open WebUI

- **Authorization:** Owner requested memory reclamation and a connected local model
  while preserving the existing benchmark workload's GPU access; selected saving
  the desktop session and pausing idle CI during inference.
- **Result:** Qwen3.5 9B Q4_K_M responds through authenticated Open WebUI, including
  streamed replies. [Operating guide](../runbooks/shared-inference.md).
- **Time:** October 15, 2026, approximately 20:20–20:42 PDT; raw UTC timestamps
  and private host measurements are retained in Homelab.

## Applied

Dedicated unprivileged LXD inference container, Ollama 0.40.5, one local model,
8 GiB system-memory cap without swap, 8K context, one request/model, 60-second
model retention. Ollama binds container loopback; a separate non-root gateway
provides bearer authentication and bounded inference operations. The UI VM's
current/boot memory target is now 2.5 GiB, with its 4 GiB maximum retained.
Existing UI container cap, login/data volume and cloud restrictions remain.

Open WebUI's provider connection and default model were saved through its admin
API. Automatic title/tag/follow-up/autocomplete generation was disabled to avoid
competing requests. The Compose defaults match; the UI container was recreated
and its authenticated provider connection/default model survived.

## Verification and limits

- Ollama sees the RTX 3090 as its service user; logs report all 33 model layers
  offloaded. `/api/ps` reports full GPU residency and context length 8,192.
- Model manifest digest:
  `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`.
- First load reported about 46 seconds; initial warmup/setup and overlapping
  verification requests made first-response wall times longer. Subsequent
  cold-after-restart streaming reply completed in about 5.1 seconds.
- A 6,668-token prompt returned the requested `ACK` through Open WebUI in about
  5.0 seconds. A subsequent 128-token bounded response completed in 1.86 seconds,
  reporting about 86 output tokens/second. These are small pilot samples, not
  sustained throughput or quality guarantees; that 128-token test hit its output cap.
- Inference cgroup reclaimed cache at its 8 GiB ceiling during the longer test;
  no OOM, OOM kill or inference swap was observed. Homelab retains exact peaks
  and host reserve samples; its budget remains authoritative.
- Unauthenticated gateway requests return 401, authenticated model listing 200,
  model-management requests 403 and a different model 400. Local integration
  tests cover concurrent-request 429 and unavailable-backend 503 behavior.
- A controlled **synthetic** low-memory condition exercised the real stop action:
  only inference stopped and GPU memory fell to zero. Admission restart passed;
  a streamed reply passed after restart and UI container replacement.
- Soren's container/driver/device configuration was preserved, and its NVIDIA
  device query still passed. No real concurrent benchmark was launched. A host
  polling guard cannot guarantee protection from simultaneous GPU allocation races.

The autonomous worker, tool permissions, independent backup/recovery and host
reboot validation remain unfinished. Text chat is working; vision is deliberately
rejected by the pilot gateway.

## Handoff

Homelab owns capacity/window switching and its
[infrastructure record](https://github.com/melliott18/homelab/blob/main/docs/logs/2026-10-15-shared-inference.md).
Implementation, runbooks and results are published on both projects' `main`
branches. Private host addresses and raw measurements remain in Homelab;
credentials and API verification artifacts remain ignored under `local/inference/`.
