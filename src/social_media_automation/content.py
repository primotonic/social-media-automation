"""Reusable text-formatting and content helpers."""

import random
from datetime import datetime


def truncate(text: str | None, max_length: int = 300) -> str:
    value = " ".join((text or "No description available.").split())
    if len(value) <= max_length:
        return value
    return value[:max_length].rsplit(" ", 1)[0] + "..."


def random_daily_post(rng: random.Random | None = None) -> str:
    day = datetime.now().strftime("%A")
    templates = [
        "🌸 {day} featured anime recommendation!",
        "👋 Hello anime fans! What are you going to watch this {day}?",
        "🔥 Happy {day}! Time for another anime adventure!",
        "🍿 It's {day}! What's on your anime watchlist today?",
        "💙 Wishing you an awesome {day}! Share your favorite anime below!",
        "📺 {day} is perfect for an anime marathon. What's first?",
        "🌟 Recommend one anime everyone should watch this {day}.",
        "🎭 Who's your favorite anime character this {day}?",
        "📖 Reading any manga this {day}? Tell us!",
        "🎶 Which anime opening is on repeat this {day}?",
        "🤔 If you could enter one anime world this {day}, where would it be?",
        "📚 Which manga deserves an anime adaptation this {day}?",
        "🎉 Happy {day}! Let's talk anime in the comments!",
    ]
    return (rng or random).choice(templates).format(day=day)
