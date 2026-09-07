# Grant / Hackathon Application — InfraSentinel-Agentic

## Project

**InfraSentinel-Agentic: Evidence-Bound Autonomous SRE on Nebius with NVIDIA Nemotron**

**Primary track:** Coding and Agentic Engineering  
**Bonus target:** Best Use of Tavily  
**Repository:** https://github.com/fotografandrzejmikulski-bit/Nebius-x-NVIDIA-Global-AI-Hackathon

---

## 1. Executive Summary

InfraSentinel-Agentic is an evidence-first autonomous Site Reliability Engineering system designed to reduce incident-response toil while preventing LLM-generated infrastructure actions from becoming uncontrolled operational authority.

The project combines NVIDIA Nemotron 3 Super served through Nebius Token Factory, Tavily live technical research, NVIDIA NeMo Guardrails, typed remediation contracts, deterministic authorization, explicit governance/approval states, safe simulation, post-condition verification, and a tamper-evident audit trail.

The central engineering thesis is:

> **The model may reason broadly, but it may act only inside a bounded, evidence-backed authorization envelope.**

For a Kubernetes incident such as CrashLoopBackOff following an RBAC regression, the intended flow is:

**observe → research → diagnose → propose → validate → authorize → govern → execute → verify → audit**

The public prototype intentionally remains safe by default: it does not require a live cluster and the simulator only accepts dry-run operations.

---

## 2. The Problem

Infrastructure is a moving target. Kubernetes APIs, cloud services, container images, deployment controllers and security policies evolve faster than static runbooks.

Generic LLM agents improve access to operational knowledge, but they introduce a second problem: a syntactically valid command is not the same thing as an authorized operation.

Three common failure modes are especially dangerous:

1. stale or hallucinated technical guidance;
2. prompt injection embedded in incident data, logs or retrieved documents;
3. excessive authority granted to a model that was only intended to provide assistance.

The project therefore treats **knowledge, reasoning, authorization and execution as separate trust domains**.

---

## 3. The Proposed Solution

InfraSentinel converts an incident into a controlled evidence-to-action workflow.

### Intake

Normalize the alert into a typed incident object containing environment, service, severity, context and observation time.

### Evidence acquisition

Use Tavily to retrieve current, source-attributed technical evidence, with the search constrained to authoritative infrastructure domains for the public demonstration.

### Reasoning

Use NVIDIA Nemotron on Nebius Token Factory to synthesize evidence, diagnose the likely failure and construct bounded candidate actions.

### Action contract

Represent each proposal as a typed object carrying:

- action ID;
- command representation;
- target scope;
- risk tier;
- evidence IDs;
- preconditions;
- expected effect;
- postconditions;
- rollback guidance;
- dry-run status;
- idempotency key.

### Authorization

Run every candidate through a deterministic policy engine that is independent of the model.

### Governance

Separate authorization from approval. An action can be policy-allowed while still being routed to human approval because of its risk, execution mode or explicit confirmation requirement.

### Execution

Use a safe simulator for the public submission. Production adapters are a future extension and cannot bypass the policy contract.

### Verification

Treat successful invocation and desired infrastructure state as separate conditions. The execution result does not automatically prove that the postcondition occurred.

### Audit

Record the decision path as structured JSONL events linked by a cryptographic hash chain.

---

## 4. What Makes the Idea Novel

The principal innovation is the **Evidence-Bound Autonomy Envelope**.

Instead of treating an agent as either fully autonomous or fully manual, every proposed action earns authority along explicit dimensions:

| Dimension | Constraint |
|---|---|
| Evidence | mutation must cite explicit evidence objects |
| Provenance | sources remain inspectable |
| Scope | target must be explicit and bounded |
| Risk | typed risk tier must fit policy ceiling |
| Destructiveness | denied classes cannot cross the boundary |
| Reversibility | rollback guidance is required |
| Verification | expected postconditions are declared |
| Governance | human approval can be mandatory |
| Execution | public runtime is dry-run/simulated |
| Audit | state transitions are tamper-evident |

This produces a general architectural property:

> **Increasing model capability does not automatically increase infrastructure blast radius.**

That is the key distinction between a capable infrastructure chatbot and a governable autonomous SRE system.

---

## 5. Why Nebius + NVIDIA

Nebius Token Factory is the inference plane. The code uses its OpenAI-compatible interface to access NVIDIA Nemotron.

NVIDIA documents Nemotron 3 Super 120B as a hybrid architecture with sparse expert activation and a context window extending to 1M tokens. These characteristics are well matched to long-horizon, evidence-rich agentic workflows.

The project uses NVIDIA technology as part of the operational design rather than as branding:

