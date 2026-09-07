# Working Prototype

The prototype intentionally has two operating modes.

## Offline judge/demo mode

No credentials are required. The system uses a deterministic incident fixture and a simulated infrastructure adapter. This makes the public repository reproducible and prevents accidental changes to real infrastructure.

```bash
python -m app.cli demo
```

Expected behavior:

1. an RBAC-related Kubernetes incident is received;
2. a diagnosis is produced;
3. read-only inspection is allowed;
4. a least-privilege RBAC server-side dry-run is allowed;
5. destructive operations remain outside the policy envelope;
6. audit events are written to `artifacts/audit.jsonl`.

## Live model + Tavily mode

Set:

```bash
NEBIUS_API_KEY=...
TAVILY_API_KEY=...
```

Then run:

```bash
python -m app.cli investigate "Kubernetes CrashLoopBackOff after RBAC change"
```

The live path sends the reasoning request to the configured Nebius Token Factory model and uses Tavily for current evidence retrieval. The application still enforces the same deterministic policy before simulated execution.

## Important prototype boundary

The project does not claim that the public demo is a production cluster operator. It demonstrates the control plane and safety architecture. Real infrastructure execution belongs behind a separately reviewed adapter with least-privilege identity and organizational change control.
