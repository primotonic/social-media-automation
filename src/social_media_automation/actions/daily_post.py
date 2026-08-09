"""Daily engagement text action."""

from social_media_automation.content import random_daily_post
from social_media_automation.integrations import AniListClient
from social_media_automation.models import Post


def build_daily_post(_: AniListClient) -> Post:
    return Post(
        message=random_daily_post(),
        first_comment="""Watch anime & read manga here:
https://moetaku.tv
https://moetaku.online""",
    )
