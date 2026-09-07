from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    nebius_api_key: str | None
    nebius_base_url: str
    nebius_model: str
    tavily_api_key: str | None
    infra_mode: str
    audit_log_path: Path

    @classmethod
    def load(cls) -> "Settings":
        load_dotenv()
        return cls(
            nebius_api_key=os.getenv("NEBIUS_API_KEY"),
            nebius_base_url=os.getenv("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/"),
            nebius_model=os.getenv("NEBIUS_MODEL", "nvidia/nemotron-3-super-120b-a12b"),
            tavily_api_key=os.getenv("TAVILY_API_KEY"),
            infra_mode=os.getenv("INFRA_MODE", "simulated"),
            audit_log_path=Path(os.getenv("AUDIT_LOG_PATH", "artifacts/audit.jsonl")),
        )

    @property
    def live_ready(self) -> bool:
        return bool(self.nebius_api_key and self.tavily_api_key)
