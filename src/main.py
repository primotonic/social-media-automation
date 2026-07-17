from config import FB_USER_TOKEN
from anilist.get_random_manga import get_random_manga
from facebook import get_page, post_single_image_to_facebook_page


page = get_page(FB_USER_TOKEN)
random_manga = get_random_manga()

title = (
    random_manga["title"].get("english")
    or random_manga["title"].get("romaji")
)

message = f"""📚 Manga Recommendation of the Day!

🔥 {title}

⭐ Score: {random_manga['averageScore']}/100

Genres:
{', '.join(random_manga['genres'])}


"""

result = post_single_image_to_facebook_page(
    page["page_id"],
    page["page_token"],
    message,
    random_manga["coverImage"]["large"]
)

print(result)