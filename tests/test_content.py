import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from social_media_automation.content import truncate


class TruncateTests(unittest.TestCase):
    def test_returns_fallback_for_empty_descriptions(self):
        self.assertEqual(truncate(None), "No description available.")

    def test_truncates_at_a_word_boundary(self):
        self.assertEqual(truncate("one two three", 8), "one two...")


if __name__ == "__main__":
    unittest.main()
