import sys

from config import FB_USER_TOKEN
from anilist.get_random_manga import get_random_manga
from anilist.get_random_character import get_random_character
from facebook import get_page, post_single_image_to_facebook_page

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

    if character["media"]["nodes"]:
        media = character["media"]["nodes"][0]
        anime = (
            media["title"].get("english")
            or media["title"].get("romaji")
        )

    description = character["description"] or "No description available."
    description = description.replace("\n", " ").replace("__", "")
    description = description[:500] + "..." if len(description) > 500 else description

    message = f"""🎭 Character Spotlight!

✨ {character["name"]["full"]}

📺 Anime: {anime}

📝 Description:
{description}
"""

    result = post_single_image_to_facebook_page(
        page["page_id"],
        page["page_token"],
        message,
        character["image"]["large"],
    )

    print(result)

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/main.py [manga|character_spotlight]")
        return

    command = sys.argv[1].lower()

    if command == "manga":
        random_manga()
    elif command == "character_spotlight":
        character_spotlight()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
    # character_spotlight()