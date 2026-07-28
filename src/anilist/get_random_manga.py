import requests
import random
import re
import html

ANILIST_URL = "https://graphql.anilist.co"

def clean_description(description):
    if not description:
        return ""

    # Decode HTML entities (e.g. &amp;, &quot;)
    description = html.unescape(description)

    # Replace <br> tags with newlines
    description = re.sub(r"<br\s*/?>", "\n", description, flags=re.IGNORECASE)

    # Remove all remaining HTML tags
    description = re.sub(r"<[^>]+>", "", description)

    # Remove AniList spoiler markup (~!spoiler!~)
    description = re.sub(r"~!(.*?)!~", r"\1", description)

    # Collapse multiple blank lines
    description = re.sub(r"\n{3,}", "\n\n", description)

    return description.strip()


def get_random_manga():
    query = """
      query ($page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        media(
          type: MANGA
          sort: POPULARITY_DESC
          averageScore_greater: 80
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
          popularity
          siteUrl
        }
      }
    }
    """

    variables = {
        "page": random.randint(1, 20),
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

    # Clean the description
    manga["description"] = clean_description(manga.get("description"))

    return manga