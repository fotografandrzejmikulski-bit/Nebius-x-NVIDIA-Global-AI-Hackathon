from __future__ import annotations

from app.schemas import RemediationAction


class SimulatedInfrastructure:
    """Safe deterministic executor used by the public prototype."""

    def execute(self, action: RemediationAction) -> str:
        if not action.dry_run:
            return "EXECUTION_REFUSED: simulated runtime only permits dry-run actions."
        return (
            f"DRY-RUN OK: {action.name} against target={action.target}; "
            f"command={action.command}; expected_effect={action.expected_effect}"
        )
