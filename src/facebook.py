import requests

def get_page(user_token):
    url = "https://graph.facebook.com/v19.0/me/accounts"

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


def post_to_facebook_page(page_id, page_token, message):
    url = f"https://graph.facebook.com/v19.0/{page_id}/feed"

    r = requests.post(
        url,
        data={
            "message": message,
            "access_token": page_token
        }
    )

    return r.json()

def post_single_image_to_facebook_page(page_id, page_token, message, image_url=None):

    url = f"https://graph.facebook.com/v19.0/{page_id}/photos"

    data = {
        "caption": message,
        "access_token": page_token
    }

    if image_url:
        data["url"] = image_url

    response = requests.post(
        url,
        data=data
    )

    return response.json()