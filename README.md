# InfraSentinel-Agentic

**Evidence-first autonomous SRE for safe, bounded remediation.**

InfraSentinel-Agentic is a competition-grade prototype for the **Nebius x NVIDIA Global AI Hackathon 2026**, targeting the **Coding and Agentic Engineering** track and the **Best Use of Tavily** bonus.

> **The agent may reason freely, but it may act only inside a bounded, evidence-backed policy envelope.**

## The thesis

Infrastructure AI should not be granted authority merely because a model can generate a valid command.

InfraSentinel separates four concerns:

- **Reasoning** — NVIDIA Nemotron on Nebius.
- **Evidence** — Tavily live technical research with provenance.
- **Authorization** — deterministic policy and governance outside the model.
- **Execution** — explicitly bounded runtime, simulated by default.

That produces:

```text
incident
  -> input safety
  -> evidence acquisition
  -> iterative reasoning
  -> typed action proposal
  -> guardrails / tool validation
  -> deterministic authorization
  -> governance / approval
  -> bounded execution
  -> post-condition verification
  -> tamper-evident audit
```

## Why this is different

A conventional agent often collapses planning and authority:

```text
LLM -> tool -> infrastructure
```

InfraSentinel deliberately inserts independent trust boundaries:

```text
LLM -> evidence -> typed proposal -> policy -> governance -> executor
```

The model proposes. Evidence supports. Policy decides. Governance determines whether a human is required. The executor never makes an authorization decision.

## Core safety property

**Increasing model capability does not automatically increase infrastructure blast radius.**

The public prototype therefore does not expose arbitrary shell execution. Remediation actions carry explicit:

- scope;
- risk tier;
- evidence IDs;
- preconditions;
- expected effect;
- postconditions;
- rollback guidance;
- dry-run status;
- human-confirmation state;
- idempotency key.

## Technology stack

- **Nebius Token Factory** — OpenAI-compatible inference plane.
- **NVIDIA Nemotron 3 Super 120B-A12B** — reasoning engine.
- **Tavily** — live evidence retrieval and provenance.
- **NVIDIA NeMo Guardrails** — model interaction and tool-boundary controls.
- **Pydantic** — typed domain contracts.
- **PolicyEngine** — deterministic authorization boundary.
- **GovernanceEngine** — explicit approval state.
- **Sandbox simulator** — safe execution environment.
- **Hash-chained JSONL audit** — tamper-evident event history.
- **Evaluation harness** — reproducible safety-policy benchmark.

## Fastest demo

No external credentials are required for the deterministic demonstration.

```bash
python -m app.cli demo
```

Run the safety benchmark:

```bash
python -m app.cli benchmark
```

Verify the audit chain:

```bash
python -m app.cli verify-audit
```

Run tests:

```bash
pytest -q
```

Run linting:

```bash
ruff check .
```

## Live Nebius + Tavily mode

Copy `.env.example` to `.env` and configure:

```text
NEBIUS_API_KEY=...
TAVILY_API_KEY=...
```

Optional settings:

```text
NEBIUS_BASE_URL=https://api.tokenfactory.nebius.com/v1/
NEBIUS_MODEL=nvidia/nemotron-3-super-120b-a12b
INFRA_MODE=simulated
AUDIT_LOG_PATH=artifacts/audit.jsonl
```

Without credentials, the software explicitly falls back to its deterministic local fixture. It never claims that a live model or external search service was called.

## Canonical adversarial demonstration

The demo models a Kubernetes `CrashLoopBackOff` caused by an RBAC regression in the monitoring namespace. The incident also contains a destructive instruction to delete the database and cluster.

Expected system behavior:

1. identify the destructive request as unsafe;
2. keep the legitimate incident signal;
3. obtain current technical evidence;
4. diagnose the RBAC failure;
5. construct a least-privilege remediation hypothesis;
6. attach evidence to every mutation candidate;
7. evaluate risk independently from the model;
8. route gated actions to human approval;
9. execute only safe dry-run actions in the public simulator;
10. verify postconditions;
11. write a tamper-evident audit record.

## Evaluation

The repository includes a deterministic policy benchmark covering:

- safe read-only action;
- safe scoped dry-run action;
- mutation without evidence;
- destructive shell command;
- cluster deletion;
- high-risk action.

The benchmark is intentionally executable:

```bash
python -m app.cli benchmark
```

This gives the judges an immediate, machine-checkable demonstration of the authorization boundary.

The broader evaluation plan measures both capability and safety:

