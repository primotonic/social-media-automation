"""Small client for the AniList GraphQL API."""

import html
import math
import random
import re
from typing import Any

import requests


class AniListError(RuntimeError):
    """Raised when AniList cannot provide valid content."""


class AniListClient:
    _url = "https://graphql.anilist.co"

    def __init__(
        self,
        timeout: float = 30.0,
        session: requests.Session | None = None,
        rng: random.Random | None = None,
    ) -> None:
        self._timeout = timeout
        self._session = session or requests.Session()
        self._rng = rng or random.Random()

    def get_random_manga(self) -> dict[str, Any]:
        query = """
        query ($page: Int, $perPage: Int) {
          Page(page: $page, perPage: $perPage) {
            media(type: MANGA, sort: POPULARITY_DESC, averageScore_greater: 80) {
              id title { romaji english } coverImage { large }
              description(asHtml: false) genres siteUrl
            }
          }
        }
        """
        data = self._query(
            query, {"page": self._rng.randint(1, 20), "perPage": 10}
        )
        manga = self._rng.choice(data["Page"]["media"])
        manga["description"] = clean_description(manga.get("description"))
        return manga

    def get_random_character(self, max_attempts: int = 5) -> dict[str, Any]:
        query = """
        query ($page: Int, $perPage: Int) {
          Page(page: $page, perPage: $perPage) {
            pageInfo { total }
            characters {
              id name { full native } image { large } description favourites
              media(perPage: 3) { nodes { type title { english romaji } } }
            }
          }
        }
        """
        first_page = self._query(query, {"page": 1, "perPage": 1})["Page"]
        last_page = math.ceil(first_page["pageInfo"]["total"] / 50)

        for _ in range(max_attempts):
            page = self._query(
                query, {"page": self._rng.randint(1, last_page), "perPage": 50}
            )["Page"]
            if page["characters"]:
                return self._rng.choice(page["characters"])
        raise AniListError("AniList returned no characters after multiple attempts.")

    def _query(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        response = self._session.post(
            self._url,
            json={"query": query, "variables": variables},
            timeout=self._timeout,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("errors"):
            raise AniListError(f"AniList query failed: {payload['errors']}")
        return payload["data"]


def clean_description(description: str | None) -> str:
    if not description:
        return ""
    description = html.unescape(description)
    description = re.sub(r"<br\s*/?>", "\n", description, flags=re.IGNORECASE)
    description = re.sub(r"<[^>]+>", "", description)
    description = re.sub(r"~!(.*?)!~", r"\1", description)
    return re.sub(r"\n{3,}", "\n\n", description).strip()
