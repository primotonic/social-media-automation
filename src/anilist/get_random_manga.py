import requests
import random

ANILIST_URL = "https://graphql.anilist.co"

def get_random_manga():
    query = """
    query ($page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        media(
          type: MANGA
        ) {
          id
          title {
            romaji
            english
          }
          coverImage {
            large
          }
          description(asHtml: false)
          genres
          averageScore
          siteUrl
        }
      }
    }
    """

    variables = {
        # AniList has many manga entries, pick a random area
        "page": random.randint(1, 500),
        "perPage": 10
    }

    response = requests.post(
        ANILIST_URL,
        json={
            "query": query,
            "variables": variables
        }
    )

    data = response.json()

    manga_list = data["data"]["Page"]["media"]

    manga = random.choice(manga_list)

    return manga