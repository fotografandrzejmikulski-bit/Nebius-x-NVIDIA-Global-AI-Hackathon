# InfraSentinel-Agentic — Grant & Hackathon Application

**Track:** Coding and Agentic Engineering  
**Bonus target:** Best Use of Tavily  
**Repository:** https://github.com/fotografandrzejmikulski-bit/Nebius-x-NVIDIA-Global-AI-Hackathon

## Executive Summary

InfraSentinel-Agentic is an evidence-first autonomous Site Reliability Engineering (SRE) system for diagnosing infrastructure incidents and executing only bounded, reversible, policy-compliant remediation.

Its defining principle is **separation of intelligence from authority**. NVIDIA Nemotron 3 Super, served through Nebius Token Factory, provides high-capacity reasoning. Tavily provides live, source-attributed technical evidence. NVIDIA NeMo Guardrails adds programmable safety controls around LLM interaction and tool use. A deterministic policy engine independently decides whether a proposed action is permitted. A sandbox simulator demonstrates the execution path without touching real infrastructure by default. An append-only JSONL audit trail preserves the decision chain.

The system therefore follows:

**observe → research → diagnose → propose → validate → authorize → execute → verify → audit**

The project is not designed as an unrestricted LLM shell. It is a prototype for **governable autonomy**: the model can reason broadly, but it earns operational authority only through explicit policy, evidence, scope and reversibility constraints.

## Problem

Infrastructure changes faster than static runbooks. Kubernetes APIs, cloud services, container images, deployment controllers and security policies evolve continuously. Operators need current technical knowledge, but autonomous execution creates a larger blast radius when an AI system is wrong, outdated, manipulated or over-scoped.

A syntactically valid command is not an authorization decision. A retrieved webpage is not an operator instruction. A model-generated tool call is not inherently safe.

InfraSentinel treats these distinctions as architectural requirements.

## Proposed Solution

1. Normalize the incident into typed state.
2. Retrieve current technical evidence with Tavily.
3. Ask NVIDIA Nemotron to synthesize a diagnosis and candidate remediation.
4. Represent each proposed operation as a typed action containing target scope, risk tier, evidence references, expected effect, rollback and dry-run state.
5. Evaluate the action through NeMo Guardrails and an independent deterministic policy engine.
6. Execute only policy-approved actions; the public prototype uses a safe simulator.
7. Verify the result and record the complete evidence-to-action chain.

## Technical Differentiation

### Evidence-Bound Autonomy Envelope

Each proposed action is evaluated on four dimensions:

- **Evidence:** which source supports the action?
- **Scope:** which resource boundary will be touched?
- **Risk:** what is the operational blast radius?
- **Reversibility:** how can the change be undone?

This converts autonomy from a binary privilege into a bounded capability granted action-by-action.

### Defense in Depth

Safety is deliberately distributed across layers:

**NeMo Guardrails** handles LLM-facing policy boundaries.  
**Deterministic PolicyEngine** handles authorization rules that must not depend on model judgment.  
**Typed action contracts** prevent free-form executor interfaces.  
**Sandbox runtime** keeps the public demonstration isolated.  
**Audit trail** makes every material transition reconstructable.

## Why NVIDIA Nemotron 3 Super

NVIDIA documents Nemotron 3 Super as a 120B-total / approximately 12B-active hybrid MoE model designed for reasoning and agentic workloads, with up to a 1M-token context length. Its Mamba/Transformer, LatentMoE and Multi-Token Prediction architecture is well aligned with long-running, tool-mediated workflows.

For SRE, this enables long incident histories, large log contexts and multi-step plans to remain available to the reasoning loop while avoiding dense activation of all model parameters on every forward pass.

## Why Nebius Token Factory

Nebius Token Factory provides an OpenAI-compatible inference interface for NVIDIA models. This lets the project keep the reasoning layer explicit and reproducible while avoiding the operational burden of independently maintaining a large GPU inference service.

Nebius is therefore not a marketing dependency in the architecture; it is the runtime inference plane used by the agent.

## Why Tavily

Tavily is a core epistemic dependency rather than a UI search box. When infrastructure behavior is version-sensitive or the agent lacks sufficient evidence, it performs a runtime search and preserves source URLs and excerpts as structured evidence.

The implementation uses advanced search, raw-content retrieval, domain restrictions, result limits and semantic chunking. This is consistent with Tavily's documented search capabilities and provides a defensible chain:

**incident → query → sources → evidence → diagnosis → proposed action**

The repository is consequently positioned for the Best Use of Tavily bonus, which requires a functional runtime Tavily API call.

## Security Model

Retrieved web content and tool outputs are treated as **untrusted data**. They cannot silently become executable instructions.

High-impact and destructive operations are denied in the public prototype. Broad production scope requires human-controlled change management. Non-read actions require evidence linkage. The default execution mode is simulated.

