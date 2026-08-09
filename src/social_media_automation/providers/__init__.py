"""Social platform provider implementations."""

from .base import SocialProvider
from .facebook import FacebookPageProvider

__all__ = ["FacebookPageProvider", "SocialProvider"]
