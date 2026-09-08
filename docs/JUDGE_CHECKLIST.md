# Judge Verification Checklist

This page is a reviewer-first map from hackathon evaluation criteria to inspectable repository evidence.

## 1. Technological Implementation

- Nebius integration: `app/providers/nebius.py`
- NVIDIA Nemotron model default: `app/config.py`
- Tavily runtime research: `app/providers/tavily.py`
- Typed action/evidence contracts: `app/schemas.py`
- Deterministic authorization: `app/policy.py`
- Human governance boundary: `app/governance.py`
- Safe execution boundary: `app/runtime/simulator.py`
- Audit trail: `app/audit.py`
- Evaluation harness: `app/evaluation.py`
- CI: `.github/workflows/ci.yml`

## 2. Design

Primary design thesis:

> Reasoning is probabilistic; authorization is deterministic.

Review `docs/ARCHITECTURE.md` and `docs/EVIDENCE_BOUND_AUTONOMY.md` for the control model.

## 3. Potential Impact

Review `docs/GRANT_APPLICATION.md` for the problem definition, target users, commercial pathway, evaluation strategy and production roadmap.

The intended value proposition is bounded autonomous incident response: improve time-to-diagnosis and operator leverage without making unrestricted infrastructure authority a side effect of LLM capability.

## 4. Quality of Idea

The differentiating construct is the **Evidence-Bound Autonomy Envelope**:

- evidence-backed action;
- explicit target scope;
- risk tier;
- reversibility requirement;
- deterministic authorization;
- human escalation;
- auditable execution.

## 5. Safety Demonstration

The canonical demo should contain both:

1. a legitimate Kubernetes incident requiring diagnosis and remediation; and
2. an adversarial/destructive instruction that must be denied.

Expected result: preserve useful diagnostic signal while refusing unauthorized destructive authority.

## 6. Reproducibility

```bash
python -m app.cli demo
pytest -q
ruff check .
python -m compileall app
```

The local demo does not require external credentials and uses the simulator by default.

## 7. Submission Claims Discipline

The repository intentionally distinguishes:

- implemented now;
- demo-only behavior;
- production roadmap items.

Live Nebius/Tavily behavior requires valid credentials. Production infrastructure mutation is not claimed as implemented in the public demo.
