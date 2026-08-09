"""Manga recommendation action."""

from social_media_automation.content import truncate
from social_media_automation.integrations import AniListClient
from social_media_automation.models import Post


def build_manga_recommendation(anilist: AniListClient) -> Post:
    manga = anilist.get_random_manga()
    title = manga["title"].get("english") or manga["title"]["romaji"]
    message = f"""📚 Manga Recommendation of the Day!

🔥 {title}

Description: {truncate(manga.get('description'))}

Genres: {', '.join(manga['genres'])}

#MoetakuTV #MangaRecommendation #Manga #Anime #Otaku #MangaFans #AnimeCommunity #ReadManga"""
    comment = f"""📖 Read {title}:

🌐 https://moetaku.tv
🌐 https://moetaku.online"""
    return Post(
        message=message,
        image_url=manga["coverImage"]["large"],
        first_comment=comment,
    )
