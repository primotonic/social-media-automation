"""Contract implemented by every social platform adapter."""

from typing import Protocol

from social_media_automation.models import Post, PublishResult


class SocialProvider(Protocol):
    name: str

    def publish(self, post: Post) -> PublishResult:
        """Publish a platform-independent post."""
        ...