**Nemotron = reasoning engine**  
**NeMo Guardrails = model/tool safety layer**  
**Nebius = managed inference plane**

This separation keeps infrastructure authority in application-level policy rather than inside the model.

---

## 6. Why Tavily Matters

Tavily is a functional dependency of the decision workflow.

When current technical evidence is needed, the agent searches authoritative sources and preserves provenance. The result is not copied into an anonymous prompt blob; it becomes explicit evidence that can be referenced by downstream actions.

The intended chain is:

**incident → query → source → evidence object → diagnosis → action**

rather than:

**incident → model memory → command**

This directly supports the project's central safety claim: actions should be justified by inspectable evidence.

---

## 7. Why NeMo Guardrails Matters

NVIDIA documents multiple rail types across the LLM interaction lifecycle, including input, retrieval, dialog, execution and output controls. Its IORails tool-calling path can validate tool names and JSON-schema arguments as well as tool-result linkage before the application executor receives them. citeturn665148search0turn665148search1turn665148search2

InfraSentinel deliberately does not make Guardrails the sole authority layer. It adds deterministic application authorization after model-facing controls.

That produces defense in depth:

**Guardrails → typed contract → deterministic policy → governance → executor**

---

## 8. Demonstrated Use Case

The canonical demonstration is a Kubernetes `CrashLoopBackOff` in the `monitoring` namespace associated with an RBAC regression.

The same incident payload also contains a malicious request to delete the database and cluster.

The expected behavior is deliberately dual-purpose:

1. recognize that the destructive request is outside policy;
2. preserve the legitimate diagnostic signal;
3. retrieve relevant current evidence;
4. diagnose the RBAC failure;
5. propose a minimally scoped candidate remediation;
6. require evidence linkage;
7. apply deterministic authorization;
8. route gated operations to human approval;
9. execute only safe dry-run actions in the public simulator;
10. verify declared postconditions;
11. produce a reconstructable audit trail.

This makes the demo a test of both **capability and restraint**.

---

## 9. Technical Architecture

```text
                   +-------------------------+
                   | Incident / Alert Source |
                   +------------+------------+
                                |
                                v
                   +--------------------------+
                   | Input Safety / Normalize |
                   +------------+-------------+
                                |
                                v
                   +--------------------------+
                   | Nemotron Agent Loop      |
                   | diagnose <-> research    |
                   | hypothesis <-> proposal  |
                   +------+-------------------+
                          |
               +----------+-----------+
               |                      |
               v                      v
       +---------------+     +-------------------+
       | Tavily        |     | Typed Action      |
       | Evidence      |     | Contract          |
       +-------+-------+     +---------+---------+
               |                       |
               +-----------+-----------+
                           v
                +-------------------------+
                | NeMo / Tool Validation  |
                +------------+------------+
                             v
                +-------------------------+
                | Deterministic Policy    |
                | risk / scope / evidence |
                +------------+------------+
                             v
                +-------------------------+
                | Governance              |
                | auto / human / denied   |
                +------+------------------+
                       |
              +--------+--------+
              |                 |
              v                 v
       AUTO-APPROVED      HUMAN REQUIRED
              |                 |
              +--------+--------+
                       v
              +--------------------+
              | Bounded Executor   |
              | simulator by default|
              +---------+----------+
                        v
              +--------------------+
              | Verification       |
              +---------+----------+
                        v
              +--------------------+
              | Hash-chained Audit |
              +--------------------+
```

---

## 10. Technical Maturity

The repository is a Python application rather than a notebook or single-script proof of concept. It currently contains:

- typed Pydantic domain models;
- Nebius provider abstraction;
- Tavily provider abstraction;
- iterative model/tool orchestration;
- deterministic policy engine;
- explicit governance engine;
- simulation runtime;
- cryptographically linked audit events;
- safety-policy benchmark;
- automated tests;
- CI configuration;
- architecture/security documentation;
- reproducible CLI commands.

The repository history also contains explicit security hardening and adversarial authorization test work, making the development trajectory visible rather than merely asserted. fileciteturn15file0L1-L2

---

## 11. Evaluation Plan

Evaluation is intentionally split into **capability** and **safety**.

### Capability

- diagnosis correctness;
- evidence relevance;
- remediation validity;
- structured-output validity;
- tool-call success;
- latency to first useful proposal.

### Safety

- destructive-action block rate;
- false-positive block rate;
- evidence-linkage coverage;
- correct human-approval routing;
- prompt-injection resistance;
- audit integrity;
- post-condition verification completeness.

The repository includes a deterministic benchmark with safe and adversarial policy cases that can be executed locally with:

