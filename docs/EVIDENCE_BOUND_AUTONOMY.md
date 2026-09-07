# Evidence-Bound Autonomy

InfraSentinel's core safety construct is an action-level autonomy envelope.

An AI-generated operation is not executable authority. Before an operation crosses into the runtime it must satisfy explicit constraints:

1. **Evidence** — the operation references current evidence objects.
2. **Scope** — the target is explicitly bounded.
3. **Risk** — the requested risk tier is within the configured autonomous ceiling.
4. **Destructiveness** — known destructive operations are denied.
5. **Reversibility** — the action declares rollback guidance.
6. **Execution mode** — the prototype defaults to dry-run/simulation.
7. **Auditability** — the policy decision and execution result are recorded.

## Design Rule

> Reasoning is probabilistic; authorization is deterministic.

The reasoning model can propose multiple candidate actions. The policy layer decides which candidates can cross the execution boundary. This prevents increased model capability from automatically becoming increased infrastructure privilege.

## Production Extension

A production adapter should add workload identity, resource allowlists, admission control, short-lived credentials, GitOps promotion, explicit human approval for high-impact changes and post-action verification.
