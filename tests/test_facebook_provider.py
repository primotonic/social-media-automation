import sys
from pathlib import Path
import unittest
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from social_media_automation.models import Post
from social_media_automation.providers.facebook import FacebookPageProvider


def response(payload):
    result = Mock()
    result.json.return_value = payload
    result.raise_for_status.return_value = None
    return result


class FacebookProviderTests(unittest.TestCase):
    def test_publishes_image_and_first_comment(self):
        session = Mock()
        session.request.side_effect = [
            response({"data": [{"id": "page-1", "name": "Page", "access_token": "page-token"}]}),
            response({"id": "post-1"}),
            response({"id": "comment-1"}),
        ]
        provider = FacebookPageProvider("user-token", session=session)

        result = provider.publish(Post("Caption", "https://image.test/a.jpg", "First!"))

        self.assertEqual(result.post_id, "post-1")
        self.assertEqual(session.request.call_count, 3)
        publish_call = session.request.call_args_list[1]
        self.assertIn("/page-1/photos", publish_call.args[1])
        self.assertEqual(publish_call.kwargs["data"]["caption"], "Caption")

    def test_reuses_resolved_page(self):
        session = Mock()
        session.request.side_effect = [
            response({"data": [{"id": "page-1", "name": "Page", "access_token": "page-token"}]}),
            response({"id": "post-1"}),
            response({"id": "post-2"}),
        ]
        provider = FacebookPageProvider("user-token", session=session)

        provider.publish(Post("First"))
        provider.publish(Post("Second"))

        account_calls = [call for call in session.request.call_args_list if "/me/accounts" in call.args[1]]
        self.assertEqual(len(account_calls), 1)


if __name__ == "__main__":
    unittest.main()
