"""Command-line interface and dependency wiring."""

import argparse

from social_media_automation.actions import ACTIONS
from social_media_automation.config import Settings
from social_media_automation.integrations import AniListClient
from social_media_automation.providers import FacebookPageProvider


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Publish social media content.")
    parser.add_argument("action", choices=sorted(ACTIONS), help="Content action to run")
    parser.add_argument(
        "--platform",
        default="facebook",
        choices=("facebook",),
        help="Target platform (default: facebook)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = Settings.from_env()
    anilist = AniListClient(timeout=settings.request_timeout_seconds)

    providers = {
        "facebook": FacebookPageProvider(
            user_token=settings.facebook_user_token,
            api_version=settings.facebook_graph_api_version,
            timeout=settings.request_timeout_seconds,
        )
    }
    result = providers[args.platform].publish(ACTIONS[args.action](anilist))
    print(f"Published {args.action} to {result.platform} (post {result.post_id}).")
    return 0
