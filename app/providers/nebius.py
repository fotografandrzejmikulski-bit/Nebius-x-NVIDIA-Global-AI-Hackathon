from __future__ import annotations

import json
from typing import Any

from openai import OpenAI


class NebiusProvider:
    def __init__(self, api_key: str | None, base_url: str, model: str) -> None:
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url) if api_key else None

    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        if not self.client:
            return {"content": "", "tool_calls": []}
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools or None,
            tool_choice="auto" if tools else None,
            temperature=0.0,
            max_tokens=3500,
        )
        message = response.choices[0].message
        return {
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": call.id,
                    "name": call.function.name,
                    "arguments": json.loads(call.function.arguments),
                }
                for call in (message.tool_calls or [])
            ],
        }
