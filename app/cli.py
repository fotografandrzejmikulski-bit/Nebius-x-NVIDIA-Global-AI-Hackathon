from __future__ import annotations

import argparse
import json
import sys

from app.config import Settings
from app.orchestrator import AgentOrchestrator
from app.schemas import Incident


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="infrasentinel", description="Evidence-first autonomous SRE demo")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("demo", help="run the deterministic incident demonstration")
    investigate = sub.add_parser("investigate", help="investigate a custom incident")
    investigate.add_argument("description", nargs="+", help="incident description")

    args = parser.parse_args(argv)
    settings = Settings.load()
    orchestrator = AgentOrchestrator(settings)

    description = (
        "Production Kubernetes CrashLoopBackOff in monitoring after a ServiceAccount RBAC change; "
        "recovery must be safe and minimal."
        if args.command == "demo"
        else " ".join(args.description)
    )
    incident = Incident(title="Kubernetes incident", description=description, service="kubernetes")
    result = orchestrator.investigate(incident)

    print(json.dumps(result.model_dump(mode="json"), indent=2, ensure_ascii=False))
    if result.blocked_actions:
        print("\nBLOCKED BY POLICY:")
        for item in result.blocked_actions:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
