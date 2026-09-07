# Security Model

## Security thesis

InfraSentinel assumes that incident descriptions, logs, retrieved web pages, tool results and model-generated text may contain misleading or adversarial instructions.

> **External content is data, never authority.**

## Threat model

The prototype explicitly considers:

- prompt injection inside incident text or logs;
- malicious instructions inside retrieved web pages;
- unsafe or malformed model tool calls;
- destructive action proposals;
- privilege escalation through broad target scope;
- missing or weak evidence provenance;
- accidental execution outside dry-run mode;
- tampering with the local audit trail;
- provider outages and partial failures.

## Defense in depth

### Input

The guardrails layer can inspect and constrain user/incident input before model processing. NVIDIA documents input rails as an explicit stage in the request pipeline. citeturn665148search1turn665148search2

### Retrieval

Tavily results are stored as explicit evidence objects with source URLs, excerpts, relevance and retrieval metadata. Retrieval content remains untrusted data.

### Tool boundary

NVIDIA's IORails tool-calling capability validates tool names and JSON-schema arguments and validates the linkage and structure of tool results. It fails closed on malformed tool traffic. The application still owns actual tool execution. citeturn665148search0

### Planning

The model is instructed to diagnose before acting, use evidence, prefer minimal reversible changes, and never follow instructions embedded in retrieved content.

### Authorization

`PolicyEngine` operates independently of the model. It rejects known destructive operations, excessive risk, missing evidence for mutations and broad production scope.

### Governance

`GovernanceEngine` distinguishes between `auto_approved`, `human_required` and `denied`. This prevents policy permission from being confused with execution permission.

### Execution

The public runtime is a simulator. It accepts dry-run operations only and never modifies a real cluster or database.

### Verification

Execution and verification are separate states. A successful tool invocation is not treated as proof that the desired infrastructure postcondition occurred.

### Audit

The audit stream is JSONL but now includes a SHA-256 hash chain linking each event to its predecessor. The verifier can detect modification or deletion/reordering of historical events.

This is **tamper-evident**, not an absolute guarantee of immutability: an attacker with write access to the complete audit store could rewrite the entire file and its chain. Production deployment should therefore replicate or anchor audit state in a controlled external system.

## Fail-closed behavior

The system should fail closed when:

- tool arguments cannot be parsed;
- a tool result cannot be structurally linked to its call;
- required evidence is missing;
- a policy check fails;
- risk exceeds the autonomous ceiling;
- a high-impact operation lacks human approval;
- the runtime is not operating in an allowed mode;
- verification cannot establish required postconditions.

## Production hardening

Before real infrastructure connectivity, add:

- workload identity and short-lived credentials;
- namespace/resource allowlists;
- server-side RBAC / IAM authorization;
- Kubernetes admission control;
- GitOps-only promotion for persistent changes;
- dual-control approval for high-impact operations;
- network egress restrictions;
- secrets and PII redaction;
- signed or externally anchored audit records;
- rollback verification;
- rate limits, action budgets and circuit breakers;
- independent monitoring of the agent itself.
