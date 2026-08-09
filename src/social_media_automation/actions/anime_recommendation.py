"""Anime recommendation action."""

from social_media_automation.content import truncate
from social_media_automation.integrations import AniListClient
from social_media_automation.models import Post


def build_anime_recommendation(anilist: AniListClient) -> Post:
    anime = anilist.get_random_anime()
    title = anime["title"].get("english") or anime["title"]["romaji"]
    details = []
    if anime.get("episodes"):
        details.append(f"Episodes: {anime['episodes']}")
    if anime.get("seasonYear"):
        details.append(f"Year: {anime['seasonYear']}")
    details_text = "\n".join(details)
    if details_text:
        details_text += "\n\n"

    message = f"""📺 Anime Recommendation of the Day!

🔥 {title}

📝 {truncate(anime.get('description'))}

{details_text}Genres: {', '.join(anime['genres'])}

#MoetakuTV #AnimeRecommendation #Anime #Otaku #AnimeFans #AnimeCommunity #WatchAnime"""
    comment = f"""▶️ Watch {title}:

🌐 https://moetaku.tv
🌐 https://moetaku.online"""
    return Post(
        message=message,
        image_url=anime["coverImage"]["large"],
        first_comment=comment,
    )
