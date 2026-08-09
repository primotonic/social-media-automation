# Social Media Automation

Publishes anime and manga content to a Facebook Page. The application separates
content actions from social-platform APIs, so additional actions and platforms can
be introduced independently.

## Setup

Requires Python 3.11 or newer.

```bash
python -m venv .venv
pip install -r requirements.txt
```

Create a `.env` file (it is ignored by Git):

```dotenv
FB_USER_TOKEN=your-facebook-user-token
# Optional values:
FACEBOOK_GRAPH_API_VERSION=v19.0
REQUEST_TIMEOUT_SECONDS=30
```

## Run an action

```bash
python src/main.py anime_recommendation
python src/main.py manga_recommendation
python src/main.py character_spotlight
python src/main.py random_daily_posts
```

Use `python src/main.py --help` to list the currently registered actions. Existing
GitHub Actions workflows continue to use this entry point.

## Architecture

```text
src/social_media_automation/
├── actions/          # Build platform-independent Post objects
├── integrations/     # Content sources such as AniList
├── providers/        # Facebook and future social-network adapters
├── cli.py            # Command routing and dependency wiring
├── config.py         # Environment configuration
├── content.py        # Shared text/content helpers
└── models.py         # Cross-platform data models
```

### Add an action

Create a builder in `actions/` that accepts the required integrations and returns
a `Post`, then register it in `actions/__init__.py`. The action does not call
Facebook directly, so it will work with every provider that supports the post.

### Add a social platform

Create an adapter in `providers/` with a `name` and `publish(Post)` method, then
wire it into `cli.py`. Platform-specific credentials and API behavior stay inside
that adapter.

## Tests

The tests do not make network requests:

```bash
python -m unittest discover -s tests -v
```
