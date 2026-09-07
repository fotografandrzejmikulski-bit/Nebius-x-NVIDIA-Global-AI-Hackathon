# 2:30 Judge Demo Script

## 0:00–0:15 — The problem

Show the CLI and say:

> "LLMs can explain infrastructure incidents, but explanation is not authorization. InfraSentinel is built around that distinction."

## 0:15–0:40 — Incident intake

Run:

```bash
python -m app.cli demo
```

Show the incident and the generated structured result.

## 0:40–1:05 — Evidence

Explain that the live configuration calls Tavily against authoritative infrastructure sources. The system preserves URLs and excerpts as evidence rather than treating search output as anonymous context.

## 1:05–1:30 — Reasoning

Show diagnosis and two actions:

1. read-only RBAC inspection;
2. least-privilege RBAC server-side dry-run.

Emphasize that every non-read action is evidence-bound.

## 1:30–1:55 — Safety boundary

Explain:

> "The model proposes. The policy engine authorizes. The simulator executes. These are separate trust boundaries."

Show that destructive production actions are blocked by deterministic policy.

## 1:55–2:15 — Auditability

Show `artifacts/audit.jsonl` and point to incident receipt, evidence collection, policy evaluation and execution events.

## 2:15–2:30 — Close

> "InfraSentinel does not try to make the model infallible. It makes the system resilient to model uncertainty. Reason broadly. Act narrowly."