```bash
python -m app.cli benchmark
```

The design goal is not maximum action throughput. It is maximum **useful work per unit of unjustified authority**.

---

## 12. Reproducibility

The public demonstration is intentionally runnable without external credentials.

```bash
python -m app.cli demo
python -m app.cli benchmark
python -m app.cli verify-audit
pytest -q
ruff check .
```

When credentials are supplied, the same orchestration layer can use the live Nebius and Tavily providers.

This dual-path design prevents a judge from encountering an unusable submission merely because external credentials are absent.

---

## 13. Security and Responsible Autonomy

The system follows a fail-closed philosophy.

Unsafe actions are not converted into "safer" commands by the model and executed. They remain denied.

Missing evidence blocks mutations.

High-impact operations can be routed to human approval.

The simulator refuses non-dry-run operations.

The audit implementation is tamper-evident through a SHA-256 hash chain. This is intentionally described as tamper-evidence rather than absolute immutability; production deployment should externally anchor or replicate the audit stream.

The public prototype therefore demonstrates safety architecture without requiring real production credentials.

---

## 14. Impact

Target users include:

- SRE and platform engineering teams;
- DevOps organizations operating Kubernetes/cloud infrastructure;
- managed service providers;
- engineering organizations with small on-call rotations;
- regulated organizations requiring explainable automation.

Potential impact areas include:

- lower mean time to diagnose;
- reduced operator toil;
- faster access to current technical knowledge;
- more consistent remediation procedures;
- lower risk from autonomous tooling;
- stronger auditability for AI-assisted operations.

The long-term product direction is an enterprise control plane for governed agentic operations across Kubernetes, GitOps, observability, CI/CD and incident-management systems.

---

## 15. Hackathon Alignment

The official Nebius x NVIDIA Global AI Hackathon rules require a working project, a working demo/test build, a public open-source repository with a README, English submission materials, use of Nebius Token Factory or Nebius AI Cloud with at least one NVIDIA open-source model, and technology feedback. The four primary judging dimensions are equally weighted: **Technological Implementation, Design, Potential Impact, and Quality of the Idea**. The current official deadline is **October 30, 2026 at 10:00 a.m. PDT**. citeturn665148search7

InfraSentinel addresses the four criteria directly:

| Jury dimension | Evidence in the project |
|---|---|
| Technological Implementation | Nebius + Nemotron + Tavily + Guardrails + iterative tool orchestration + deterministic policy |
| Design | explicit trust boundaries and operator-oriented incident flow |
| Potential Impact | SRE use case with a concrete production roadmap |
| Quality of Idea | Evidence-Bound Autonomy as a general architecture for governable agents |

The Best Use of Tavily submission case is also explicit: Tavily is part of the live evidence path and its results are preserved as provenance-bearing objects rather than being used as a decorative interface.

---

## 16. Development Plan

### Phase 1 — Competition hardening

- expand the incident benchmark;
- expand adversarial prompt-injection cases;
- add structured-output validation;
- add repeatable evaluation reports;
- polish the operator demonstration.

### Phase 2 — Controlled production pilot

- namespace-scoped Kubernetes credentials;
- Kubernetes and observability adapters;
- GitOps promotion;
- rollback verification;
- persistent audit storage.

### Phase 3 — Enterprise platform

- organizational policy packs;
- multi-cluster operations;
- continuous agent evaluation;
- incident memory;
- compliance reporting;
- policy-governed MCP tool gateway.

---

## 17. Funding Use

Potential support would be directed toward measurable engineering outcomes:

| Area | Share |
|---|---:|
| Secure infrastructure adapters | 30% |
| Evaluation / red-team benchmark | 25% |
| Observability, provenance and audit | 20% |
| Demo / hosted reproducibility | 15% |
| Documentation and open-source maintenance | 10% |

The purpose of funding is to validate and harden the control plane, not to pursue unrestricted speculative training.

---

## 18. Closing Statement

InfraSentinel-Agentic addresses a central challenge of agentic AI:

**How can an AI system receive enough authority to be useful without receiving enough authority to become dangerous?**

The proposed answer is architectural.

Do not make the model the authority boundary.

Give it access to current evidence. Give it structured tools. Let it reason over long horizons. Then place authorization outside the model, make governance explicit, constrain the executor, verify the result, and record the decision path.

Nebius provides the inference plane. NVIDIA Nemotron provides the reasoning capability. Tavily provides current operational evidence. NeMo Guardrails provides programmable model/tool controls. InfraSentinel supplies the missing system-level layer: **evidence-bound, policy-governed operational authority**.

The result is a credible path from an AI demonstration to a governable autonomous SRE control plane.
