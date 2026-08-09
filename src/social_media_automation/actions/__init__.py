"""Available automation actions and their registry."""

from collections.abc import Callable

from social_media_automation.integrations import AniListClient
from social_media_automation.models import Post

from .character_spotlight import build_character_spotlight
from .daily_post import build_daily_post
from .manga_recommendation import build_manga_recommendation

Action = Callable[[AniListClient], Post]

ACTIONS: dict[str, Action] = {
    "character_spotlight": build_character_spotlight,
    "manga_recommendation": build_manga_recommendation,
    "random_daily_posts": build_daily_post,
}

__all__ = ["ACTIONS", "Action"]
