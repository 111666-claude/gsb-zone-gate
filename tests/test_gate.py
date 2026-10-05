import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zonegate.gate import Gates  # noqa: E402

ZONES = {"cave": {"level": 5, "requires": [], "cooldown_ms": 1000, "daily_limit": 2}}


class GatesTest(unittest.TestCase):
    def test_high_level_is_allowed(self):
        self.assertTrue(Gates(ZONES).allowed("p1", "cave", 9, [], 1, 0))

    def test_iter_is_lazy(self):
        stream = Gates(ZONES).iter_allowed("p1", 9, [], 1, 0)
        self.assertEqual(list(stream), ["cave"])

    def test_unknown_zone_raises(self):
        with self.assertRaises(KeyError):
            Gates(ZONES).allowed("p1", "nope", 9, [], 1, 0)


if __name__ == "__main__":
    unittest.main()
