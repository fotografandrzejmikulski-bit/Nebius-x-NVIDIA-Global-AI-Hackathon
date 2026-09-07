# InfraSentinel-Agentic

**Evidence-first autonomous SRE for safe incident diagnosis and bounded remediation.**

InfraSentinel-Agentic is a competition-grade prototype for the **Nebius x NVIDIA Global AI Hackathon 2026**. It uses NVIDIA Nemotron served through Nebius Token Factory, Tavily for live technical research, and NVIDIA NeMo Guardrails as a policy enforcement layer around tool use.

The core design principle is simple:

> **The agent may reason freely, but it may act only inside a bounded, evidence-backed policy envelope.**

## Why this project exists

Traditional automation can execute known playbooks, while generic LLM agents can produce plausible but unsafe commands. InfraSentinel combines model reasoning with live evidence, typed incident state, deterministic risk classification, a dry-run/apply boundary, and immutable audit events.

## Hackathon alignment

- **Primary track:** Coding and Agentic Engineering
- **Required platform:** Nebius Token Factory
- **NVIDIA model:** `nvidia/nemotron-3-super-120b-a12b`
- **Tavily:** runtime search for current infrastructure documentation
- **NVIDIA NeMo Guardrails:** input and output safety plus tool-call policy checks
- **Demo mode:** deterministic local simulation; no real infrastructure is touched by default

The hackathon requires a working software application on Nebius Token Factory or Nebius AI Cloud, use of at least one NVIDIA open-source model, a public open-source repository, a README with run instructions, a working demo/test build, and a public demonstration video shorter than three minutes. See the official rules: https://nebiusglobalaihackathon.devpost.com/rules

## Architecture

```text
                         +----------------------+
                         | Incident / Operator  |
                         +----------+-----------+
                                    |
                                    v
                       +--------------------------+
                       | Input Policy + Sanitizer |
                       | NeMo Guardrails          |
                       +------------+-------------+
                                    |
                                    v
                 +-------------------------------------------+
                 | Agent Orchestrator                         |
                 |                                           |
                 | 1. classify incident                     |
                 | 2. research current evidence             |
                 | 3. synthesize diagnosis                   |
                 | 4. create bounded remediation plan       |
                 | 5. score risk / require evidence          |
                 +-------------------+-----------------------+
                                     |
                      +--------------+--------------+
                      |                             |
                      v                             v
             +----------------+           +---------------------+
             | Tavily Search  |           | Policy Engine       |
             | live evidence  |           | allow / deny / ask  |
             +--------+-------+           +----------+----------+
                      |                              |
                      +---------------+--------------+
                                      |
                                      v
                             +------------------+
                             | Sandbox Executor |
                             | dry-run default  |
                             +--------+---------+
                                      |
                                      v
                             +------------------+
                             | Audit Trail      |
                             | JSONL events     |
                             +------------------+
```

## Safety model

The prototype deliberately does **not** expose arbitrary shell execution. Remediation is represented as structured actions with:

- explicit action IDs,
- target scope,
- risk tier,
- evidence references,
- expected effect,
- rollback guidance,
- dry-run support,
- deterministic allow/deny policy.

High-impact operations are denied in the demo policy. The architecture is designed so a future production adapter can connect to Kubernetes, cloud APIs, CI/CD or ticketing systems without removing the policy boundary.

## Live Tavily research

The Tavily adapter uses advanced search with raw content and domain constraints. Current Tavily documentation confirms `advanced`, `include_raw_content`, `include_domains`, and `chunks_per_source` as supported controls for search. The implementation intentionally keeps source URLs and excerpts in the evidence model so the final report can cite where a recommendation came from.

## Running locally

### 1. Environment

```bash
cp .env.example .env
# set NEBIUS_API_KEY and TAVILY_API_KEY
```

### 2. Install

Python 3.11+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Demo

The demo runs without touching real infrastructure:

```bash
python -m app.cli demo
```

You can also run a custom incident:

```bash
python -m app.cli investigate "Kubernetes CrashLoopBackOff after RBAC change"
```

With `TAVILY_API_KEY` and `NEBIUS_API_KEY` configured, the live path calls the real services. Without credentials, the deterministic demo fixture keeps the software runnable for judges and local review.

## Test suite

```bash
pytest -q
```

The tests cover policy decisions, destructive-action denial, evidence requirements, demo execution, and serialization.

## Configuration

Environment variables:

- `NEBIUS_API_KEY` — Nebius Token Factory API key
- `NEBIUS_BASE_URL` — optional override for the Nebius OpenAI-compatible endpoint
- `NEBIUS_MODEL` — defaults to NVIDIA Nemotron 3 Super
- `TAVILY_API_KEY` — Tavily API key
- `INFRA_MODE` — `simulated` by default
- `AUDIT_LOG_PATH` — JSONL audit path, defaults to `artifacts/audit.jsonl`

## Repository layout

```text
infraSentinel-agentic/
├── app/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── schemas.py
│   ├── orchestrator.py
│   ├── policy.py
│   ├── audit.py
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── nebius.py
│   │   └── tavily.py
│   └── runtime/
│       ├── __init__.py
│       └── simulator.py
├── configs/
│   └── guardrails/
├── data/
│   └── demo_incidents.json
├── tests/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── SECURITY.md
│   └── GRANT_APPLICATION.md
├── artifacts/
│   └── .gitkeep
├── .env.example
├── .gitignore
├── LICENSE
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Roadmap beyond the hackathon

1. Kubernetes adapter with namespace-scoped service accounts.
2. GitOps change proposals and automatic rollback verification.
3. Prometheus/Loki/OpenTelemetry adapters.
4. Policy packs for different regulated environments.
5. Continuous evaluation against an incident benchmark.
6. Optional MCP gateway so the same policy engine protects external tool servers.

## License

Apache License 2.0. See `LICENSE`.
