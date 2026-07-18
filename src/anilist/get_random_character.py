import math
import random
import requests

ANILIST_API = "https://graphql.anilist.co"

QUERY = """
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    pageInfo {
      total
    }
    characters {
      id
      name {
        full
        native
      }
      image {
        large
      }
      description
      favourites
      media(perPage: 3) {
        nodes {
          title {
            english
            romaji
          }
        }
      }
    }
  }
}
"""


def get_random_character():
    per_page = 50

    # Get the total number of characters
    response = requests.post(
        ANILIST_API,
        json={
            "query": QUERY,
            "variables": {
                "page": 1,
                "perPage": 1,
            },
        },
    )

    response.raise_for_status()

    total = response.json()["data"]["Page"]["pageInfo"]["total"]

    # Calculate the number of pages
    last_page = math.ceil(total / per_page)

    # Keep trying until we find a page with characters
    while True:
        random_page = random.randint(1, last_page)

        response = requests.post(
            ANILIST_API,
            json={
                "query": QUERY,
                "variables": {
                    "page": random_page,
                    "perPage": per_page,
                },
            },
        )

        if response.status_code != 200:
            continue

        data = response.json()

        if "errors" in data:
            continue

        characters = data["data"]["Page"]["characters"]

        if not characters:
            continue

        return random.choice(characters)