"""Backward-compatible entry point for the automation CLI."""

from social_media_automation.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
