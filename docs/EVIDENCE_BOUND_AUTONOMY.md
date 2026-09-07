# Evidence-Bound Autonomy

## The central design principle

InfraSentinel treats autonomous infrastructure action as an **authorization problem**, not merely a generation problem.

> **Reasoning is probabilistic; authorization is deterministic.**

The model can explore hypotheses and propose candidate actions. It does not decide whether the action is permitted.

## Action-level autonomy envelope

Every proposed operation is evaluated across independent dimensions:

| Dimension | Required property |
|---|---|
| Evidence | mutation references explicit evidence objects |
| Provenance | source URL and retrieval metadata are retained |
| Scope | target resource is explicit and narrow |
| Risk | action is assigned a typed risk tier |
| Destructiveness | known destructive classes are denied |
| Reversibility | rollback guidance is present |
| Preconditions | conditions that must hold before execution are declared |
| Postconditions | observable success criteria are declared |
| Governance | auto-approval vs human approval is explicit |
| Execution mode | public prototype is dry-run/simulated |
| Auditability | policy and execution events are hash chained |

## Why four boundaries instead of one

### 1. Model boundary

Nemotron decides what it believes should be investigated or proposed.

### 2. Evidence boundary

Tavily supplies current technical material. Retrieved content remains untrusted data; a webpage cannot grant authority.

### 3. Policy boundary

The deterministic policy engine checks risk, scope, evidence and destructive patterns independently of the model.

### 4. Governance boundary

Even an allowed action can be routed to human approval based on risk, execution mode or explicit confirmation requirements.

This makes **allowed**, **approved**, and **executed** three separate states rather than one overloaded boolean.

## Formal intuition

A candidate action \(a\) is eligible for autonomous execution only when:

\[
A(a)=E(a) \land S(a) \land R(a) \land D(a) \land V(a) \land M(a)
\]

where:

- \(E\) = sufficient evidence;
- \(S\) = bounded scope;
- \(R\) = risk within policy ceiling;
- \(D\) = not in a denied destructive class;
- \(V\) = reversibility / verification requirements satisfied;
- \(M\) = permitted execution mode.

Governance then determines whether \(A(a)\) results in automatic execution or human approval.

The equation is a design model rather than a claim that safety can be reduced to one mathematical score.

## Production evolution

The public prototype deliberately stops short of live infrastructure mutation. Production adapters should add:

- workload identity;
- resource allowlists;
- namespace-scoped service accounts;
- admission control;
- short-lived credentials;
- GitOps promotion;
- approval workflows;
- rollback verification;
- secret and PII redaction;
- network egress controls;
- persistent audit storage.

The policy contract should remain stable while infrastructure adapters change.
