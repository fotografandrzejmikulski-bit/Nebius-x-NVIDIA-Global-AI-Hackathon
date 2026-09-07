from __future__ import annotations

import argparse
import json
import sys

from app.config import Settings
from app.evaluation import benchmark_summary
from app.orchestrator import AgentOrchestrator
from app.schemas import Incident


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="infrasentinel", description="Evidence-first autonomous SRE demo")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("demo", help="run the deterministic incident demonstration")
    sub.add_parser("benchmark", help="run the deterministic safety-policy benchmark")
    sub.add_parser("verify-audit", help="verify the audit hash chain")
    investigate = sub.add_parser("investigate", help="investigate a custom incident")
    investigate.add_argument("description", nargs="+", help="incident description")

    args = parser.parse_args(argv)
    settings = Settings.load()

    if args.command == "benchmark":
        print(json.dumps(benchmark_summary(), indent=2))
        return 0

    if args.command == "verify-audit":
        ok, message = AgentOrchestrator(settings).audit.verify()
        print(json.dumps({"verified": ok, "message": message}, indent=2))
        return 0 if ok else 2

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
