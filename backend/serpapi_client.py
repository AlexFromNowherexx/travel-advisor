from __future__ import annotations

from dataclasses import dataclass
# pyrefly: ignore [missing-import]
import httpx

from .config import settings


@dataclass(slots=True)
class SerpApiResult:
    title: str
    link: str
    snippet: str | None = None


class SerpApiClientError(RuntimeError):
    pass


class SerpApiClient:
    def __init__(self) -> None:
        self.api_key = settings.serpapi_api_key
        self.limit = settings.serpapi_limit

    def enabled(self) -> bool:
        return bool(self.api_key)

    def search(self, query: str) -> list[SerpApiResult]:
        if not self.enabled():
            return []

        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "num": self.limit,
        }
        url = "https://serpapi.com/search"

        try:
            response = httpx.get(url, params=params, timeout=20)
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise SerpApiClientError(f"SerpAPI request failed: {exc}") from exc

        organic_results = payload.get("organic_results") or []
        results: list[SerpApiResult] = []
        for item in organic_results[: self.limit]:
            results.append(
                SerpApiResult(
                    title=str(item.get("title") or "No Title"),
                    link=str(item.get("link") or ""),
                    snippet=item.get("snippet"),
                )
            )
        return results


_client = SerpApiClient()


def get_serpapi_results(query: str) -> list[SerpApiResult]:
    return _client.search(query=query)
