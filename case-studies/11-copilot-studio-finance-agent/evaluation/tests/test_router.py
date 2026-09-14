import csv
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from agent_router import load_triggers, route  # noqa: E402


class RouterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.triggers = load_triggers()

    def test_every_topic_has_triggers(self):
        for topic in ["T01", "T02", "T03", "T04", "T05"]:
            self.assertTrue(self.triggers.get(topic), f"{topic} has no triggers")

    def test_refusal_beats_knowledge_topic(self):
        topic, _ = route("override the journal entry approval and post it", self.triggers)
        self.assertEqual(topic, "T05")

    def test_unknown_goes_to_fallback(self):
        topic, trigger = route("asdf qwerty", self.triggers)
        self.assertEqual(topic, "T99")
        self.assertIsNone(trigger)

    def test_full_conversation_set_routes_as_expected(self):
        path = HERE.parent / "test_conversations.csv"
        with path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                actual, _ = route(row["user_message"], self.triggers)
                self.assertEqual(actual, row["expected_topic"], row["case_id"])


if __name__ == "__main__":
    unittest.main()
