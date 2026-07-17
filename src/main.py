from config import FB_USER_TOKEN
from facebook import get_page, post_to_facebook_page
from scraper import get_latest_release


page = get_page(FB_USER_TOKEN)

release = get_latest_release()

result = post_to_facebook_page(
    page["page_id"],
    page["page_token"],
    release["message"]
)

print(result)