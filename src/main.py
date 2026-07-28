import sys
import random
from config import FB_USER_TOKEN
from anilist.get_random_manga import get_random_manga
from anilist.get_random_character import get_random_character
from facebook import get_page, post_to_facebook_page, post_single_image_to_facebook_page, comment_on_post
from daily_text_posts import get_random_daily_post

page = get_page(FB_USER_TOKEN)

def random_manga():
    random_manga = get_random_manga()

    title = (
        random_manga["title"].get("english")
        or random_manga["title"].get("romaji")
    )

    message = f"""📚 Manga Recommendation of the Day!

🔥 {title}

Description: {random_manga['description']}

Genres: {', '.join(random_manga['genres'])}
"""

    result = post_single_image_to_facebook_page(
        page["page_id"],
        page["page_token"],
        message,
        random_manga["coverImage"]["large"],
    )

    print(result)


def character_spotlight():
    character = get_random_character()

    anime = "Unknown"

    media = character["media"]["nodes"][0]
    media_type = media["type"]  # "ANIME" or "MANGA"
    title = (
        media["title"].get("english")
        or media["title"].get("romaji")
    )
    emoji = "📺" if media_type == "ANIME" else "📚"

    if character["media"]["nodes"]:
        media = character["media"]["nodes"][0]
        anime = (
            media["title"].get("english")
            or media["title"].get("romaji")
        )

    description = character["description"] or "No description available."
    description = (
        description
        .replace("\n", " ")
        .replace("__", "")
        .replace("~!", "")
        .replace("!~", "")
    )

    MAX_LENGTH = 300
    if len(description) > MAX_LENGTH:
        description = description[:MAX_LENGTH].rsplit(" ", 1)[0] + "..."

    message = f"""🎭 Character Spotlight!

✨ {character["name"]["full"]}

{emoji} {media_type.title()}: {title}

📝 Description:
{description}

#MoetakuTV #CharacterSpotlight #Anime #Manga
"""

    footer = """

Watch anime & read manga here:
https://moetaku.tv
https://moetaku.online
"""

    comments = [
        f"""Have you watched {anime}? Tell us what you think!{footer}""",

        f"""⭐ Is {character['name']['full']} one of your favorite characters?{footer}""",

        f"""🔥 Would you recommend {anime} to other anime fans?{footer}""",

        f"""❤️ What's your favorite moment featuring {character['name']['full']}?{footer}""",

        f"""👇 Share your thoughts below! We'd love to hear from you!{footer}""",
    ]

    comment_message = random.choice(comments)

    result = post_single_image_to_facebook_page(
        page["page_id"],
        page["page_token"],
        message,
        character["image"]["large"],
        comment_message=comment_message,
    )

    return result

def random_daily_posts():
    message = get_random_daily_post()
    result = post_to_facebook_page(
        page["page_id"],
        page["page_token"], 
        message
    )

    comment_on_post(
        result["id"], 
        page["page_token"],
        """Watch anime & read manga here:
https://moetaku.tv
https://moetaku.online"""
    )

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/main.py [manga|character_spotlight|random_daily_posts]")
        return

    command = sys.argv[1].lower()

    if command == "manga":
        random_manga()
    elif command == "character_spotlight":
        character_spotlight()
    elif command == "random_daily_posts":
        random_daily_posts()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

# random_daily_posts()