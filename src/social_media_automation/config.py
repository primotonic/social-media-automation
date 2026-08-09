"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    facebook_user_token: str
    facebook_graph_api_version: str = "v19.0"
    request_timeout_seconds: float = 30.0

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        token = os.getenv("FB_USER_TOKEN", "").strip()
        if not token:
            raise ValueError("FB_USER_TOKEN is required.")

        return cls(
            facebook_user_token=token,
            facebook_graph_api_version=os.getenv(
                "FACEBOOK_GRAPH_API_VERSION", "v19.0"
            ),
            request_timeout_seconds=float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30")),
        )
