# Grant Application — InfraSentinel-Agentic

## Project Title

**InfraSentinel-Agentic: Evidence-First Autonomous SRE on Nebius with NVIDIA Nemotron**

## Executive Summary

InfraSentinel-Agentic is a safety-first autonomous Site Reliability Engineering system designed to shorten incident response without turning infrastructure access into an uncontrolled LLM side effect.

The system combines NVIDIA Nemotron served through Nebius Token Factory, Tavily live technical research, NVIDIA NeMo Guardrails, typed remediation contracts, deterministic risk policy, a dry-run execution boundary, and an auditable event trail.

Its central innovation is architectural rather than cosmetic: **the model is allowed to reason broadly, but it is authorized to act narrowly**.

For a production incident such as a Kubernetes CrashLoopBackOff following an RBAC regression, the system can collect current evidence, formulate a diagnosis, propose a minimal reversible remediation, validate the action against deterministic policy, execute only within the approved envelope, and record the entire chain for later review.

The public hackathon prototype intentionally uses a safe simulator. No real production infrastructure is modified. The same policy and action contracts are designed to support future Kubernetes, GitOps, observability and cloud adapters.

## Problem

Modern infrastructure failures move faster than static runbooks. Kubernetes, cloud APIs, container runtimes, deployment controllers and security policies evolve continuously. An incident responder therefore needs two things at the same time: current technical knowledge and safe operational authority.

Generic LLM agents address the first problem but can worsen the second. A plausible command is not an authorization decision. A retrieved web page is not an instruction from the operator. A model-generated tool call is not automatically safe because it is syntactically valid.

InfraSentinel treats these boundaries as first-class engineering requirements.

## Proposed Solution

InfraSentinel turns incident response into a controlled evidence-to-action pipeline:

1. Normalize and classify an incident.
2. Retrieve fresh, source-attributed technical evidence with Tavily.
3. Ask NVIDIA Nemotron to diagnose the fault and construct a remediation hypothesis.
4. Convert proposed operations into typed actions with explicit scope, risk, evidence and rollback metadata.
5. Pass the action through NeMo Guardrails and a deterministic policy engine.
6. Execute only the actions permitted by the policy boundary; the public prototype remains dry-run only.
7. Record evidence, policy decisions and execution results in an audit trail.

## Why Nebius + NVIDIA

Nebius Token Factory provides an OpenAI-compatible inference path for NVIDIA Nemotron models. NVIDIA positions Nemotron 3 Super 120B as a hybrid MoE model optimized for efficient multi-agent AI and complex reasoning. This makes it a natural reasoning layer for a long-horizon, tool-mediated operational workflow.

The engineering benefit is that the project can concentrate on agentic control logic rather than maintaining a GPU inference stack. The hackathon itself requires projects to run on Nebius Token Factory or Nebius AI Cloud and use at least one NVIDIA open-source model.

## Why Tavily

Tavily is not included as a decorative search box. It is a decision dependency.

When the agent encounters version-sensitive infrastructure behavior, it searches authoritative technical sources and preserves provenance in the evidence model. The current Tavily Python SDK supports advanced search, domain inclusion, raw content, result limits and chunk controls. The prototype uses these capabilities to reduce irrelevant context and keep evidence tied to explicit URLs.

This creates a defensible chain:

**incident -> query -> sources -> evidence -> diagnosis -> proposed action**

rather than:

**incident -> model memory -> command**

## Why NVIDIA NeMo Guardrails

The security design uses defense in depth. NVIDIA documents input, retrieval, dialog, execution and output rails as distinct control points; execution rails govern custom actions and tools, and the IORails tool-calling path can validate OpenAI-compatible tool traffic before it reaches the application executor.

InfraSentinel goes one step further by retaining a deterministic application policy outside the LLM. This matters because semantic safety and infrastructure authorization are related but not identical problems.

## Innovation

The key innovation is an **Evidence-Bound Autonomy Envelope**.

An AI agent does not receive a binary "autonomous / not autonomous" setting. Instead, each proposed operation is evaluated across four dimensions:

- Evidence: what source supports the action?
- Scope: what resources will it touch?
- Risk: what is the blast radius?
- Reversibility: how can the change be undone?

The agent earns operational authority one bounded action at a time.

This creates a general pattern for secure agentic infrastructure: **reasoning can be open-ended while authority remains constrained**.

## Technical Architecture

### Cognitive layer

NVIDIA Nemotron on Nebius Token Factory provides reasoning, incident decomposition and plan synthesis.

### Epistemic layer

Tavily provides live evidence retrieval and source provenance.

### Safety layer

NVIDIA NeMo Guardrails provides LLM-facing input/output and tool-boundary controls.