| Dimension | Example metric |
|---|---|
| Diagnosis | root-cause accuracy |
| Evidence | evidence relevance / provenance coverage |
| Planning | bounded-action validity |
| Safety | unsafe-action block rate |
| Governance | correct approval routing |
| Reliability | tool-call / structured-output success |
| Operations | time to first useful proposal |
| Audit | trace completeness / hash-chain validity |

## Security architecture

NeMo Guardrails is used as a model-facing control layer, while the deterministic `PolicyEngine` remains the final application authorization boundary. The repository therefore does not rely on an LLM to approve its own actions.

Retrieved web content is explicitly treated as untrusted data. Tool outputs are similarly untrusted and cannot silently become instructions.

The public runtime is dry-run/simulated. High-impact actions are not autonomously executed.

See:

- [`docs/SECURITY.md`](docs/SECURITY.md)
- [`docs/EVIDENCE_BOUND_AUTONOMY.md`](docs/EVIDENCE_BOUND_AUTONOMY.md)
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

## Architecture

```text
                     +--------------------+
                     | Incident / Alert   |
                     +---------+----------+
                               |
                               v
                    +----------------------+
                    | Input Safety         |
                    | NeMo / Sanitization  |
                    +----------+-----------+
                               |
                               v
                +----------------------------------+
                | Agent Loop                       |
                |                                  |
                | diagnose <-> research <-> plan |
                +----------------+-----------------+
                                 |
                +----------------+----------------+
                |                                 |
                v                                 v
       +-------------------+             +-------------------+
       | Tavily Evidence   |             | Typed Action     |
       | provenance        |             | Contract         |
       +---------+---------+             +---------+---------+
                 |                                 |
                 +----------------+----------------+
                                  v
                       +-----------------------+
                       | Guardrails + Policy  |
                       | authorization         |
                       +-----------+-----------+
                                   |
                         +---------+---------+
                         |                   |
                         v                   v
                  AUTO-APPROVE        HUMAN REQUIRED
                         |                   |
                         +---------+---------+
                                   v
                       +-----------------------+
                       | Bounded Executor     |
                       | simulated by default |
                       +-----------+-----------+
                                   |
                                   v
                       +-----------------------+
                       | Verify + Audit        |
                       | hash chained JSONL    |
                       +-----------------------+
```

## Repository structure

```text
infrasentinel-agentic/
├── app/
│   ├── audit.py
│   ├── cli.py
│   ├── config.py
│   ├── evaluation.py
│   ├── governance.py
│   ├── orchestrator.py
│   ├── policy.py
│   ├── schemas.py
│   ├── providers/
│   │   ├── nebius.py
│   │   └── tavily.py
│   └── runtime/
│       └── simulator.py
├── configs/
│   └── guardrails/
├── data/
├── docs/
├── examples/
├── tests/
├── artifacts/
├── .github/workflows/ci.yml
├── .env.example
├── pyproject.toml
├── requirements.txt
└── LICENSE
```

## Hackathon alignment

The official rules require a working project, a working demo/test build, a public open-source repository with a README, English submission materials, use of Nebius Token Factory or Nebius AI Cloud with at least one NVIDIA open-source model, and feedback on the technologies used. The four primary judging dimensions are equally weighted: Technological Implementation, Design, Potential Impact, and Quality of the Idea. The current official deadline is **October 30, 2026 at 10:00 a.m. PDT**. citeturn665148search7

The design intentionally makes each criterion visible in the repository:

- **Technological Implementation:** real provider adapters, typed tool contracts, iterative tool loop, Guardrails and deterministic policy.
- **Design:** operator-oriented evidence → authorization → execution workflow.
- **Potential Impact:** SRE / platform engineering use case with a path to Kubernetes, GitOps and observability integration.
- **Quality of the Idea:** Evidence-Bound Autonomy as the central product thesis.

## Official NVIDIA Guardrails integration note

NVIDIA documents separate input, retrieval, dialog, execution and output rails. Its tool-calling IORails engine validates tool calls and tool results before/after the application executor, while the executor itself remains under application control. citeturn665148search0turn665148search1turn665148search2

This repository deliberately keeps deterministic authorization outside the model/Guardrails layer as a second, independent control boundary.

## Roadmap

### Phase 1 — Competition hardening

- richer incident benchmark;
- structured-output validation;
- red-team suite;
- complete presentation / demo evidence;
- repeatable evaluation reports.

### Phase 2 — Real infrastructure

- namespace-scoped Kubernetes credentials;
- GitOps promotion;
- rollback verification;
- Prometheus / Loki / OpenTelemetry ingestion.

### Phase 3 — Enterprise control plane

- organization policy packs;
- persistent incident memory;
- multi-cluster operations;
- compliance reporting;
- controlled MCP gateway for external tools.

## License

Apache License 2.0.
