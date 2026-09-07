from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


class AuditTrail:
    """Append-only, tamper-evident JSONL event stream using a hash chain."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._previous_hash = self._load_previous_hash()

    def _load_previous_hash(self) -> str:
        if not self.path.exists():
            return "0" * 64
        last = "0" * 64
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                last = json.loads(line).get("event_hash", last)
        return last

    def record(self, event_type: str, payload: dict[str, Any]) -> str:
        event_id = str(uuid4())
        event = {
            "event_id": event_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "payload": payload,
            "previous_hash": self._previous_hash,
        }
        canonical = json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        event_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        event["event_hash"] = event_hash
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        self._previous_hash = event_hash
        return event_id

    def verify(self) -> tuple[bool, str]:
        previous = "0" * 64
        if not self.path.exists():
            return True, "empty"
        for index, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            event = json.loads(line)
            supplied = event.pop("event_hash", "")
            if event.get("previous_hash") != previous:
                return False, f"chain break at line {index}"
            canonical = json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            expected = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
            if supplied != expected:
                return False, f"hash mismatch at line {index}"
            previous = supplied
        return True, "verified"