### Authorization layer

A deterministic PolicyEngine independently validates risk tier, command patterns, evidence linkage and target scope.

### Execution layer

The public submission includes a deterministic simulator. A production adapter can later target Kubernetes/GitOps APIs while preserving the same action contract.

### Observability layer

An append-only JSONL audit trail records incident receipt, evidence collection, policy evaluation and execution outcomes.

## Demonstrated Prototype

The included demonstration scenario is a Kubernetes RBAC regression causing CrashLoopBackOff. The agent researches the problem, produces a diagnosis, proposes read-only validation and a least-privilege RBAC dry-run, and blocks destructive commands such as cluster deletion.

A second adversarial scenario places a destructive instruction inside log content. The system is expected to treat that string as untrusted evidence rather than executable authority.

## Impact

The intended users are:

- SRE and platform engineering teams,
- DevOps organizations operating Kubernetes and cloud infrastructure,
- managed service providers,
- engineering teams with small on-call rotations,
- organizations that need explainable automation rather than opaque autonomous behavior.

The immediate impact target is reduced mean time to diagnose and reduced operator toil. The safety target is more important: automation should reduce time-to-recovery without increasing the probability of catastrophic operator-equivalent mistakes.

## Evaluation Plan

The prototype should be evaluated using an incident benchmark containing normal, ambiguous and adversarial cases.

Primary metrics:

- diagnosis accuracy,
- evidence relevance,
- percentage of proposed actions linked to evidence,
- unsafe-action block rate,
- false-positive policy block rate,
- dry-run success rate,
- latency to first useful remediation proposal,
- audit completeness.

A successful system is not the one that executes the most actions. It is the one that solves the incident while minimizing unjustified authority.

## Security and Responsible Autonomy

The prototype defaults to safe simulation. No live cluster is required to evaluate it.

Before production deployment, the runtime adapter should add workload identity, resource allowlists, admission control, short-lived credentials, human approval for high-risk changes, secret redaction, network egress controls and rollback verification.

The architecture explicitly rejects the idea that an LLM alone can be trusted to authorize infrastructure changes.

## Hackathon Compliance

The project targets the **Coding and Agentic Engineering Track**. The official rules require a working application running on Nebius Token Factory or Nebius AI Cloud, at least one NVIDIA open-source model, a public open-source code repository, a README and a public demonstration video shorter than three minutes. The official deadline is October 30, 2026 at 10:00 a.m. PDT.

The submission is also eligible in principle for the Best Use of Tavily bonus because Tavily is used as a functional runtime component rather than only mentioned in documentation. Final prize eligibility remains subject to the official rules and actual submission evidence.

## Project Maturity

This repository is intentionally organized as a real software project rather than a notebook or single proof-of-concept script. It includes:

- typed domain models,
- provider adapters,
- policy enforcement,
- safe runtime simulation,
- audit logging,
- configuration management,
- automated tests,
- security documentation,
- architecture documentation,
- reproducible run instructions.

## Future Development

With grant support, the project can evolve from a competition prototype into an open agentic SRE control plane:

**Phase 1 — Robustness:** richer incident benchmark, policy packs, structured output validation and evaluation harness.

**Phase 2 — Real infrastructure:** Kubernetes and GitOps adapters with namespace-scoped credentials and rollback verification.

**Phase 3 — Organization scale:** integrations with Prometheus, Loki, OpenTelemetry, CI/CD and incident-management systems.

**Phase 4 — Agent interoperability:** policy-governed MCP gateways so third-party tools can participate without bypassing the same authorization envelope.

## Funding Use

Potential grant funding would be allocated to engineering, evaluation and infrastructure hardening rather than speculative model training:

- 35% — production-grade execution adapters and security boundaries,
- 25% — incident benchmark and evaluation infrastructure,
- 20% — observability, provenance and audit features,
- 10% — deployment automation and hosted demonstration environment,
- 10% — documentation, open-source maintenance and developer onboarding.

## Closing Statement

InfraSentinel-Agentic proposes a practical answer to one of the central questions of agentic AI: **How do we give an AI system enough authority to be useful without giving it enough authority to become dangerous?**

The answer is not to remove autonomy. It is to engineer autonomy as a bounded capability.

Nebius supplies scalable inference infrastructure. NVIDIA Nemotron supplies the reasoning engine. Tavily supplies current evidence. NeMo Guardrails supplies programmable model-level controls. The project's deterministic policy and execution boundary convert these capabilities into an operational system whose authority is explicit, reviewable and testable.

That is the foundation for an SRE agent that can move from demo to production without pretending that intelligence and authorization are the same thing.
