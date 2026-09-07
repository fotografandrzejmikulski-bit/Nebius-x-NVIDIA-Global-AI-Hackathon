# Judges' Verification Checklist

This file is intentionally concise: a reviewer should be able to verify the principal claims without reading the entire repository first.

## Criterion 1 — Technological Implementation

- [x] Nebius provider exists in `app/providers/nebius.py`.
- [x] NVIDIA Nemotron model is configurable and defaulted explicitly.
- [x] Tavily provider performs live evidence retrieval and preserves source metadata.
- [x] Typed tool contracts constrain model-generated arguments.
- [x] Iterative model/tool loop supports multiple reasoning rounds.
- [x] Deterministic `PolicyEngine` is independent of model output.
- [x] `GovernanceEngine` distinguishes automatic approval from human approval.
- [x] Runtime simulator is dry-run only.
- [x] Audit stream is tamper-evident through a SHA-256 hash chain.
- [x] Deterministic policy benchmark is executable with `python -m app.cli benchmark`.

## Criterion 2 — Design

- [x] Incident → evidence → diagnosis → action is explicit.
- [x] Authorization is separated from model reasoning.
- [x] Evidence provenance is retained as first-class state.
- [x] Scope, risk, reversibility, preconditions and postconditions are modeled explicitly.
- [x] Human-in-the-loop is represented as a first-class governance state.

## Criterion 3 — Potential Impact

- [x] Primary use case is SRE / platform engineering.
- [x] Public runtime is safe for reproducible demonstration.
- [x] Production roadmap specifies Kubernetes, GitOps and observability adapters.
- [x] The architecture is provider-adapter based rather than tied to one executor.

## Criterion 4 — Quality of the Idea

- [x] Core thesis is Evidence-Bound Autonomy.
- [x] Safety is an architectural property rather than a prompt-only instruction.
- [x] The central proposition is falsifiable and benchmarkable.
- [x] The concept generalizes beyond one incident type.

## Demo commands

```bash
python -m app.cli demo
python -m app.cli benchmark
python -m app.cli verify-audit
pytest -q
ruff check .
```

## Important evidence boundary

The public repository demonstrates the architecture and safe simulator. It does **not** claim that production Kubernetes mutation is already implemented. Live infrastructure adapters remain a future controlled-deployment step.
