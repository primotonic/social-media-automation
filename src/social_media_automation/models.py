"""Platform-independent publishing models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Post:
    message: str
    image_url: str | None = None
    first_comment: str | None = None


@dataclass(frozen=True)
class PublishResult:
    platform: str
    post_id: str
    raw_response: dict
