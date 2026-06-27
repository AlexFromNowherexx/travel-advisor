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


@dataclass(slots=True)
class SerpApiImageResult:
    title: str
    image_url: str
    thumbnail_url: str | None = None
    source_url: str | None = None


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

    def search_images(self, query: str) -> list[SerpApiImageResult]:
        if not self.enabled():
            return []

        params = {
            "engine": "google_images",
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
            raise SerpApiClientError(f"SerpAPI image request failed: {exc}") from exc

        image_results = payload.get("images_results") or []
        results: list[SerpApiImageResult] = []
        for item in image_results[: self.limit]:
            original = item.get("original") or item.get("thumbnail")
            if not original:
                continue
            results.append(
                SerpApiImageResult(
                    title=str(item.get("title") or "Travel image"),
                    image_url=str(original),
                    thumbnail_url=item.get("thumbnail"),
                    source_url=item.get("link") or item.get("source"),
                )
            )
        return results


_client = SerpApiClient()


def get_serpapi_results(query: str) -> list[SerpApiResult]:
    return _client.search(query=query)


def get_serpapi_image_results(query: str) -> list[SerpApiImageResult]:
    return _client.search_images(query=query)
