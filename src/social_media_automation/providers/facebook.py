"""Facebook Page implementation of the social provider contract."""

from dataclasses import dataclass
from typing import Any

import requests

from social_media_automation.models import Post, PublishResult


class FacebookAPIError(RuntimeError):
    """Raised when Facebook returns an invalid or unsuccessful response."""


@dataclass(frozen=True)
class FacebookPage:
    id: str
    name: str
    access_token: str


class FacebookPageProvider:
    name = "facebook"

    def __init__(
        self,
        user_token: str,
        api_version: str = "v19.0",
        timeout: float = 30.0,
        session: requests.Session | None = None,
    ) -> None:
        self._user_token = user_token
        self._base_url = f"https://graph.facebook.com/{api_version}"
        self._timeout = timeout
        self._session = session or requests.Session()
        self._page: FacebookPage | None = None

    def publish(self, post: Post) -> PublishResult:
        page = self._get_page()
        endpoint = "photos" if post.image_url else "feed"
        data = {
            "access_token": page.access_token,
            "caption" if post.image_url else "message": post.message,
        }
        if post.image_url:
            data["url"] = post.image_url

        result = self._request("POST", f"/{page.id}/{endpoint}", data=data)
        post_id = str(result["id"])

        if post.first_comment:
            self._request(
                "POST",
                f"/{post_id}/comments",
                data={"message": post.first_comment, "access_token": page.access_token},
            )

        return PublishResult(platform=self.name, post_id=post_id, raw_response=result)

    def _get_page(self) -> FacebookPage:
        if self._page is None:
            result = self._request(
                "GET", "/me/accounts", params={"access_token": self._user_token}
            )
            pages = result.get("data", [])
            if not pages:
                raise FacebookAPIError("No Facebook Pages found for this user token.")
            page = pages[0]
            self._page = FacebookPage(
                id=str(page["id"]),
                name=page["name"],
                access_token=page["access_token"],
            )
        return self._page

    def _request(self, method: str, path: str, **kwargs: Any) -> dict:
        response = self._session.request(
            method, f"{self._base_url}{path}", timeout=self._timeout, **kwargs
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            try:
                details = response.json().get("error", {}).get("message", response.text)
            except ValueError:
                details = response.text
            raise FacebookAPIError(f"Facebook API request failed: {details}") from error
        return response.json()
