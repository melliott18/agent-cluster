# Shared local inference

The text chatbot uses `qwen3.5:9b-q4_K_M` through a private Ollama gateway.
Open WebUI selects it by default. [Dated verification](../logs/2026-10-15-shared-inference.md).
The custom autonomous worker and tool integrations are still future work.

## Use and availability

Start the existing [Open WebUI tunnel](open-webui.md#access) and open
<http://127.0.0.1:8088>. Use the existing owner login. The provider key is stored
in the private Open WebUI database, not in Git or browser-side direct connections.

The host currently runs an **inference window**: the management desktop's session
is saved and the idle CI guest is shut down. New CI jobs wait. Homelab owns
[window switching and recovery](https://github.com/melliott18/homelab/blob/main/docs/runbooks/shared-inference.md).
Until this feature is published, that new record is on local
`feature/shared-inference` in `../homelab-agent-cluster-vm`; main links become
available after both projects are merged.

The UI VM has a 2.5 GiB current/boot memory target with a retained 4 GiB maximum.
Its 1.5 GiB UI container cap is unchanged. Revisit capacity before adding workers,
embeddings or other services. The dedicated inference container has 8 GiB hard
system-memory and zero-swap limits; no dedicated GPU/VRAM partition is provided.

## Request policy

[Gateway source](../../deploy/inference/gateway.py) allows only authenticated
model listing/version/residency, model information, chat and text generation.
Model pull/delete/create, arbitrary models and vision inputs are denied. Local
container administrators perform model maintenance separately.

- One request at a time; a concurrent generation receives HTTP 429.
- One model, 8,192-token context, default 1,024 and maximum 2,048 output tokens.
- Text-only pilot, thinking off by default; no tools execute in this gateway.
- Model retention is fixed at 60 seconds after use, then VRAM is released.
- Model providers remain local; cloud connections and Ollama cloud features are
  disabled. Downloading images/packages/weights required Internet access.
- Automatic title/tag/follow-up/autocomplete generation is disabled so it does
  not compete with chat. Owner authentication and disabled signup remain.

The host guard stops the inference container below 12 GiB host available RAM,
on another GPU compute process, or when its observations fail. Starting requires
20 GiB available RAM, 12 GiB free VRAM and no competing GPU compute process.
It does not automatically restart after a stop. The UI will report unavailable;
ask the owner to inspect/start through Homelab's control. Stop inference before
planned benchmark work. Polling is a fallback, not protection against every
simultaneous GPU allocation race.

## Reproduce and connect

Homelab provisions the separate unprivileged LXD container, NVIDIA device access,
capacity guard and host lifecycle. Preserve its pinned image/GPU mapping and
accepted decision 0013. Do not install a new NVIDIA driver or move the device
exclusively into the UI VM.

Inside that newly admitted container, [install.sh](../../deploy/inference/install.sh)
installs the SHA-256-verified Ollama 0.40.5 archive and reviewed
[service](../../deploy/inference/ollama.service) and
[gateway unit](../../deploy/inference/inference-gateway.service). The private
bootstrap directory supplies a freshly generated token and allowed source IPs.
No existing installation may be overwritten using this fresh-install script.

Pull `qwen3.5:9b-q4_K_M` through container-local Ollama. The verified model digest
is `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`;
recheck a future tag against this identity before assuming it is unchanged.
Revalidate cold load, host headroom, GPU residency and long prompts after updates.

In Open WebUI's admin Connections settings, configure the private gateway URL
from Homelab, enable Ollama and use its bearer token. Keep direct browser/provider
connections disabled. The equivalent admin API is `POST /ollama/config/update`
with `ENABLE_OLLAMA_API`, `OLLAMA_BASE_URLS` and `OLLAMA_API_CONFIGS` (index `0`,
`auth_type: bearer`, `key`, local connection, selected model). Do not print the
response because it contains the provider key. These settings persist in the
application database and can supersede environment defaults.

## Recovery

Stopping inference preserves downloaded weights and container files. Restart
through Homelab's admission command, then verify `/api/tags`, `/api/ps` after a
request, and a response through Open WebUI. Retain the gateway key in a protected
password store or ignored mode-0600 file. A fresh checkout lacks that key.

To disconnect, disable the Ollama connection through the admin UI/API and stop
inference using Homelab's control. Preserve the UI data volume, model data and
saved desktop session. Restore desktop/CI availability as described by Homelab;
do not resume them and assume the same inference capacity remains available.
No independent application backup/restore or physical-host reboot was tested.

Sources: [Ollama Linux](https://docs.ollama.com/linux),
[local-only, context and concurrency settings](https://docs.ollama.com/faq),
[chat API](https://docs.ollama.com/api/chat),
[pinned Open WebUI connection implementation](https://github.com/open-webui/open-webui/blob/v0.12.2/backend/open_webui/routers/ollama.py).
