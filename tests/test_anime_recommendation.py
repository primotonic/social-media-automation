import random
import sys
from pathlib import Path
import unittest
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from social_media_automation.actions.anime_recommendation import (
    build_anime_recommendation,
)
from social_media_automation.integrations.anilist import AniListClient


class AnimeRecommendationTests(unittest.TestCase):
    def test_builds_post_from_anilist_anime(self):
        anilist = Mock()
        anilist.get_random_anime.return_value = {
            "title": {"english": "Frieren", "romaji": "Sousou no Frieren"},
            "description": "An elven mage begins a new journey.",
            "genres": ["Adventure", "Fantasy"],
            "episodes": 28,
            "seasonYear": 2023,
            "coverImage": {"large": "https://image.test/frieren.jpg"},
        }

        post = build_anime_recommendation(anilist)

        self.assertIn("Frieren", post.message)
        self.assertIn("Episodes: 28", post.message)
        self.assertIn("Adventure, Fantasy", post.message)
        self.assertEqual(post.image_url, "https://image.test/frieren.jpg")
        self.assertIn("Watch Frieren", post.first_comment)

    def test_anilist_client_requests_finished_anime(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "data": {
                "Page": {
                    "media": [
                        {
                            "title": {"english": None, "romaji": "Test Anime"},
                            "description": "A <b>great</b> show.",
                            "genres": ["Drama"],
                            "coverImage": {"large": "https://image.test/anime.jpg"},
                        }
                    ]
                }
            }
        }
        session = Mock()
        session.post.return_value = response
        client = AniListClient(session=session, rng=random.Random(1))

        anime = client.get_random_anime()

        query = session.post.call_args.kwargs["json"]["query"]
        self.assertIn("type: ANIME", query)
        self.assertIn("status: FINISHED", query)
        self.assertEqual(anime["description"], "A great show.")


if __name__ == "__main__":
    unittest.main()
