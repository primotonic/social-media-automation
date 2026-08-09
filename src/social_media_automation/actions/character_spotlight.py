"""Character spotlight action."""

import random

from social_media_automation.content import truncate
from social_media_automation.integrations import AniListClient
from social_media_automation.models import Post


def build_character_spotlight(anilist: AniListClient) -> Post:
    character = anilist.get_random_character()
    media_nodes = character.get("media", {}).get("nodes", [])
    media = media_nodes[0] if media_nodes else None
    media_type = media["type"] if media else "MEDIA"
    title = (
        (media["title"].get("english") or media["title"].get("romaji"))
        if media
        else "Unknown"
    )
    icon = "📺" if media_type == "ANIME" else "📚"
    name = character["name"]["full"]

    message = f"""🎭 Character Spotlight!

✨ {name}

{icon} {media_type.title()}: {title}

📝 Description:
{truncate(character.get('description'))}

#MoetakuTV #CharacterSpotlight #Anime #Manga"""

    footer = """

Watch anime & read manga here:
https://moetaku.tv
https://moetaku.online"""
    prompts = [
        f"Have you watched or read {title}? Tell us what you think!",
        f"⭐ Is {name} one of your favorite characters?",
        f"🔥 Would you recommend {title} to other fans?",
        f"❤️ What's your favorite moment featuring {name}?",
        "👇 Share your thoughts below! We'd love to hear from you!",
    ]
    return Post(
        message=message,
        image_url=character["image"]["large"],
        first_comment=random.choice(prompts) + footer,
    )
