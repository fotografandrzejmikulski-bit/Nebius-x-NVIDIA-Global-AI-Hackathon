from __future__ import annotations

import json
from typing import Any

from openai import OpenAI


class NebiusProvider:
    """Thin OpenAI-compatible adapter for Nebius Token Factory."""

    def __init__(self, api_key: str | None, base_url: str, model: str) -> None:
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url) if api_key else None

    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        if not self.client:
            return {"content": "", "tool_calls": [], "assistant_message": {"role": "assistant", "content": ""}}

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools or None,
            tool_choice="auto" if tools else None,
            temperature=0.0,
            max_tokens=3500,
        )
        message = response.choices[0].message
        raw_calls = message.tool_calls or []
        tool_calls = []
        for call in raw_calls:
            try:
                arguments = json.loads(call.function.arguments or "{}")
            except json.JSONDecodeError as exc:
                arguments = {"_parse_error": str(exc)}
            tool_calls.append({"id": call.id, "name": call.function.name, "arguments": arguments})

        assistant_message: dict[str, Any] = {"role": "assistant", "content": message.content or ""}
        if raw_calls:
            assistant_message["tool_calls"] = [
                {
                    "id": c.id,
                    "type": "function",
                    "function": {"name": c.function.name, "arguments": c.function.arguments or "{}"},
                }
                for c in raw_calls
            ]
        return {"content": message.content or "", "tool_calls": tool_calls, "assistant_message": assistant_message}
