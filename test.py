import requests

def get_page(user_token):
    url = "https://graph.facebook.com/v25.0/me/accounts"

    r = requests.get(
        url,
        params={
            "access_token": user_token
        }
    )

    data = r.json()

    if "data" not in data or not data["data"]:
        raise Exception("No Facebook Pages found.")

    return {
        "page_id": data["data"][0]["id"],
        "page_name": data["data"][0]["name"],
        "page_token": data["data"][0]["access_token"]
    }


def create_post(page_id, message):
    return {
        "page_id": page_id,
        "message": message.strip()
    }


def preview_post(post):
    print("=== Facebook Post ===")
    print("Page ID:", post["page_id"])
    print("Message:")
    print(post["message"])
    print("=====================")


def post_to_facebook_page(page_id, page_token, message):
    url = f"https://graph.facebook.com/v25.0/{page_id}/feed"

    r = requests.post(
        url,
        data={
            "message": message,
            "access_token": page_token
        }
    )

    return r.json()


USER_TOKEN = "EAAUJX1oDWogBR25NWMOvcXxqgmWtz9V15HdegmB5hqQnpLyd7Pg2RYwetbGfIV0dZAbbZCWu0DftECUVcP4GN0zYi1TBQ2jewf3pwYq1tcNwrm6j1a0ebZAfbNaFBBhvHLmvw8vgcNSaHEV7JbBobk19gbZCY3RSBj5srpcKKPcOa14zcZArZCHWA0pV0Jd9vihtkwVGihWc9Y0QYhEZCrYu5uVQDLe2qO2PTJPz5S7Vi6JGeqbkdTMlFZChVthwqhXzrSpnSwU9L3Kt4iWRdhKM0wZDZD"

page = get_page(USER_TOKEN)

post = create_post(
    page["page_id"],
    """Test post scraped from my website.

This is where your scraped content goes."""
)

preview_post(post)

# Publish the post
result = post_to_facebook_page(
    page["page_id"],
    page["page_token"],
    post["message"]
)

print(result)