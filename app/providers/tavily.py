from __future__ import annotations

from app.schemas import Evidence


class TavilyProvider:
    """Live evidence provider. Falls back to no external evidence when not configured."""

    def __init__(self, api_key: str | None) -> None:
        self.api_key = api_key
        self.client = None
        if api_key:
            from tavily import TavilyClient

            self.client = TavilyClient(api_key=api_key)

    def search(self, query: str, domains: list[str] | None = None) -> list[Evidence]:
        if not self.client:
            return []
        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_raw_content=True,
            include_domains=domains or [
                "kubernetes.io",
                "docs.docker.com",
                "github.com",
            ],
            chunks_per_source=3,
            include_usage=True,
        )
        evidence: list[Evidence] = []
        for item in response.get("results", []):
            evidence.append(
                Evidence(
                    source="tavily",
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    excerpt=(item.get("raw_content") or item.get("content") or "")[:1800],
                    relevance=float(item.get("score", 0.0) or 0.0),
                )
            )
        return evidence
