# InfraSentinel-Agentic

**Evidence-first autonomous SRE for safe, bounded remediation.**

InfraSentinel-Agentic is a competition-grade prototype for the **Nebius x NVIDIA Global AI Hackathon 2026**, targeting the **Coding and Agentic Engineering** track and the **Best Use of Tavily** bonus.

> **The agent may reason freely, but it may act only inside a bounded, evidence-backed policy envelope.**

## What it does

InfraSentinel turns infrastructure incidents into a controlled loop:

```text
incident
  -> input safety
  -> live evidence (Tavily)
  -> reasoning (NVIDIA Nemotron on Nebius)
  -> typed remediation proposal
  -> NeMo Guardrails
  -> deterministic policy authorization
  -> dry-run / sandbox execution
  -> verification
  -> audit
```

The public prototype deliberately avoids arbitrary shell execution. Actions are structured objects with explicit scope, risk tier, evidence references, expected effect and rollback guidance.

## Why this is different

A normal LLM agent looks like:

```text
LLM -> tool -> infrastructure
```

InfraSentinel uses:

```text
LLM -> evidence -> policy -> bounded executor
```

The model proposes. Evidence constrains. Policy authorizes. The executor applies only what is allowed.

## Stack

- **Nebius Token Factory** — OpenAI-compatible inference plane.
- **NVIDIA Nemotron 3 Super 120B-A12B** — reasoning engine.
- **Tavily** — live technical research and evidence provenance.
- **NVIDIA NeMo Guardrails** — LLM interaction and tool-boundary controls.
- **Pydantic** — typed incident/evidence/action contracts.
- **Deterministic PolicyEngine** — final authorization boundary.
- **Sandbox simulator** — safe public execution path.
- **JSONL audit trail** — reconstructable decision history.

## Demo

Run without external credentials:

```bash
python -m app.cli demo
```

Run a custom incident:

```bash
python -m app.cli investigate "Kubernetes CrashLoopBackOff after RBAC regression"
```

Run tests:

```bash
pytest -q
```

Run linting:

```bash
ruff check .
```

## Live mode

Copy `.env.example` to `.env` and configure:

```text
NEBIUS_API_KEY=...
TAVILY_API_KEY=...
```

Optional settings include `NEBIUS_BASE_URL`, `NEBIUS_MODEL`, `INFRA_MODE` and `AUDIT_LOG_PATH`.

The Nebius adapter uses the OpenAI-compatible API. When credentials are absent, the system runs a deterministic local demonstration rather than pretending a live model or search service is available.

## Security model

Autonomous actions are evaluated independently from the LLM. The deterministic policy blocks destructive patterns, high-impact risk tiers, missing evidence on mutations and broad production scope.

Web pages and tool outputs are treated as untrusted data. They are never implicitly promoted to executable instructions.

The default runtime is simulated/dry-run.

See [`docs/EVIDENCE_BOUND_AUTONOMY.md`](docs/EVIDENCE_BOUND_AUTONOMY.md) and [`docs/SECURITY.md`](docs/SECURITY.md).

## Canonical demonstration

A Kubernetes `CrashLoopBackOff` is associated with an RBAC regression in the monitoring namespace. The input also includes a malicious request to delete the database and cluster.

Expected behavior:

1. reject the destructive intent;
2. preserve the useful diagnostic signal;
3. research current RBAC evidence;
4. propose the smallest scoped remediation;
5. require evidence linkage;
6. validate the operation against deterministic policy;
7. execute only in simulation;
8. produce an auditable result.

## Repository structure

```text
infrasentinel-agentic/
├── app/
│   ├── audit.py
│   ├── cli.py
│   ├── config.py
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
│   └── demo_incidents.json
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DEMO_SCRIPT.md
│   ├── EVIDENCE_BOUND_AUTONOMY.md
│   ├── GRANT_APPLICATION.md
│   ├── GRANT_APPLICATION_2026.md
│   ├── PROTOTYPE.md
│   └── SECURITY.md
├── examples/
│   └── rbac-fix.yaml
├── tests/
├── artifacts/
├── .github/workflows/ci.yml
├── .env.example
├── pyproject.toml
├── requirements.txt
└── LICENSE
```

## Hackathon alignment

The official hackathon rules require a working project, a working demo/test build, a public open-source repository with a README, English submission materials, use of Nebius Token Factory or Nebius AI Cloud with at least one NVIDIA open-source model, and feedback on the technologies used. Judging is equally weighted across Technological Implementation, Design, Potential Impact, and Quality of the Idea.

InfraSentinel is explicitly built around those requirements. Tavily is a runtime component, positioning the project for the Best Use of Tavily bonus subject to the official eligibility rules.

## Roadmap

1. Kubernetes and observability adapters with namespace-scoped credentials.
2. GitOps promotion and rollback verification.
3. Persistent incident memory and continuous evaluation.
4. Enterprise policy packs.
5. Policy-governed MCP gateway for external tools.

## License

Apache License 2.0.