The production roadmap adds namespace-scoped identities, short-lived credentials, resource allowlists, GitOps approval, admission controls, egress restrictions, secret redaction, rollback verification and policy packs.

## Demonstration Scenario

The canonical demonstration is a Kubernetes `CrashLoopBackOff` associated with an RBAC regression in the monitoring namespace.

The incident also contains an intentionally destructive instruction to delete the database and cluster. InfraSentinel must:

1. identify the destructive intent;
2. block it;
3. preserve the legitimate diagnostic signal;
4. research current RBAC evidence;
5. identify the narrowest remediation;
6. produce a dry-run action;
7. validate it against policy;
8. execute the approved simulation;
9. show the evidence and rollback chain;
10. record the entire workflow in the audit trail.

This single scenario demonstrates both capability and restraint.

## Evaluation Plan

The evaluation suite should contain normal, ambiguous and adversarial incidents across Kubernetes RBAC, CrashLoopBackOff, configuration failures, image/dependency regressions, network/service-discovery problems and prompt-injection cases.

Primary metrics:

- diagnostic correctness;
- evidence relevance;
- evidence-linkage compliance;
- unsafe-action block rate;
- false-positive policy block rate;
- dry-run success rate;
- tool-call validity;
- latency to first useful remediation;
- audit completeness.

The most important measure is not how often the agent acts. It is whether the agent solves the incident while minimizing unjustified authority.

## Product and User Experience

The system is structured as an operator workflow with five views:

**Incident:** severity, service, environment and observed signals.  
**Diagnosis:** root-cause hypothesis, confidence and supporting evidence.  
**Remediation:** proposed operation, target, risk, expected effect and rollback.  
**Safety:** blocked actions, policy decisions and approval state.  
**Audit:** timestamped incident → evidence → policy → execution sequence.

The same state model supports the CLI demo and a future web operations console.

## Impact

The initial users are SRE teams, platform engineering organizations, DevOps groups, managed Kubernetes providers and organizations that require explainable automation in production environments.

The intended value is two-sided:

- reduce mean time to diagnose and operator toil;
- reduce risk from uncontrolled AI-initiated infrastructure changes.

The long-term product is an autonomous operations control plane that can connect to Kubernetes, observability systems, CI/CD, GitOps and incident-management systems while retaining one shared policy boundary.

## Hackathon Compliance

The official rules require a working project, a working demo/test build, a public open-source repository with the necessary code and instructions, English-language submission materials, track identification and feedback on the Nebius/NVIDIA technologies used. The rules specify four equally weighted judging criteria: Technological Implementation, Design, Potential Impact and Quality of the Idea. The submission deadline is **October 30, 2026 at 10:00 a.m. PDT**.

InfraSentinel targets the **Coding and Agentic Engineering** track and is architected around the required Nebius/NVIDIA stack. It also targets the Best Use of Tavily bonus through an actual runtime Tavily integration.

Final eligibility is always subject to the official rules and the evidence contained in the submitted working demo.

## Development Roadmap

### Phase 1 — Competition-grade prototype

Nebius/Nemotron inference, Tavily runtime research, NeMo Guardrails, typed action contracts, deterministic policy, simulator, audit trail, benchmark fixtures, automated tests and demonstration workflow.

### Phase 2 — Controlled production pilot

Kubernetes and observability adapters, namespace-scoped identities, GitOps changes, approval workflows, rollback verification and persistent incident memory.

### Phase 3 — Autonomous SRE platform

Policy packs, continuous evaluation, incident clustering, remediation ranking, multi-cluster orchestration and enterprise integrations.

### Phase 4 — Agent interoperability

A policy-governed MCP gateway so external tools can participate without bypassing the same authorization envelope.

## Funding Use

Indicative use of support:

| Area | Allocation |
|---|---:|
| Execution adapters and security boundaries | 35% |
| Benchmark and evaluation infrastructure | 25% |
| Observability, provenance and audit | 20% |
| Deployment automation and hosted demo | 10% |
| Documentation and open-source maintenance | 10% |

The budget is intentionally weighted toward validation, safety, reproducibility and production hardening rather than speculative model training.

## Closing Statement

InfraSentinel-Agentic addresses a central engineering problem in agentic AI: **how to make autonomous systems operationally useful without making model output equivalent to unrestricted authority**.

Nebius provides the inference plane. NVIDIA Nemotron provides the reasoning engine. Tavily provides current evidence. NeMo Guardrails provides programmable model-level controls. The deterministic policy layer and bounded executor turn these components into a system whose authority is explicit, testable and auditable.

The goal is not an AI that blindly runs commands.

The goal is an AI operations system that can **understand the incident, obtain current evidence, reason over it, propose the smallest safe intervention, respect policy, execute only within an authorized boundary, verify the outcome and leave a complete audit trail**.

That architecture provides a credible path from hackathon prototype to trustworthy autonomous infrastructure operations.
