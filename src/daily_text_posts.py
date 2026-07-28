import random
from datetime import datetime

def get_random_daily_post():
    today = datetime.now().strftime("%A")

    posts = [
        f"🌸 {today} featured anime recommendation!",
        f"👋 Hello anime fans! What are you going to watch this {today}?",
        f"🔥 Happy {today}! Time for another anime adventure!",
        f"🍿 It's {today}! What's on your anime watchlist today?",
        f"💙 Wishing you an awesome {today}! Share your favorite anime below!",
        f"🎌 Happy {today}! Which anime are you watching today?",
        f"📺 {today} is perfect for an anime marathon. What's first?",
        f"🌟 Recommend one anime everyone should watch this {today}.",
        f"🎭 Who's your favorite anime character this {today}?",
        f"📖 Reading any manga this {today}? Tell us!",
        f"🍜 Best anime to watch while eating ramen this {today}?",
        f"🎥 Drop your current anime obsession this {today}!",
        f"❤️ Make someone's {today}! Recommend your favorite anime.",
        f"🔥 What's the most underrated anime you've seen this {today}?",
        f"🎶 Which anime opening is on repeat this {today}?",
        f"🤔 If you could enter one anime world this {today}, where would it be?",
        f"💬 Describe your favorite anime using only three words this {today}.",
        f"🏆 What's your Anime of the Year so far this {today}?",
        f"✨ {today} challenge: Name an anime without using its title!",
        f"🎬 Watching anything new this {today}? Share it below!",
        f"🎮 Anime and games go together! What are you playing this {today}?",
        f"🌅 Start your {today} with a great anime recommendation!",
        f"📚 Which manga deserves an anime adaptation this {today}?",
        f"🎉 Happy {today}! Let's talk anime in the comments!",
    ]

    return random.choice(posts)

def other_post_but_different_topic():
    pass