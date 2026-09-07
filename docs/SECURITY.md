# Security model

## Threat model

InfraSentinel assumes that incident descriptions, logs, retrieved web pages, tool results and model-generated text can all contain misleading or adversarial instructions.

The system therefore treats external content as **data, not authority**.

## Controls

### Input

NeMo Guardrails can apply jailbreak heuristics and input policy checks before model processing. NVIDIA documents these as input rails and also documents PII masking and related built-in controls.

### Retrieval

Tavily searches are constrained to selected authoritative domains for the demo. The evidence object stores provenance so a recommendation can be inspected instead of accepted as an anonymous model fact.

### Planning

The model is instructed to diagnose before action, use evidence, prefer minimal reversible changes, and never treat retrieved text as executable instruction.

### Authorization

`PolicyEngine` is deterministic and independent of the model. It rejects known destructive command patterns, high/critical autonomous risk, unsupported broad production scope, and non-read actions without evidence.

### Execution

The public prototype uses a simulator and keeps all actions in dry-run mode. No real cluster, database or cloud account is modified.

### Audit

Each incident, evidence collection phase, policy decision and action result is written to an append-only JSONL audit file with unique event IDs and UTC timestamps.

## Security boundary statement

NeMo Guardrails is a programmable LLM safety layer, not a complete infrastructure authorization system. The strongest architectural choice in this prototype is therefore defense in depth: LLM guardrails + typed action schemas + deterministic policy + least-privilege execution adapters + auditability.

## Production hardening

Before connecting a real cluster, the runtime adapter must add workload identity, short-lived credentials, namespace/resource allowlists, server-side authorization, admission controls, approval workflows for high-risk changes, network egress policy, secret redaction, and rollback verification.
