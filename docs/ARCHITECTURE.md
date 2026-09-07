# InfraSentinel-Agentic — Architecture

## 1. Design thesis

InfraSentinel is not an LLM that happens to have shell access. It is a policy-governed incident response system in which the model is a planner and synthesizer, while evidence, schemas, and policy boundaries constrain what can become an action.

## 2. Control loop

```text
Incident
  -> normalize + classify
  -> retrieve current evidence
  -> diagnose
  -> propose typed actions
  -> policy evaluation
  -> dry-run execution
  -> observe result
  -> audit
```

This loop creates a clean separation of concerns:

- **Nebius / Nemotron:** reasoning and plan generation.
- **Tavily:** current external evidence.
- **NeMo Guardrails:** LLM interaction and tool-boundary controls.
- **Policy Engine:** deterministic authorization decision.
- **Runtime Adapter:** actual effect boundary.
- **Audit Trail:** machine-readable trace of each transition.

## 3. Evidence contract

An action is not considered autonomous-safe merely because the model proposed it. Every non-read action must link to evidence identifiers and stay below the configured risk ceiling. Evidence is preserved as source URL, title, excerpt and relevance score.

## 4. Action model

Each action carries:

- unique ID,
- target scope,
- risk tier,
- dry-run flag,
- evidence references,
- expected effect,
- rollback strategy.

The explicit model is important because free-form command generation makes downstream enforcement ambiguous.

## 5. Failure posture

The default posture is fail-closed:

- missing credentials -> local deterministic demo instead of pretending live access exists;
- missing evidence -> deny non-read action;
- high/critical action -> deny autonomous execution;
- broad production scope -> deny autonomous execution;
- destructive command signature -> deny;
- simulator non-dry-run -> deny.

## 6. Production evolution

A production deployment would replace the simulator with scoped adapters. The policy interface remains unchanged. This is intentional: infrastructure-specific implementation should be replaceable without weakening authorization logic.

## 7. Why this is agentic engineering

The intelligence lives in the iterative loop, not in a single completion. The agent can research, revisit its hypothesis, construct a plan, receive tool results, and decide what should happen next. The execution layer never delegates authorization back to the model.
