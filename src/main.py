from config import FB_USER_TOKEN
from anilist.get_random_manga import get_random_manga
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
        random_manga["coverImage"]["large"]
    )

    # print(random_manga)

def main():
    random_manga()
    # latest_anime_episode()
    # character_spotlight()
    # manga_news()

if __name__ == "__main__":
    main()